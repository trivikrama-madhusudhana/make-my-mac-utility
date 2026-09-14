"""Deterministic loopback integration tests; disposable input and state files only."""
import concurrent.futures
import http.client
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest import mock
from urllib.error import HTTPError

HELPER = Path(__file__).resolve().parents[1] / 'skills/make-my-mac-utility/scripts/design_review.py'
spec = importlib.util.spec_from_file_location('design_review', HELPER)
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)


class DesignReview(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='utility-review-test-')
        self.root = Path(self.temp.name)
        self.html = self.root / 'options with spaces.html'
        self.brief = self.root / 'brief.md'
        self.html.write_text('<!doctype html><title>Options</title><script>window.example = true</script>A B C')
        self.brief.write_text('# Agreed brief\nLocal sample data only.\n')
        self.before = (self.html.read_bytes(), self.brief.read_bytes())
        self.path = self.root / 'round-1.json'
        self.review = bridge.Review(self.html, self.brief, self.path, 'round 1')
        self.thread = threading.Thread(target=self.review.run)
        self.thread.start()

    def tearDown(self):
        if self.thread.is_alive():
            bridge.request(self.review.state, 'stop')
        self.thread.join(timeout=3)
        self.assertFalse(self.thread.is_alive(), 'server did not stop')
        self.assertTrue(self.path.is_file(), 'receipt evidence was deleted')
        self.assertFalse(list(self.root.glob('.round-1.json-*')), 'atomic write left temporary files')
        self.temp.cleanup()

    def request(self, endpoint='select', **fields):
        return bridge.request(self.review.state, endpoint, **fields)

    def wire(self, method, path, body=None, headers=None):
        client = http.client.HTTPConnection('127.0.0.1', self.review.server.server_port, timeout=3)
        try:
            client.request(method, path, body=body, headers=headers or {})
            result = client.getresponse()
            return result.status, dict(result.getheaders()), result.read()
        finally:
            client.close()

    def post(self, endpoint='/api/select', **overrides):
        headers = {'Host': self.review.state['url'].split('//')[1],
                   'Origin': self.review.state['url'], 'X-Review-Token': self.review.state['token'],
                   'Content-Type': 'application/json'}
        headers.update(overrides)
        return self.wire('POST', endpoint, json.dumps(dict(
            review_id=self.review.state['review_id'], choice='A', feedback='')), headers)

    def test_active_cli_waiter_gets_selection_and_replay_survives_stop(self):
        waiter = subprocess.Popen([sys.executable, str(HELPER), 'wait', '--state', str(self.path), '--timeout', '5'],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            deadline = time.monotonic() + 3
            while not self.request('status')['waiting_clients']:
                if time.monotonic() > deadline:
                    self.fail('CLI waiter did not connect')
                time.sleep(0.02)
            receipt = self.request(choice='B', feedback='Keep the compact layout.')
            stdout, stderr = waiter.communicate(timeout=3)
            self.assertEqual(waiter.returncode, 0, stderr)
            delivered = json.loads(stdout)
            self.assertEqual(delivered['status'], 'selected')
            self.assertEqual(delivered['selection'], receipt['selection'])
            self.assertIsNotNone(delivered['delivered_at'])
            replay = bridge.client('wait', self.path, 0)
            self.assertEqual(replay['selection'], receipt['selection'])
            self.request('stop')
            self.thread.join(3)
            offline = bridge.client('wait', self.path, 0)
            self.assertEqual(offline['connection'], 'server_unavailable')
            self.assertEqual(offline['selection'], receipt['selection'])
            self.assertEqual((self.html.read_bytes(), self.brief.read_bytes()), self.before)
        finally:
            if waiter.poll() is None:
                waiter.kill()
                waiter.communicate()

    def test_offline_replay_rechecks_source_hashes_and_missing_files(self):
        selected = self.request(choice='A')['selection']
        self.request('stop')
        self.thread.join(3)
        self.brief.write_text('Changed after server stop')
        result = bridge.client('wait', self.path, 0)
        self.assertEqual(result['status'], 'stale')
        self.assertEqual(result['selection'], selected)
        self.brief.write_bytes(self.before[1])
        self.html.unlink()
        self.assertEqual(bridge.client('status', self.path)['status'], 'stale')

    def test_identical_retry_and_conflicting_selection(self):
        first = self.request(choice='A', feedback='A clear layout')
        persisted = self.path.read_bytes()
        again = self.request(choice='A', feedback='A clear layout')
        self.assertEqual(first['selection'], again['selection'])
        self.assertEqual(self.path.read_bytes(), persisted)
        for change in (dict(choice='B', feedback='A clear layout'), dict(choice='A', feedback='Changed')):
            with self.assertRaises(HTTPError) as error:
                self.request(**change)
            self.assertEqual(error.exception.code, 409)
        self.assertEqual(self.path.read_bytes(), persisted)

    def test_none_delivers_feedback_and_never_build_permission(self):
        selected = self.request(choice='None', feedback='Try a single-column design.')['selection']
        self.assertEqual(selected['choice'], 'None')
        self.assertEqual(selected['feedback'], 'Try a single-column design.')
        self.assertFalse(selected['build_authorized'])
        self.assertEqual(selected['html_sha256'], bridge.digest(self.html)[1])
        self.assertEqual(selected['brief_sha256'], bridge.digest(self.brief)[1])
        self.assertEqual(selected['review_id'], self.review.state['review_id'])

    def test_none_with_empty_feedback_is_a_complete_choice(self):
        selected = self.request(choice='None', feedback='')['selection']
        self.assertEqual(selected['choice'], 'None')
        self.assertEqual(selected['feedback'], '')
        self.assertFalse(selected['build_authorized'])
        page = self.wire('GET', '/')[2]
        self.assertIn(b'(optional for any choice)', page)
        self.assertNotIn(b'feedback.value.trim()', page)

    def test_changed_html_or_brief_invalidates_round_permanently(self):
        self.brief.write_text('Changed brief')
        with self.assertRaises(HTTPError) as error:
            self.request(choice='C')
        self.assertEqual(error.exception.code, 409)
        self.brief.write_bytes(self.before[1])
        self.assertTrue(self.request('status')['stale'])
        self.assertEqual(bridge.client('wait', self.path, 0)['status'], 'stale')
        self.assertIsNone(bridge.read_state(self.path)['selection'])

    def test_changed_html_while_waiting_returns_stale(self):
        with concurrent.futures.ThreadPoolExecutor() as pool:
            future = pool.submit(bridge.client, 'wait', self.path, 3)
            self.html.write_text('Revised options')
            result = future.result(timeout=3)
        self.assertEqual(result['status'], 'stale')

    def test_tokens_origins_hosts_and_review_ids(self):
        for headers in ({'X-Review-Token':'wrong'}, {'Origin':'null'}, {'Origin':'http://evil.example'},
                        {'Host':'localhost:' + str(self.review.server.server_port)}, {'Host':'evil.example'}):
            self.assertEqual(self.post(**headers)[0], 403)
        state = dict(self.review.state, review_id='another-round')
        with self.assertRaises(HTTPError) as error:
            bridge.request(state, 'select', choice='A', feedback='')
        self.assertEqual(error.exception.code, 409)
        self.assertEqual(self.post('/api/stop', **{'X-Review-Token':'bad'})[0], 403)
        self.assertEqual(self.request('status')['lifecycle'], 'running')
        self.assertNotIn('token', self.request('status'))

    def test_iframe_isolation_named_routes_and_body_bounds(self):
        status, headers, page = self.wire('GET', '/')
        self.assertEqual(status, 200)
        self.assertIn(b'sandbox="allow-scripts"', page)
        self.assertNotIn(b'allow-same-origin', page)
        self.assertIn(b'src="/preview"', page)
        self.assertNotIn(self.review.state['token'].encode(), page)
        self.assertIn("frame-ancestors 'none'", headers['Content-Security-Policy'])
        status, headers, preview = self.wire('GET', '/preview')
        self.assertEqual(preview, self.before[0])
        self.assertIn('sandbox allow-scripts', headers['Content-Security-Policy'])
        self.assertIn("connect-src 'none'", headers['Content-Security-Policy'])
        self.assertIn("form-action 'none'", headers['Content-Security-Policy'])
        for path in ('/../brief.md', '/%2e%2e/brief.md', '/preview?file=brief.md', '/round-1.json', '/favicon.ico'):
            self.assertEqual(self.wire('GET', path)[0], 404)
        self.assertEqual(self.post(**{'Content-Length': str(bridge.MAX_BODY + 1)})[0], 413)
        with self.assertRaises(HTTPError) as error:
            self.request(choice='A', feedback='x' * (bridge.MAX_FEEDBACK + 1))
        self.assertEqual(error.exception.code, 400)

    def test_private_unique_state_and_preservation(self):
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        before = self.path.read_bytes()
        with self.assertRaises(FileExistsError):
            bridge.Review(self.html, self.brief, self.path, 'another')
        self.assertEqual(self.path.read_bytes(), before)
        link = self.root / 'link.json'
        link.symlink_to(self.path)
        with self.assertRaises(FileExistsError):
            bridge.Review(self.html, self.brief, link, 'another')
        self.assertEqual(self.path.read_bytes(), before)
        self.request(choice='C')
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
        os.chmod(self.path, 0o644)
        with self.assertRaisesRegex(ValueError, 'private'):
            bridge.read_state(self.path)
        os.chmod(self.path, 0o600)

    def test_pending_timeout_and_no_auto_selection(self):
        result = bridge.client('wait', self.path, 0.05)
        self.assertEqual(result['status'], 'pending')
        self.assertIsNone(result['selection'])
        self.assertEqual(self.request('status')['waiting_clients'], 0)
        self.request('stop')
        self.thread.join(3)
        self.assertEqual(bridge.client('status', self.path)['status'], 'unavailable')

    def test_disk_failure_cannot_return_a_saved_receipt(self):
        with mock.patch.object(self.review, 'persist', side_effect=OSError('disk full')):
            with self.assertRaises(HTTPError) as error:
                self.request(choice='A')
            self.assertEqual(error.exception.code, 500)
        self.assertIsNone(self.request('status')['selection'])
        self.assertIsNone(bridge.read_state(self.path)['selection'])
        self.assertEqual(self.request(choice='A')['selection']['choice'], 'A')


if __name__ == '__main__':
    unittest.main()
