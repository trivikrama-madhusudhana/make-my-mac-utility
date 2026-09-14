#!/usr/bin/env python3
"""Loopback design selection receipt and replay, using only Python's standard library."""
import argparse
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import secrets
import socket
import stat
import sys
import tempfile
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen, ProxyHandler, build_opener

MAX_HTML = 10 * 1024 * 1024
MAX_BODY = 20000
MAX_FEEDBACK = 4000
ASSET = Path(__file__).resolve().parents[1] / 'assets/design-review.html'


def now():
    return datetime.now(timezone.utc).isoformat()


def encoded(value):
    return json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')


def digest(path):
    with open(path, 'rb') as source:
        data = source.read(MAX_HTML + 1)
    if len(data) > MAX_HTML:
        raise ValueError('HTML and brief must each be at most 10 MiB.')
    return data, hashlib.sha256(data).hexdigest()


def atomic_write(path, value):
    fd, temp = tempfile.mkstemp(prefix='.' + path.name + '-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as output:
            output.write(encoded(value))
            output.flush()
            os.fsync(output.fileno())
        os.replace(temp, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def read_state(path):
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
    with os.fdopen(fd, 'rb') as source:
        info = os.fstat(source.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077:
            raise ValueError('State must be a private regular file (mode 600).')
        data = source.read(65537)
    if len(data) > 65536:
        raise ValueError('State file is too large.')
    state = json.loads(data)
    url = urlsplit(state['url'])
    if (url.scheme != 'http' or url.hostname != '127.0.0.1' or not url.port
            or url.netloc != f'127.0.0.1:{url.port}' or url.path or url.query or url.fragment):
        raise ValueError('Invalid loopback review URL in state.')
    return state


class Review:
    def __init__(self, html, brief, state_path, revision):
        self.html = Path(html).expanduser().resolve(strict=True)
        self.brief = Path(brief).expanduser().resolve(strict=True)
        # Do not resolve the final component: an existing symlink is also a collision.
        requested = Path(state_path).expanduser().absolute()
        self.path = requested.parent.resolve(strict=True) / requested.name
        if self.path in (self.html, self.brief):
            raise ValueError('State must be separate from HTML and brief.')
        if not revision.strip() or len(revision) > 200:
            raise ValueError('Revision must be a nonempty label of at most 200 characters.')
        self.preview, html_hash = digest(self.html)
        _, brief_hash = digest(self.brief)
        self.template = ASSET.read_text()
        self.condition = threading.Condition()
        self.waiters = 0
        self.state = dict(version=1, review_id=secrets.token_hex(16), revision=revision,
                          html=str(self.html), brief=str(self.brief), html_sha256=html_hash,
                          brief_sha256=brief_hash, token=secrets.token_urlsafe(32),
                          created_at=now(), lifecycle='running', selection=None,
                          delivered_at=None, stale=False)
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), self.handler())
        self.server.daemon_threads = True
        self.server.request_queue_size = 16
        self.state['url'] = f'http://127.0.0.1:{self.server.server_port}'
        try:
            # O_EXCL reserves this round without overwriting any prior evidence.
            fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd, 'wb') as output:
                output.write(encoded(self.state))
                output.flush()
                os.fsync(output.fileno())
        except BaseException:
            self.server.server_close()
            raise

    def persist(self):
        atomic_write(self.path, self.state)

    def stale(self):
        try:
            changed = (digest(self.html)[1] != self.state['html_sha256'] or
                       digest(self.brief)[1] != self.state['brief_sha256'])
        except (OSError, ValueError):
            changed = True
        if changed and not self.state['stale']:
            self.state['stale'] = True
            self.persist()
            self.condition.notify_all()
        return self.state['stale']

    def public(self):
        return {key: value for key, value in self.state.items() if key not in ('token', 'url')} | {
            'waiting_clients': self.waiters}

    def handler(self):
        review = self

        class Handler(BaseHTTPRequestHandler):
            server_version = 'DesignReview/1'

            def log_message(self, *_):
                pass  # Never log the token or submitted feedback.

            def setup(self):
                super().setup()
                self.connection.settimeout(5)

            def reply(self, status, body, content_type='application/json', preview=False, nonce=None):
                if not isinstance(body, bytes):
                    body = encoded(body)
                self.send_response(status)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(body)))
                self.send_header('Cache-Control', 'no-store')
                self.send_header('Referrer-Policy', 'no-referrer')
                self.send_header('X-Content-Type-Options', 'nosniff')
                self.send_header('Permissions-Policy', 'camera=(), microphone=(), geolocation=()')
                self.send_header('Connection', 'close')
                if preview:
                    csp = ("default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
                           "img-src data:; font-src data:; connect-src 'none'; frame-src 'none'; "
                           "form-action 'none'; base-uri 'none'; sandbox allow-scripts; frame-ancestors 'self'")
                else:
                    csp = (f"default-src 'none'; script-src 'nonce-{nonce}'; style-src 'unsafe-inline'; "
                           "connect-src 'self'; frame-src 'self'; base-uri 'none'; form-action 'none'; "
                           "frame-ancestors 'none'")
                self.send_header('Content-Security-Policy', csp)
                self.end_headers()
                try:
                    self.wfile.write(body)
                except (BrokenPipeError, ConnectionResetError, socket.timeout):
                    pass

            def valid_host(self):
                return self.headers.get_all('Host') == [urlsplit(review.state['url']).netloc]

            def do_GET(self):
                if not self.valid_host():
                    return self.reply(403, {'error': 'Wrong Host.'})
                if self.path == '/':
                    nonce = secrets.token_urlsafe(24)
                    page = review.template.replace('__NONCE__', nonce)
                    return self.reply(200, page.encode(), 'text/html; charset=utf-8', nonce=nonce)
                if self.path == '/preview':
                    return self.reply(200, review.preview, 'text/html; charset=utf-8', preview=True)
                self.reply(404, {'error': 'Unknown path.'})

            def do_POST(self):
                if not self.valid_host() or self.headers.get_all('Origin') != [review.state['url']]:
                    return self.reply(403, {'error': 'Wrong Host or Origin.'})
                if self.headers.get_all('X-Review-Token') != [review.state['token']]:
                    return self.reply(403, {'error': 'Invalid review token.'})
                if self.path not in ('/api/status', '/api/select', '/api/wait', '/api/ack', '/api/stop'):
                    return self.reply(404, {'error': 'Unknown path.'})
                lengths = self.headers.get_all('Content-Length')
                try:
                    if (not lengths or len(lengths) != 1 or self.headers.get('Transfer-Encoding')
                            or self.headers.get('Content-Type') != 'application/json'):
                        raise ValueError()
                    length = int(lengths[0])
                    if not 0 < length <= MAX_BODY:
                        return self.reply(413, {'error': 'Request body must be 1–20000 bytes.'})
                    raw = self.rfile.read(length)
                    if len(raw) != length:
                        raise ValueError()
                    payload = json.loads(raw)
                    if not isinstance(payload, dict):
                        raise ValueError()
                except (ValueError, UnicodeError, socket.timeout):
                    return self.reply(400, {'error': 'Invalid JSON request.'})
                with review.condition:
                    if (payload.get('review_id') != review.state['review_id']
                            and not (self.path == '/api/status' and payload.get('review_id') is None)):
                        return self.reply(409, {'error': 'Wrong review. Open the current review URL.'})
                    if self.path == '/api/stop':
                        review.state['lifecycle'] = 'stopped'
                        review.persist()
                        review.condition.notify_all()
                        self.reply(200, review.public())
                        threading.Thread(target=review.server.shutdown, daemon=True).start()
                        return
                    if self.path == '/api/ack':
                        if review.state['selection'] is None:
                            return self.reply(409, {'error': 'No selection to acknowledge.'})
                        review.state['delivered_at'] = review.state['delivered_at'] or now()
                        review.persist()
                        return self.reply(200, review.public())
                    stale = review.stale()
                    if self.path == '/api/select':
                        choice, feedback = payload.get('choice'), payload.get('feedback', '')
                        if (choice not in ('A', 'B', 'C', 'None') or not isinstance(feedback, str)
                                or len(feedback) > MAX_FEEDBACK):
                            return self.reply(400, {'error': 'Choose A, B, C or None; feedback is limited to 4000 characters.'})
                        if stale:
                            return self.reply(409, {'error': 'HTML or brief changed. Start a new review.', 'stale': True})
                        if review.state['lifecycle'] != 'running':
                            return self.reply(409, {'error': 'Review has ended. Start a new review.'})
                        previous = review.state['selection']
                        if previous:
                            if previous['choice'] != choice or previous['feedback'] != feedback:
                                return self.reply(409, {'error': 'A different choice is already saved. Start a new review to change it.'})
                        else:
                            review.state['selection'] = dict(
                                choice=choice, feedback=feedback, selected_at=now(),
                                review_id=review.state['review_id'], revision=review.state['revision'],
                                html=review.state['html'], brief=review.state['brief'],
                                html_sha256=review.state['html_sha256'], brief_sha256=review.state['brief_sha256'],
                                evidence='explicit_browser_choice', build_authorized=False)
                            try:
                                review.persist()  # Receipt follows durable replacement.
                            except OSError:
                                review.state['selection'] = None
                                return self.reply(500, {'error': 'Could not save receipt. Retry after checking local storage.'})
                            review.condition.notify_all()
                    if self.path == '/api/wait':
                        seconds = payload.get('timeout', 30)
                        if isinstance(seconds, bool) or not isinstance(seconds, (float, int)) or not 0 <= seconds <= 30:
                            return self.reply(400, {'error': 'Wait timeout must be between 0 and 30 seconds.'})
                        review.waiters += 1
                        try:
                            deadline = time.monotonic() + seconds
                            while (not review.state['selection'] and not review.state['stale']
                                   and review.state['lifecycle'] == 'running'):
                                remaining = deadline - time.monotonic()
                                if remaining <= 0:
                                    break
                                review.condition.wait(min(remaining, 0.5))
                                review.stale()
                            return self.reply(200, review.public())
                        finally:
                            review.waiters -= 1
                    self.reply(200, review.public())
        return Handler

    def run(self):
        try:
            self.server.serve_forever(poll_interval=0.2)
        finally:
            with self.condition:
                self.state['lifecycle'] = 'stopped'
                self.persist()
                self.condition.notify_all()
            self.server.server_close()


def request(state, endpoint, **fields):
    req = Request(state['url'] + '/api/' + endpoint,
                  data=encoded(dict(review_id=state['review_id'], **fields)),
                  headers={'Origin': state['url'], 'X-Review-Token': state['token'],
                           'Content-Type': 'application/json'}, method='POST')
    # A machine's proxy settings must never send this token outside loopback.
    with build_opener(ProxyHandler({})).open(req, timeout=35) as response:
        return json.load(response)


def result_summary(state, connection):
    status = 'selected' if state.get('selection') else 'pending'
    if state.get('stale'):
        status = 'stale'
    elif not state.get('selection') and state.get('lifecycle') != 'running':
        status = 'ended'
    return dict(status=status, connection=connection, review_id=state['review_id'],
                revision=state['revision'], selection=state.get('selection'),
                stale=state.get('stale', False), lifecycle=state.get('lifecycle'),
                delivered_at=state.get('delivered_at'), waiting_clients=state.get('waiting_clients', 0))


def client(command, path, timeout=30):
    state = read_state(path)
    try:
        if command == 'stop':
            live = request(state, 'stop')
        elif command == 'wait':
            live = request(state, 'wait', timeout=timeout)
            if live.get('selection'):
                live = request(state, 'ack')
        else:
            live = request(state, 'status')
        return result_summary(live, 'server_connected')
    except HTTPError as error:
        # Authentication failures must never be disguised as an offline success.
        raise ValueError(f'Review server rejected {command}: HTTP {error.code}.') from error
    except (URLError, TimeoutError, ConnectionError, OSError):
        state = read_state(path)
        # Replayed evidence must be checked against today's files, even after stop/crash.
        try:
            state['stale'] = state.get('stale', False) or (
                digest(state['html'])[1] != state['html_sha256'] or
                digest(state['brief'])[1] != state['brief_sha256'])
        except (OSError, ValueError):
            state['stale'] = True
        # Saved results survive the server or client exiting; never claim a live waiter.
        summary = result_summary(state, 'server_unavailable')
        if not state.get('selection') and not state.get('stale'):
            summary['status'] = 'unavailable'
        return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    serve = commands.add_parser('serve')
    for flag in ('html', 'brief', 'state', 'revision'):
        serve.add_argument('--' + flag, required=True)
    for command in ('status', 'wait', 'stop'):
        sub = commands.add_parser(command)
        sub.add_argument('--state', required=True, type=Path)
        if command == 'wait':
            sub.add_argument('--timeout', type=float, default=30)
    args = parser.parse_args()
    try:
        if args.command == 'serve':
            review = Review(args.html, args.brief, args.state, args.revision)
            print(json.dumps(dict(status='serving', review_id=review.state['review_id'],
                                  url=review.state['url'] + '/#' + review.state['token'],
                                  state=str(review.path), html=str(review.html), brief=str(review.brief))), flush=True)
            try:
                review.run()
            except KeyboardInterrupt:
                pass
        else:
            if args.command == 'wait' and not 0 <= args.timeout <= 30:
                raise ValueError('Use bounded wait cycles of 0–30 seconds.')
            print(json.dumps(client(args.command, args.state, getattr(args, 'timeout', 30))), flush=True)
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({'status': 'error', 'error': str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
