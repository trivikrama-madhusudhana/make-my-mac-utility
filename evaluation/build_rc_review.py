#!/usr/bin/env python3
"""Archive fresh four-model consultations without overwriting previous versions."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import html
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'review' / 'release-candidate'
MODELS = [('astra', 'Codex · Astra', 'Steep'), ('opus', 'Claude Code · Opus', 'Steep'),
          ('sol', 'Codex · Sol', 'Frame Names'), ('fable', 'Claude Code · Fable', 'Frame Names')]


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    manifest = DEST / 'manifest.json'
    entries = json.loads(manifest.read_text()) if manifest.exists() else []
    for key, agent, job in MODELS:
        source = ROOT / 'evaluation' / 'runs' / f'rc1-{key}' / 'design' / 'options.html'
        if not source.is_file():
            continue
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        old = [e for e in entries if e['model'] == key]
        if any(e['sha256'] == digest for e in old):
            continue
        version = len(old) + 1
        relative = f'{key}/v{version}.html'
        target = DEST / relative
        target.parent.mkdir(exist_ok=True)
        if target.exists():
            raise RuntimeError(f'Snapshot already exists: {target}')
        shutil.copyfile(source, target)
        entries.append(dict(model=key, agent=agent, job=job, version=version,
                            file=relative, sha256=digest, source=str(source.relative_to(ROOT)),
                            preserved_utc=datetime.now(timezone.utc).isoformat()))
    for e in entries:
        assert hashlib.sha256((DEST / e['file']).read_bytes()).hexdigest() == e['sha256'], e['file']
    manifest.write_text(json.dumps(entries, indent=2) + '\n')
    rows = []
    options = []
    for key, agent, job in MODELS:
        versions = sorted([e for e in entries if e['model'] == key], key=lambda e: e.get('display_order', e['version']))
        links = ' · '.join(f'<a href="{e["file"]}" target="_blank">{html.escape(e.get("label", "Version " + str(e["version"])))}</a>' for e in versions)
        rows.append(f'<tr><td>{html.escape(agent)}</td><td>{html.escape(job)}</td><td>{links or "Pending"}</td></tr>')
        for e in versions:
            label = f'{agent} / {job} / {e.get("label", "version " + str(e["version"]))}'
            options.append(f'<option value="{e["file"]}">{html.escape(label)}</option>')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Four-model release review</title>
<style>*{box-sizing:border-box}body{margin:0;background:#f4f1eb;color:#242725;font:16px/1.5 system-ui}main{max-width:1600px;margin:auto;padding:32px}h1{letter-spacing:-.04em;font-size:40px;margin:12px 0}p{max-width:850px;color:#535b57}a{color:#17605e}table{border-collapse:collapse;width:100%;background:white}td,th{padding:14px;text-align:left;border-bottom:1px solid #ddd}select,button{font:inherit;padding:10px;background:white;border:1px solid #aaa;border-radius:6px}button{cursor:pointer}.controls{display:flex;gap:14px;align-items:center;margin:28px 0 12px;flex-wrap:wrap}.views{display:grid;grid-template-columns:1fr;gap:16px}.views.compare{grid-template-columns:1fr 1fr}.pane{min-width:0}.bar{display:flex;gap:12px;margin-bottom:8px;align-items:center}.bar select{min-width:0;flex:1}iframe{width:100%;height:960px;border:1px solid #bbb;background:white;border-radius:8px}:focus-visible{outline:3px solid #087d77;outline-offset:3px}[hidden]{display:none!important}@media(max-width:900px){main{padding:16px}.views.compare{grid-template-columns:1fr}h1{font-size:30px}}</style>
<main><a href="../index.html">Original sprint archive</a><h1>Four models. Two fresh jobs.</h1>
<p>These are the actual interfaces generated after consultations for Steep and Frame Names. Each version preserves the model's three design options. Compare their judgment, usability and visual character; this gallery does not grant build approval. Check statements inside each preview belong to its generation run; independent results are linked below.</p>
<table><thead><tr><th>Agent and model</th><th>App</th><th>Preserved versions</th></tr></thead><tbody>ROWS</tbody></table>
<div class="controls"><button id="compare" aria-pressed="false">Compare two</button><span>Open a version in its own tab to see the full layout.</span></div>
<div class="views" id="views"><section class="pane"><div class="bar"><select id="left" aria-label="First interface">OPTIONS</select><a id="left-link" target="_blank">Open ↗</a></div><iframe id="left-frame" title="First consultation" sandbox="allow-scripts"></iframe></section>
<section class="pane" id="second" hidden><div class="bar"><select id="right" aria-label="Second interface">OPTIONS</select><a id="right-link" target="_blank">Open ↗</a></div><iframe id="right-frame" title="Second consultation" sandbox="allow-scripts"></iframe></section></div>
<p><a href="../../evaluation/RELEASE-CANDIDATE-RESULTS.md">Results and repairs</a> · <a href="../../evaluation/RELEASE-CANDIDATE-PLAN.md">Evaluation contract</a> · <a href="manifest.json">Snapshot hashes</a></p></main>
<script>function show(side){let value=document.getElementById(side).value;if(!value)return;document.getElementById(side+'-frame').src=value;document.getElementById(side+'-link').href=value}for(let side of ['left','right'])document.getElementById(side).onchange=()=>show(side);let right=document.getElementById('right');let choices=Array.from(right.options);let final=choices.findIndex(o=>o.textContent.includes('Opus')&&o.textContent.includes('final'));right.selectedIndex=Math.max(0,final>=0?final:choices.findIndex(o=>o.textContent.includes('Opus')&&o.textContent.includes('approved')));show('left');show('right');document.getElementById('compare').onclick=function(){let on=this.getAttribute('aria-pressed')!=='true';this.setAttribute('aria-pressed',String(on));this.textContent=on?'Single view':'Compare two';document.getElementById('views').classList.toggle('compare',on);document.getElementById('second').hidden=!on};</script></html>'''
    (DEST / 'index.html').write_text(page.replace('ROWS', ''.join(rows)).replace('OPTIONS', ''.join(options)))
    print(f'Preserved {len(entries)} versions: {DEST / "index.html"}')


if __name__ == '__main__':
    main()
