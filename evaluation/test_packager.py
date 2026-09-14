"""Real SwiftPM resource packaging regression; no GUI app or installation."""
import importlib.util
import os
from pathlib import Path
import plistlib
import subprocess
import tempfile
import unittest
from argparse import Namespace

HELPER = Path(__file__).resolve().parents[1] / 'skills/make-my-mac-utility/scripts/package_app.py'
spec=importlib.util.spec_from_file_location('packager',HELPER)
packager=importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class Packaging(unittest.TestCase):
    def test_plain_resources_survive_move_and_missing_build_tree(self):
        with tempfile.TemporaryDirectory(prefix='utility-resource-eval-') as folder:
            root=Path(folder)
            project=root/'project with spaces'
            source=project/'Sources/ResourceProbe'
            source.mkdir(parents=True)
            (project/'Package.swift').write_text('''// swift-tools-version: 5.9
import PackageDescription
let package = Package(name: "ResourceProbe", platforms: [.macOS(.v13)],
 products: [.executable(name: "ResourceProbe", targets: ["ResourceProbe"])],
 targets: [.executableTarget(name: "ResourceProbe")])
''')
            (source/'main.swift').write_text('''import Foundation
let url = Bundle.main.url(forResource: "sample", withExtension: "txt")!
print(try String(contentsOf: url, encoding: .utf8))
''')
            resources=project/'Resources'
            resources.mkdir()
            (resources/'sample.txt').write_text('RESOURCE_OK_314159')
            args=Namespace(project=str(project),output=str(root/'staging'),name='Resource Probe',
                           executable='ResourceProbe',bundle_id='com.example.resourceprobe',mode='companion',resources=str(resources),sdk=None)
            bundle=packager.package(args)
            info=plistlib.loads((bundle/'Contents/Info.plist').read_bytes())
            self.assertTrue(info['LSUIElement'])
            # Remove SwiftPM's development-location fallback without deleting source.
            os.rename(project/'.build',project/'.build-hidden')
            moved=root/'Moved Resource Probe.app'
            os.rename(bundle,moved)
            result=subprocess.run([str(moved/'Contents/MacOS/ResourceProbe')],
                                  capture_output=True,text=True,check=True)
            self.assertEqual(result.stdout.strip(),'RESOURCE_OK_314159')
            subprocess.run(['codesign','--verify','--strict',str(moved)],check=True)
            # Existing user content must survive an attempted rebuild.
            args.name='Moved Resource Probe';args.output=str(root)
            before=(moved/'Contents/Info.plist').read_bytes()
            with self.assertRaisesRegex(ValueError,'Already exists'):
                packager.package(args)
            self.assertEqual((moved/'Contents/Info.plist').read_bytes(),before)

    def test_path_traversal_rejected_before_build(self):
        args=Namespace(project='/does/not/exist',output='/tmp',name='../escape',
                       executable='Probe',bundle_id='com.example.probe',mode='app',resources=None,sdk=None)
        with self.assertRaisesRegex(ValueError,'Invalid name'):
            packager.package(args)

    def test_recursive_resource_copy_rejected_before_build(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'Package.swift').write_text('// fixture: should never be built')
            for out in (root,root/'dist'):
                args=Namespace(project=str(root),output=str(out),name='Probe',
                    executable='Probe',bundle_id='com.example.probe',mode='app',resources=str(root),sdk=None)
                with self.assertRaisesRegex(ValueError,'outside the resources'):
                    packager.package(args)

    def test_resource_symlink_cannot_reenter_output(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            (root/'Package.swift').write_text('// fixture: should never be built')
            assets=root/'assets'; assets.mkdir()
            output=root/'dist'; output.mkdir()
            (assets/'loop').symlink_to(output, target_is_directory=True)
            args=Namespace(project=str(root),output=str(output),name='Probe',
                executable='Probe',bundle_id='com.example.probe',mode='app',resources=str(assets),sdk=None)
            with self.assertRaisesRegex(ValueError,'symlinks'):
                packager.package(args)


if __name__=='__main__':unittest.main()
