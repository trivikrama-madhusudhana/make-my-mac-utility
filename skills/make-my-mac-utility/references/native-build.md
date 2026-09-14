# Build the approved Mac utility

## Preflight and packaging

Inspect existing project conventions. Check macOS, `xcrun --find swift`, `xcrun swift --version`, and `xcrun --show-sdk-path`. Derive a supported deployment target from the actual SDK and required APIs. If tools are missing, explain the exact prerequisite; do not silently install a large toolchain. HTML work can be done elsewhere, but native runtime verification needs a Mac.

A reported Swift version alone does not prove the UI SDK works. A disposable compile importing AppKit and SwiftUI can reveal an incomplete default SDK. If another compatible installed SDK works, use an explicit project build override and record it; the helper accepts `--sdk PATH`. Keep global toolchain settings unchanged unless the user asks to repair them.

For a small new app, Swift Package Manager with SwiftUI views hosted by AppKit is a useful default. A normal Xcode project is fine when needed by the agreed features. Keep the main UI responsive; isolate slow I/O and provide error states. Use UserDefaults for preferences and a suitable Application Support file for user records; keep secrets in Keychain or another agreed secure credential store.

The bundled `scripts/package_app.py` packages an existing Swift executable package as a local `.app` using `swift build`, `Info.plist` and ad-hoc signing. It creates a new output bundle and refuses to overwrite one. Use a fresh staging output when rebuilding, inspect it, then replace/install only the intended app within the user's scope. It is optional for existing Xcode projects.

Example, from the generated package:

```sh
python3 /path/to/skill/scripts/package_app.py --project . --executable QuickLog --name 'Quick Log' --bundle-id com.example.quicklog --mode companion --output ./dist
```

The helper outputs a locally signed bundle, not a notarized release. A successful build/signature check is not a successful launch test. Public distribution, signing identity and notarization are a separate release concern; describe the current artifact accurately.

Verify the bundle at its delivered location too. Finder information or resource-fork extended attributes can invalidate code signing. If they keep reappearing in a file-provider-managed project folder, stop repeatedly clearing metadata: use a verified staging location and create an archive without those attributes, or choose a suitable local output location within the user's scope. Verify the extracted archive, and state any remaining location-dependent limitation. See [Apple's signing diagnosis](https://developer.apple.com/library/archive/qa/qa1940/_index.html).

For plain assets, pass `--resources ./Resources` and load them with `Bundle.main.url(forResource:withExtension:)`. Keep that directory outside the executable target. The helper rejects SwiftPM `Bundle.module` resource bundles because their generated lookup can depend on the build directory and differs from a signed app's resource layout. Use an Xcode app target when package resources, embedded frameworks, entitlements or specialized bundle configuration are required.

This small helper targets a clean single-product package. Its conservative resource check also rejects stale/unrelated `.bundle` outputs in the shared release directory; use a fresh build directory/project or an appropriate Xcode target rather than deleting user work automatically. The app output directory must be outside the plain resources directory. Supply self-contained plain assets; resource symlinks are rejected.

## Window foundations

Use SwiftUI for the selected design and AppKit for the agreed window semantics. Keep entrypoints and AppKit state on the main thread. Consult current Apple documentation when target-version behavior is uncertain.

Provide ordinary app and Edit responder commands even when the app has no Dock icon. Verify Select All, copy/paste and Quit in the packaged app; a custom panel or text field alone does not establish that these keyboard commands work.

Carry the selected light/dark behavior into both SwiftUI and embedded AppKit controls. A fixed light background with a system-dark `NSSearchField` can make typed text or placeholders unreadable. Check editable text while focused and unfocused, not only static labels. Keep primary actions discoverable to accessibility and usable from the keyboard; hover-only controls and zero-opacity buttons can disappear from the accessibility tree. Test the intended keyboard path with the current system settings rather than assuming Full Keyboard Access is enabled. Exercise both mouse and keyboard activation of actions that return to a form; check that the next typed character reaches the intended field after the view changes. If the agreement requires buttons in the Tab order, implement that path or resolve the changed requirement with the user; a handoff footnote requiring a global setting does not satisfy it. Match the agreed window chrome as well as its content; adding a native title bar to a borderless design changes the result.

For the companion starting point:

```swift
final class UtilityPanel: NSPanel {
    override var canBecomeKey: Bool { true }
    override var canBecomeMain: Bool { false }
}
// At launch:
NSApp.setActivationPolicy(.accessory)
// After creating a borderless panel:
panel.level = .normal
panel.collectionBehavior = [.transient, .ignoresCycle, .fullScreenNone]
panel.hidesOnDeactivate = false
panel.isMovableByWindowBackground = true
```

Provide a retained menu-bar status item with Show/Hide/Quit. A form needs explicit keyboard focus on invocation. Showing at login should respect the agreed focus behavior rather than stealing focus. Keep the delegate and window strongly referenced for the app's lifetime.

For the mini-app starting point, use `.regular`, an `NSWindow` with `.titled` and optional `.fullSizeContentView`, `.normal` level and `[.managed, .participatesInCycle, .fullScreenNone]`. Keep app switching and a normal Quit command. If hiding standard controls, supply clear replacements. Hiding the title text changes appearance, not the app's activation policy.

Customize these foundations to the brief; they are not assurances of identical behavior on every macOS version. Floating above other apps, appearing on all Spaces and attaching to the desktop are separate choices. Persist window position, restore it into a current screen's visible frame, and provide a recoverable default.

## Adapt to the app's responsibilities

Derive implementation and acceptance checks from the actual job. Use the relevant branches below; they are engineering concerns, not a feature menu to add to every app.

- **Invocation and focus:** for a menu, popover or shortcut, check open, dismiss, repeated invocation, focus return and an accessible way to quit. Detect shortcut conflicts and permission requirements before promising a trigger. Menu-only apps still need a discoverable first-use path.
- **Time and background work:** define what sleep, wake, restart and missed events mean. Derive elapsed time from timestamps when appropriate; a paused display timer must not silently corrupt the underlying state. Bound polling and stop work that is no longer needed.
- **Local files and other apps:** use only the agreed files or operations. Handle moved files, revoked access and partial failure. Distinguish a missing state file from an unreadable existing file: preserve unreadable data and show a recovery path instead of silently treating it as empty or overwriting it. Default to a read-only Retry. Reset/Start Fresh is a separate capability: add it only when it is in the approved scope, and require an explicit user choice before replacing unreadable data even when a backup is available. For consequential actions, provide a preview, confirmation or recovery matching the agreed experience. Treat user text as data rather than interpolating it into shell commands.
- **Remote services:** use the real documented contract, keep I/O off the UI thread, show stale/offline state, and preserve user work. Handle expired access and ambiguous write outcomes. A small interface can depend on a complex service; distinguish the local app's responsibilities from what that service already supplies.

Investigate APIs and permissions specific to an unfamiliar capability using current authoritative documentation and a bounded feasibility probe. Resolve material limitations before building the affected interface. Existing sample apps illustrate mechanics; their fields, data models and layout do not define a new app.

Recovery can fail too. Track each completed operation and each attempted restoration; do not suppress a restoration error and then report success. If recovery is incomplete, retain the remaining data and report the actual original/current locations or an equivalent actionable state. Test a secondary failure during recovery when the operation can leave user data partly changed. An attempted rollback alone does not establish all-or-nothing behavior.

Keep a failed action's pending retry separate from unrelated edits. Disable or safely queue conflicting changes while recovery is pending, and check that editing another field or losing focus cannot silently replace what Retry will do. Preserve failed input visibly until it is saved or the user explicitly abandons it.

## Verify the delivered artifact

Create an acceptance table with result and evidence for every agreed behavior. Run the packaged executable, not just a compiler or preview. Verify the main action, validation, failure recovery and persistence through quit/relaunch. For integrations, distinguish a mock from a real authorized round trip; use a harmless test record only within the user's permission.

Check the appropriate window behavior: app switching, covering with another app, Show Desktop, Mission Control, changing Spaces, show/hide/reopen/quit and keyboard focus. Check an external-display change when available; otherwise record it as unverified. Compare the native app with the selected HTML's layout and important states. Focus automated tests on data loss, retries or logic that warrants them; UI behavior needs observation.

Inspect native text and controls at the agreed window size, including realistic long content and failure messages. Protect essential labels and editable controls from compression; truncate or constrain secondary text where appropriate. Repair layout defects against the approved preview rather than changing that preview to justify the defect. Compilation cannot reveal a label wrapping into unreadable fragments.

Use available native/browser automation or direct user testing. Do not depend on a named MCP tool or claim that a process listing proves interaction. Report any unavailable check specifically. If important visual or interaction checks remain, label the result ready for user testing rather than fully validated.

## Authoritative references

- [App activation policy](https://developer.apple.com/documentation/appkit/nsapplication/activationpolicy-swift.enum)
- [NSPanel](https://developer.apple.com/documentation/appkit/nspanel)
- [Window collection behavior](https://developer.apple.com/documentation/appkit/nswindow/collectionbehavior-swift.struct)
- [WidgetKit creation and interaction limits](https://developer.apple.com/documentation/WidgetKit/Creating-a-Widget-Extension)
- [Widget lifecycle](https://developer.apple.com/documentation/widgetkit/keeping-a-widget-up-to-date)
