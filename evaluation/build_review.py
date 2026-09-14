#!/usr/bin/env python3
"""Preserve immutable preview versions and rebuild the offline review index."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import html
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / 'review'
MODELS = [
    ('codex-astra', 'Codex CLI', 'Astra · gpt-6-astra', 'artifacts-gpt-6-astra-r1'),
    ('codex-sol', 'Codex CLI', 'Sol · gpt-5.6-sol', 'artifacts-gpt-5.6-sol-r1'),
    ('claude-opus', 'Claude Code CLI', 'Opus · claude-opus-5', 'artifacts-opus-r2'),
    ('claude-fable', 'Claude Code CLI', 'Fable · claude-fable-5-1', 'artifacts-fable-r1'),
    ('grok-build', 'Grok Build CLI', 'Grok · grok-4.6-build', 'artifacts-grok-r1'),
]

def main():
    REVIEW.mkdir(exist_ok=True)
    manifest_path = REVIEW / 'manifest.json'
    entries = json.loads(manifest_path.read_text()) if manifest_path.exists() else []
    for key, agent, model, run in MODELS:
        source = ROOT / 'evaluation/runs' / run / 'design/options.html'
        if not source.exists():
            continue
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        previous = [e for e in entries if e['client_model'] == key]
        if not any(e['sha256'] == digest for e in previous):
            stage = 'initial' if not previous else f'revision-{len(previous)+1}'
            relative = f'{key}/{stage}.html'
            destination = REVIEW / relative
            destination.parent.mkdir(exist_ok=True)
            if destination.exists():
                raise RuntimeError(f'Refusing to replace snapshot: {destination}')
            shutil.copyfile(source, destination)
            entries.append({'client_model':key, 'iteration':stage, 'file':relative,
                'source':str(source.relative_to(ROOT)), 'sha256':digest,
                'preserved_utc':datetime.now(timezone.utc).isoformat()})
    for e in entries:
        if hashlib.sha256((REVIEW / e['file']).read_bytes()).hexdigest() != e['sha256']:
            raise RuntimeError(f'Snapshot changed: {e["file"]}')
    manifest_path.write_text(json.dumps(entries, indent=2) + '\n')
    rows=[]
    for key, agent, model, run in MODELS:
        versions=[e for e in entries if e['client_model']==key]
        links=' '.join(f'<a href="{html.escape(e["file"])}" target="_blank" rel="noopener">{html.escape(e["iteration"].replace("-"," "))} ↗</a>' for e in versions) or 'No preview completed'
        rows.append(f'<tr><td>{html.escape(agent)}</td><td>{html.escape(model)}</td><td>{links}</td></tr>')
    options=[]
    for key, agent, model, run in MODELS:
        for e in entries:
            if e['client_model']==key:
                options.append(f'<option value="{html.escape(e["file"])}">{html.escape(agent+" / "+model+" / "+e["iteration"])}</option>')
    page='''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mac Utility Skill · Sprint Review</title>
<style>
:root{color-scheme:light;font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#242a30;background:#f5f4ef}
*{box-sizing:border-box}body{margin:0}header,main{max-width:1440px;margin:auto;padding:28px 32px}header{padding-bottom:10px}.eyebrow{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:#5b625f}h1{font-size:clamp(26px,4vw,42px);letter-spacing:-.04em;margin:6px 0 12px}p{max-width:850px;color:#59605e}a{color:#1b595c;text-underline-offset:3px}table{width:100%;border-collapse:collapse;background:#fff;border-radius:10px;overflow:hidden}th,td{text-align:left;padding:12px 16px;border-bottom:1px solid #e6e8e2}th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:#636b66}td a{display:inline-block;margin-right:14px}.table-wrap{overflow-x:auto}.toolbar{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:28px 0 12px}label{font-weight:600}select,button{font:inherit;padding:10px 12px;border:1px solid #b8c2ba;border-radius:8px;background:#fff}select{max-width:100%}button{cursor:pointer}button:hover{background:#e9eeea}:focus-visible{outline:3px solid #397c87;outline-offset:3px}.viewers{display:grid;grid-template-columns:1fr;gap:16px}.viewers.compare{grid-template-columns:1fr 1fr}.viewer{min-width:0}.viewer-bar{display:flex;justify-content:space-between;gap:10px;align-items:center;margin-bottom:8px}.viewer-bar select{min-width:0;width:100%}.viewer-bar a{white-space:nowrap;flex-shrink:0}iframe{width:100%;height:950px;border:1px solid #bac3bb;border-radius:10px;background:white}.note{font-size:13px}footer{padding:20px 0;color:#66716a;font-size:13px}[hidden]{display:none!important}@media(max-width:900px){.viewers.compare{grid-template-columns:1fr}header,main{padding:20px 16px}iframe{height:800px}}
</style>
<header><div class="eyebrow">Make My Mac Utility · Evaluation archive</div><h1>Five models. Fifteen original designs.</h1><p>Every model received the same fictional Pocket Notes brief: capture, search, timestamps, delete and undo. These are the actual consultation interfaces they produced. Original snapshots stay intact; revisions appear separately.</p><p class="note">Preview controls change demo state only. Selecting a design here does not approve a native build. Codex Desktop was used to inspect the interfaces; it was a surface check, not a sixth independent model run.</p></header>
<main><div class="table-wrap"><table><thead><tr><th>Coding agent</th><th>Model</th><th>Preserved interfaces</th></tr></thead><tbody>ROWS</tbody></table></div>
<div class="toolbar"><label for="left-choice">Review an interface</label><button id="compare" type="button" aria-pressed="false">Compare two</button><span class="note">Open a full page to see the designs at their intended sizes.</span></div>
<div id="viewers" class="viewers"><section class="viewer"><div class="viewer-bar"><select id="left-choice" aria-label="First model and iteration">OPTIONS</select><a id="left-open" target="_blank" rel="noopener">Open ↗</a></div><iframe id="left-frame" title="First preserved consultation interface" sandbox="allow-scripts"></iframe></section>
<section class="viewer" id="right-viewer" hidden><div class="viewer-bar"><select id="right-choice" aria-label="Second model and iteration">OPTIONS</select><a id="right-open" target="_blank" rel="noopener">Open ↗</a></div><iframe id="right-frame" title="Second preserved consultation interface" sandbox="allow-scripts"></iframe></section></div>
<footer>Preserved locally for sprint review. <a href="../evaluation/README.md">Evaluation report</a> · <a href="manifest.json">Snapshot hashes</a></footer></main>
<script>
function show(side){const value=document.getElementById(side+'-choice').value;document.getElementById(side+'-frame').src=value;document.getElementById(side+'-open').href=value;}
for(const side of ['left','right'])document.getElementById(side+'-choice').addEventListener('change',()=>show(side));
document.getElementById('right-choice').selectedIndex=Math.min(1,document.getElementById('right-choice').options.length-1);show('left');show('right');
document.getElementById('compare').onclick=()=>{const button=document.getElementById('compare'),on=button.getAttribute('aria-pressed')!=='true';button.setAttribute('aria-pressed',String(on));button.textContent=on?'Single view':'Compare two';document.getElementById('right-viewer').hidden=!on;document.getElementById('viewers').classList.toggle('compare',on);};
</script></html>'''.replace('ROWS',''.join(rows)).replace('OPTIONS',''.join(options))
    (REVIEW/'index.html').write_text(page)
    print(f'Preserved {len(entries)} immutable snapshots across {len(MODELS)} models: {REVIEW / "index.html"}')

if __name__=='__main__':main()
