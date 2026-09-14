#!/usr/bin/env python3
"""Execute a fixture prompt with real coding tools in an isolated directory."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'make-my-mac-utility'
DESIGN = """Use the make-my-mac-utility skill at ./skill/SKILL.md.

Build consultation for a fictional personal app called Pocket Notes. I want a
quiet desktop companion for capturing a short note and finding a saved one.
The agreed first version has exactly these capabilities: one note input, Save,
a searchable saved-note list with timestamps, and Delete with an undo opportunity.
Everything is local on this Mac in a JSON file under the app's Application Support
directory. No accounts, sync, network, markdown editor, tags or AI. Use fictional
example notes in the preview. Preserve text on a failed save and show the error.

Behavior agreed: accessory app, no Dock icon, normal window level (covered by other
apps), current Space, menu-bar Show/Hide/Quit, remember a reachable position, no
login startup. Show focuses the note field. Keep keyboard use straightforward.
I delegate minor implementation and accessibility choices. I like calm readable
designs but don't have a preferred layout, size or color; recommend those visually.
The success test is save a note, search it, delete and undo, then quit/reopen and
find it still there. The Mac toolchain is available; inspect it if needed.

Please show me the three HTML options first; I will choose after seeing them.

Evaluation environment: this is a disposable fixture, not production data. Work
only in this current directory, with reads of the bundled skill and toolchain.
No other skills, subagents, network calls, publication, installations or startup
changes. You may use shell/file tools. Browser automation is not exposed to this
CLI run, so provide the HTML path for me to open and inspect. Do not open GUI apps
from this headless run. Be honest about which visual checks you could perform.
"""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model',required=True)
    ap.add_argument('--label',required=True)
    ap.add_argument('--prompt-file')
    ap.add_argument('--existing',action='store_true')
    ap.add_argument('--stage')
    ap.add_argument('--timeout',type=int,default=1800)
    ap.add_argument('--effort',choices=['low','medium','high'],default='high')
    ap.add_argument('--logs-outside',action='store_true',help='Keep evaluator streams out of the generated project')
    args=ap.parse_args()
    out=ROOT/'evaluation'/'runs'/args.label
    if not args.existing:
        out.mkdir(parents=True,exist_ok=False)
        shutil.copytree(SKILL,out/'skill')
    content=Path(args.prompt_file).read_text() if args.prompt_file else DESIGN
    stage=args.stage or ('build' if args.existing else 'design')
    logs=ROOT/'evaluation'/'runs'/'_logs'/args.label if args.logs_outside else out
    logs.mkdir(parents=True,exist_ok=True)
    (out/f'{stage}-prompt.txt').write_text(content)
    if args.model.startswith('gpt-'):
        cmd=['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check',
             '--sandbox','workspace-write','-m',args.model,'-C',str(out),'--color','never',
             '--json','-o',str(out/f'{stage}-answer.md'),'-']
    elif args.model.startswith('grok'):
        cmd=['grok','--cwd',str(out),'--model',args.model,'--no-memory','--no-subagents',
             '--disable-web-search','--permission-mode','acceptEdits',
             '--tools','read_file,list_dir,grep,search_replace,run_terminal_cmd',
             '--allow','Bash(*)','--max-turns','60','--output-format','json',
             '--prompt-file',str(out/f'{stage}-prompt.txt')]
    else:
        cmd=['claude','-p','--model',args.model,'--effort',args.effort,
             '--no-session-persistence','--safe-mode','--strict-mcp-config',
             '--mcp-config','{"mcpServers":{}}','--tools','Read,Write,Edit,Bash,Glob,Grep',
             '--allowedTools','Read,Write,Edit,Bash,Glob,Grep','--permission-mode','acceptEdits',
             '--verbose','--output-format','stream-json']
    skill_hashes={str(p.relative_to(out/'skill')):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((out/'skill').rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
    started=time.monotonic()
    try:
        with (logs/f'{stage}.stdout').open('w') as stdout, (logs/f'{stage}.stderr').open('w') as stderr:
            result=subprocess.run(cmd,input=content,text=True,stdout=stdout,stderr=stderr,cwd=out,timeout=args.timeout)
        meta={'model_requested':args.model,'exit_code':result.returncode,
              'elapsed_seconds':round(time.monotonic()-started,2),
              'prompt_sha256':hashlib.sha256(content.encode()).hexdigest()}
        if not args.model.startswith('gpt-'):
            try:
                raw=(logs/f'{stage}.stdout').read_text()
                if args.model.startswith('grok'):
                    obj=json.loads(raw)
                else:
                    events=[json.loads(line) for line in raw.splitlines() if line.startswith('{')]
                    obj=next((event for event in reversed(events) if event.get('type')=='result'),{})
                (out/f'{stage}-answer.md').write_text(obj.get('result',obj.get('text','')))
                meta['model_usage']=obj.get('modelUsage')
                meta['is_error']=obj.get('is_error')
                meta['permission_denials']=obj.get('permission_denials')
            except json.JSONDecodeError:meta['parse_error']=True
    except subprocess.TimeoutExpired as err:
        meta={'model_requested':args.model,'timeout_seconds':args.timeout}
    meta.update({'skill_sha256':skill_hashes,'reasoning_effort':args.effort if not args.model.startswith(('gpt-', 'grok')) else 'client default','timeout_limit_seconds':args.timeout})
    meta['log_directory']=str(logs.relative_to(ROOT))
    (out/f'{stage}-meta.json').write_text(json.dumps(meta,indent=2))
    print(json.dumps(meta),flush=True)

if __name__=='__main__':main()
