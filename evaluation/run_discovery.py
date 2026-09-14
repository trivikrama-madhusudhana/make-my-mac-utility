#!/usr/bin/env python3
"""Smoke test installed skill discovery without including the skill's path or text."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse, json, subprocess, time
root=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--client',choices=['codex','claude','both'],default='both')
ap.add_argument('--label',default='discovery')
args=ap.parse_args()
def run(client):
 out=root/'evaluation/runs'/(args.label+'-'+client)
 out.mkdir(exist_ok=False)
 prompt='Use make-my-mac-utility. I want to make something for my Mac desktop. What do we decide first? This is a consultation only; do not create implementation files.'
 if client=='codex':
  cmd=['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','--sandbox','read-only','-m','gpt-5.6-sol','-C',str(out),'--json','-o',str(out/'answer.md'),'-']
 else:
  cmd=['claude','-p','--model','fable','--effort','low','--no-session-persistence','--setting-sources','user','--settings','{"disableAllHooks":true}','--strict-mcp-config','--mcp-config','{"mcpServers":{}}','--tools','Read,Glob,Grep,Skill','--allowedTools','Read,Glob,Grep,Skill','--verbose','--output-format','stream-json']
 start=time.monotonic()
 with (out/'stdout').open('w') as stdout,(out/'stderr').open('w') as stderr:
  try:
   r=subprocess.run(cmd,input=prompt,text=True,stdout=stdout,stderr=stderr,cwd=out,timeout=300)
   meta={'client':client,'exit_code':r.returncode,'elapsed_seconds':round(time.monotonic()-start,2)}
  except subprocess.TimeoutExpired:meta={'client':client,'timeout_seconds':300}
 (out/'meta.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta),flush=True)
clients=['codex','claude'] if args.client=='both' else [args.client]
with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,clients))
