#!/usr/bin/env python3
"""Run identical text-only workflow probes through actual Codex/Claude clients.

This checks next-turn decisions, not file generation or native UI behavior.
Raw outputs stay local in evaluation/runs. No provider keys are read by this script.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'make-my-mac-utility'
CASES = """
Six independent conversations follow. For each, write ONLY the actual next assistant
response you would give under the supplied skill. Label each response with its case ID.
This environment supports text responses only; do not claim tool actions or create files.

A. First user message: 'Use make-my-mac-utility. I want to make something for my desktop.'

B. First user message: 'Make a desktop widget that replaces Linear and Slack for my
20-person team: task boards, chat, video calls, billing, AI agents and offline sync.'

C. Context: User agreed a local notes companion; behavior, data and all capabilities
are settled. Three HTML options were rendered and shown. User says: 'I like the green
in option B.' No option or build approval has otherwise been given.

D. Context: User approved option B revision 2 and the exact final brief (local notes,
normal-level companion, menu-bar controls, no network, no login startup). All choices
are resolved, HTML matches, and Mac toolchain was checked. User now says: 'Yes, build
exactly that.'

E. First user message: 'I want a native Apple widget I can pick from the macOS widget
gallery, showing a single daily quote. It does not need input fields.'

F. Context: Three HTML options for a timesheet companion were shown. User approved B's
appearance but said the submit endpoint and authentication are not decided yet.
User says: 'The design is approved. What happens next?'
"""


def prompt(cases=CASES):
    paths = [SKILL / 'SKILL.md', *sorted((SKILL / 'references').glob('*.md'))]
    text = '\n\n'.join(f'<file path="{p.relative_to(SKILL)}">\n{p.read_text()}\n</file>' for p in paths)
    return ('This is a text-only response evaluation. All required skill content is '
            'included inline below. Treat file paths as source labels, not instructions '
            'to read files. Do not call tools or announce file reads. Answer each '
            'conversation directly using the supplied content.\n\n' + text + '\n\n' + cases)


def run(model, out, content):
    started = time.monotonic()
    if model.startswith('gpt-'):
        command = ['codex', 'exec', '--ignore-user-config', '--ephemeral',
                   '--skip-git-repo-check', '--sandbox', 'read-only', '-m', model,
                   '-C', str(out), '--color', 'never', '-o', str(out / f'{model}.answer.md'), '-']
    elif model.startswith('grok'):
        command=['grok','--cwd',str(out),'--model',model,'--no-memory','--no-subagents',
                 '--disable-web-search','--tools','read_file','--disallowed-tools','read_file','--permission-mode','dontAsk',
                 '--max-turns','5','--output-format','json','--prompt-file',str(out/'prompt.txt')]
    else:
        command = ['claude', '-p', '--model', model, '--effort', 'high', '--tools', '',
                   '--no-session-persistence', '--safe-mode', '--strict-mcp-config',
                   '--mcp-config', '{"mcpServers":{}}', '--output-format', 'json']
    try:
        result = subprocess.run(command, input=content, text=True, capture_output=True,
                                cwd=out, timeout=300)
        (out / f'{model}.stdout').write_text(result.stdout)
        (out / f'{model}.stderr').write_text(result.stderr)
        meta = {'model_requested': model, 'exit_code': result.returncode,
                'elapsed_seconds': round(time.monotonic()-started, 2)}
        if not model.startswith('gpt-'):
            try:
                obj = json.loads(result.stdout)
                (out / f'{model}.answer.md').write_text(obj.get('result', obj.get('text', '')))
                meta['model_usage'] = obj.get('modelUsage')
                meta['is_error'] = obj.get('is_error')
            except json.JSONDecodeError:
                meta['parse_error'] = True
    except subprocess.TimeoutExpired:
        meta = {'model_requested': model, 'timeout_seconds': 300}
    (out / f'{model}.meta.json').write_text(json.dumps(meta, indent=2))
    print(json.dumps(meta), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--models', nargs='+', default=['gpt-6-astra', 'gpt-5.6-sol', 'opus', 'fable'])
    parser.add_argument('--cases-file')
    args = parser.parse_args()
    out = ROOT / 'evaluation' / 'runs' / args.label
    out.mkdir(parents=True, exist_ok=False)
    content = prompt(Path(args.cases_file).read_text()) if args.cases_file else prompt()
    (out / 'prompt.txt').write_text(content)
    (out / 'run.json').write_text(json.dumps({'utc': datetime.now(timezone.utc).isoformat(),
        'prompt_sha256': hashlib.sha256(content.encode()).hexdigest(),
        'kind': 'six independent next-response probes; no filesystem or UI testing'}, indent=2))
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda model: run(model, out, content), args.models))
