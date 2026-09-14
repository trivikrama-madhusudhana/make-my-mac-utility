#!/usr/bin/env python3
"""Archive a fixture app without xattrs, then verify a fresh extracted copy."""
import argparse
import json
from pathlib import Path
import stat
import subprocess
import tempfile
import zipfile

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('app',type=Path)
ap.add_argument('--label',required=True)
args=ap.parse_args()
app=args.app.resolve()
if not app.is_dir() or app.suffix!='.app':raise SystemExit('Expected an existing .app directory')
if not args.label.replace('-','').isalnum():raise SystemExit('Use an alphanumeric archive label')
archive=app.parent/f'{app.stem}-{args.label}.zip'
if archive.exists():raise SystemExit(f'Archive already exists: {archive}')
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(app.rglob('*')):
        if p.is_symlink():raise SystemExit('This fixture archive helper expects no symlinks')
        if p.is_file():z.write(p,p.relative_to(app.parent))
with tempfile.TemporaryDirectory(prefix='utility-archive-verify-') as folder:
    with zipfile.ZipFile(archive) as z:
        z.extractall(folder)
        for info in z.infolist():
            mode=stat.S_IMODE(info.external_attr>>16)
            if mode:(Path(folder)/info.filename).chmod(mode)
    result=subprocess.run(['codesign','--verify','--strict',str(Path(folder)/app.name)],capture_output=True,text=True)
    report={'archive':str(archive),'fresh_extraction_strict_codesign_exit':result.returncode,
            'diagnostic':result.stderr.strip(),'method':'ZIP stores file contents and Unix mode; extended attributes are not copied. Verified temporary extraction outside the synced project.'}
    archive.with_suffix('.verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
    if result.returncode:raise SystemExit(result.returncode)
