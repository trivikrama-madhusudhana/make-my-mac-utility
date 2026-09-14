#!/usr/bin/env python3
"""Package an existing Swift executable as a fresh locally signed macOS app."""
import argparse
import os
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys
import tempfile


def run(*args, cwd=None, capture=False):
    return subprocess.run(args, cwd=cwd, check=True, text=True,
                          stdout=subprocess.PIPE if capture else None).stdout


def package(args):
    if sys.platform != "darwin":
        raise ValueError("A Mac with the Swift toolchain is required to package this app.")
    for label, value in (("name", args.name), ("executable", args.executable)):
        if not value.strip() or value in (".", "..") or any(c in value for c in "/\\\0\n\r"):
            raise ValueError(f"Invalid {label}: use a single nonempty file name.")
    if not re.fullmatch(r"[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", args.bundle_id):
        raise ValueError("Use a reverse-domain bundle identifier, such as com.example.quicklog.")
    project = Path(args.project).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if not (project / "Package.swift").is_file():
        raise ValueError(f"No Package.swift in {project}")
    destination = output / f"{args.name}.app"
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"Already exists: {destination}. Choose a fresh staging output.")
    resources = Path(args.resources).expanduser().resolve() if args.resources else None
    if resources and not resources.is_dir():
        raise ValueError(f"Resources directory not found: {resources}")
    if resources and (output == resources or resources in output.parents):
        raise ValueError("The output directory must be outside the resources directory.")
    if resources and any(p.is_symlink() for p in resources.rglob("*")):
        raise ValueError("Plain resources must not contain symlinks; provide self-contained asset files.")
    run("xcrun", "--find", "swift", capture=True)
    sdk_args = ["--sdk", str(Path(args.sdk).expanduser().resolve())] if args.sdk else []
    run("xcrun", "swift", "build", "-c", "release", *sdk_args, "--product", args.executable, cwd=project)
    bin_path = Path(run("xcrun", "swift", "build", "-c", "release", *sdk_args, "--show-bin-path",
                        cwd=project, capture=True).strip())
    binary = bin_path / args.executable
    if not binary.is_file():
        raise ValueError(f"Built executable not found: {binary}")
    if list(bin_path.glob("*.bundle")):
        raise ValueError("SwiftPM resource bundles require a different resource accessor/layout. "
                         "Use an Xcode app target, or plain resources with --resources and "
                         "Bundle.main.url(forResource:withExtension:), then rebuild cleanly.")
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".utility-build-", dir=output) as temp:
        bundle = Path(temp) / destination.name
        contents = bundle / "Contents"
        (contents / "MacOS").mkdir(parents=True)
        (contents / "Resources").mkdir()
        shutil.copy2(binary, contents / "MacOS" / args.executable)
        if resources:
            shutil.copytree(resources, contents / "Resources", dirs_exist_ok=True)
        plist = {
            "CFBundleExecutable": args.executable,
            "CFBundleIdentifier": args.bundle_id,
            "CFBundleName": args.name,
            "CFBundleDisplayName": args.name,
            "CFBundlePackageType": "APPL",
            "CFBundleVersion": "1",
            "CFBundleShortVersionString": "0.1.0",
            "LSUIElement": args.mode == "companion",
            "NSHighResolutionCapable": True,
        }
        with (contents / "Info.plist").open("wb") as f:
            plistlib.dump(plist, f)
        run("codesign", "--force", "--sign", "-", str(bundle))
        run("codesign", "--verify", "--strict", str(bundle))
        # Reserve the destination to refuse even a concurrent conflicting build.
        destination.mkdir()
        try:
            os.rename(contents, destination / "Contents")
        except BaseException:
            destination.rmdir()
            raise
    try:
        run("codesign", "--verify", "--strict", str(destination))
    except subprocess.CalledProcessError as error:
        raise ValueError(f"Final bundle failed signature verification: {destination}. "
                         "Inspect extended attributes and use a fresh output outside a syncing "
                         "file-provider directory if metadata is being reattached. "
                         "The bundle is retained for inspection; do not report it as verified.") from error
    print(destination)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True)
    parser.add_argument("--executable", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--bundle-id", required=True)
    parser.add_argument("--mode", choices=("companion", "app"), required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--resources", help="Plain assets copied into Contents/Resources; use Bundle.main to read them")
    parser.add_argument("--sdk", help="Explicit installed SDK path, when preflight established an override is needed")
    args = parser.parse_args()
    try:
        package(args)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Packaging failed: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
