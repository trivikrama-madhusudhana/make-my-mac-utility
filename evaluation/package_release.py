#!/usr/bin/env python3
"""Build portable release archives from an explicit public-file allowlist."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'


def files_below(folder):
    for path in sorted(folder.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Unexpected symlink: {path}')
        if path.is_file() and path.name != '.DS_Store' and '__pycache__' not in path.parts:
            yield path


def archive(name, files, prefix):
    target = DIST / name
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in sorted(set(files)):
            relative = path.relative_to(ROOT)
            assert 'runs' not in relative.parts and 'screenshots' not in relative.parts
            z.write(path, str(Path(prefix) / relative))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
    return dict(file=target.name, sha256=hashlib.sha256(target.read_bytes()).hexdigest(), bytes=target.stat().st_size)


def main():
    DIST.mkdir(exist_ok=True)
    skill = list(files_below(ROOT / 'skills'))
    public = [ROOT / name for name in ['README.md', 'LICENSE', '.gitignore']]
    public += skill + list(files_below(ROOT / 'review')) + list(files_below(ROOT / 'examples'))
    public += [p for p in (ROOT / 'evaluation').iterdir()
               if p.is_file() and p.suffix in {'.md', '.txt', '.py', '.cjs', '.sha256'}]
    public.append(ROOT / 'evaluation' / 'rc-prompts' / 'FACTS.md')
    records = [archive('make-my-mac-utility-release.zip', public, 'make-my-mac-utility')]
    # The install archive extracts directly to a skill folder.
    target = DIST / 'make-my-mac-utility-skill.zip'
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in skill:
            z.write(p, str(p.relative_to(ROOT / 'skills')))
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
    records.append(dict(file=target.name, sha256=hashlib.sha256(target.read_bytes()).hexdigest(), bytes=target.stat().st_size))
    (DIST / 'release-manifest.json').write_text(json.dumps(records, indent=2) + '\n')
    print(json.dumps(records, indent=2))


if __name__ == '__main__':
    main()
