# September 14 publish validation

**Verdict: ready for an initial public beta of the skill.** The new browser-choice handoff works in an active Codex session, the fresh native fixture passes the repaired paths exercised on this Mac, and the portable release includes the helper, its UI, instructions, tests, and license. This is not a guarantee of defect-free generated apps or all-Mac compatibility. Publication itself has not been performed.

## What changed

- Added a Python standard-library review server with **Choose A, Choose B, Choose C, and None of these**, plus optional feedback. A deliberate browser click returns a revision-bound selection to the waiting agent tool call. No external webhook, account, proprietary connector, or Impeccable installation is required.
- Updated the workflow to consume browser receipts as design choices. None requests revised options. A choice does not grant blanket build approval; existing explicit authorization is honored without asking twice.
- Moved unreadable-data recovery into consultation and preview preparation, after a fresh preview omitted that screen until review.
- Added native guidance for ordinary app/Edit commands and for protecting a pending Retry from unrelated edits, based on reproduced native defects.
- Included the existing MIT license in the installable skill folder, so the standalone skill archive carries the notice too.

The implementation uses the general localhost event/wait pattern inspected in Impeccable. Its source was independently implemented for this smaller workflow; Impeccable code is not bundled.

## Fresh native build and repair

A fresh Codex subagent received a fictional everyday knitting problem without earlier findings or the evaluator's test plan. Consultation established one named project, completed-row count, +1, one-step undo, confirmed reset, local persistence, a covered-by-other-windows accessory panel, and no login startup. Three HTML designs were produced. The evaluator selected A Cozy card at 300 × 440 after browser inspection. A second preview revision added unreadable-data recovery; the evaluator inspected it and explicitly approved the disposable build.

The [preserved gallery](../review/publish-validation/index.html) contains both actual generated preview revisions. They remain historical snapshots, including their original verification-status text.

All three original previews were observed incrementing, undoing, retaining count during simulated save failure, retrying once after recovery, and rendering long names with a 1,234-row count. They stacked and remained usable at a 620 × 800 browser viewport. A's confirmed reset and reset undo passed. All three revised previews blocked mutation while data was unreadable, remained blocked after failed Retry, and recovered the saved project after restoring readable data.

The generating agent built a native SwiftUI host with AppKit controls. The evaluator operated the actual packaged app. Initial GUI checks passed counting, undo, reset cancellation/confirmation/undo, keyboard primary action, failed-write retention, malformed-data blocking, and read-only recovery. Two defects required native repair:

1. **Ordinary keyboard commands were absent.** Cmd+A inserted at the cursor instead of selecting all; Cmd+Q did not quit. The repair added standard app/Edit responder commands. In the repaired packaged app, Cmd+A replaced the complete project name, paste visibly entered the supplied text, Cmd+Q ended the process, and an actual menu Quit also ended the process.
2. **An unrelated name edit could replace a failed increment's pending retry.** A real directory-permission failure left the count unchanged, but editing the still-enabled name field replaced the pending action. After access was restored, Retry saved only the name. The repair guards pending operations in the core and disables conflicting UI edits. The evaluator reproduced the fault conditions: the name field was disabled, saved bytes stayed unchanged, and Retry committed the original increment exactly once. A separate failed-name test preserved the draft onscreen; Tab and Space on Retry saved it after permissions were restored.

The final app restored the exact saved name/count after Quit and relaunch. With its saved file made unreadable through actual filesystem permissions, the final app exposed only read recovery; unsuccessful Retry preserved the exact bytes. Restoring the original permissions and retrying recovered the expected project without rewriting its data.

An independent static review found no actionable core defect, and identified the UI's responsibility for protecting pending intent; the subsequent GUI test exercised that boundary. The initial executable test runner passed 40 assertions. After the repair, **49 assertions passed**, including pending-operation regressions. These assertions are generated-app checks, not 49 independent skill tasks.

## Browser-to-agent handoff

**12 integration tests pass** in `evaluation/test_design_review.py`. They cover active wait delivery, durable replay after stop, offline source revalidation, duplicate/conflicting submissions, None with empty or nonempty feedback, source invalidation, token/Host/Origin checks, request/path bounds, preview sandbox policy, private state, existing-file preservation, bounded timeout, cleanup, and failed persistence without a false receipt.

Two additional tests used the real browser and a separately running yielded wait command:

| Browser action | Observed agent-tool result |
| --- | --- |
| Click None of these, with no feedback | Immediate structured None receipt, matching review and source hashes, `build_authorized: false` |
| Enter feedback, then click Choose A | Immediate A receipt containing the exact feedback, matching review and source hashes, `build_authorized: false` |

Both submissions were deliberately labeled disposable tests. They are evaluation evidence, not approval from the conversation user. One browser inspection found that the choice buttons fell below a typical laptop viewport; the final layout moves buttons and receipt ahead of optional feedback and bounds preview height. A second inspection confirmed visible choice buttons and receipt at 1470 × 745.

The wrapper isolates generated preview scripts from its selection token. It saves before acknowledging, binds a round to the exact HTML and brief, rejects stale/conflicting choices, and retains receipts for replay. It serves only its wrapper and named preview snapshot on loopback. Private review files and token-bearing URLs are excluded from the public package.

**A waiting session is required for automatic continuation.** The helper does not restart a finished session. In Codex, a yielded execution call delivered the event in these tests. The Claude Code background-notification route is documented using the same plain CLI, but was not separately exercised in this follow-up. Manual chat selection remains available when localhost or persistent execution is unavailable.

## Response and package checks

Ten identical scenario prompts were given to separate fresh agents, one reading the frozen skill and one without skill content. Both handled most cases sensibly. The with-skill responses met all ten reviewed criteria. In the unresolved-sharing/design case, the baseline proposed starting UI/logging work, while the skill response held implementation until the material decision was settled. This is a small, non-repeated response comparison with evaluator-visible conditions, not proof of a general performance gain or a reliability percentage.

A fresh sketch-reference scenario picked up the added pre-design read-recovery guidance without being prompted about read failure. Five final response probes correctly described active browser waits, None handling, stale-choice rejection, native command/pending-operation repairs, and the inability to wake an ended session. Text responses do not prove native behavior; the separate execution evidence above does.

The existing app-packaging helper's **four regression tests passed**: plain assets survived moving the app after hiding the build tree, existing destinations were preserved, and traversal/recursive-resource/symlink inputs were rejected. Skill metadata validation passed. Final archive hashes, clean extraction, local links, and public-file checks are recorded in the local audit evidence. Both installed client paths link to the same updated skill source.

## Environment and evidence limits

Host: macOS 26.5.1, Apple silicon, Apple Swift 5.10 Command Line Tools. The default SDK lacks required UI headers; an explicit installed macOS 13.3 SDK was used without changing global settings. XCTest is unavailable in this installation, so the native tests ran through an executable assertion runner. Build and local ad-hoc signature verification passed. No notarized public app binary is claimed.

This follow-up adds one new native job. The earlier [four-model release evaluation](RELEASE-CANDIDATE-RESULTS.md) remains relevant historical evidence; it is not relabeled as generation from today's final text. Later shortcut/retry guidance was derived from observed repairs and checked with final response probes. The new bridge was tested separately with real browser interaction and deterministic integration tests. There was no fresh four-model end-to-end generation round after all final edits.

No external Mac, Intel Mac, older macOS runtime, external-display change, full Spaces/Show Desktop/Mission Control matrix, VoiceOver session, or real sleep/wake test was available or established. Status-item Show/Hide interaction was not established in this follow-up; the SystemUIServer accessibility request timed out. Normal app quit/relaunch was observed. These are explicit coverage limits, not passing results inferred from compilation.

One intervening user interaction changed the fixture count; the baseline was refreshed before the scored repaired tests. A screen-capture interruption and a clipboard-acknowledgment timeout were treated as harness issues; the latter's text insertion was independently visible. Test filesystem permissions were restored, the fixture app was quit, and its runtime data was moved into local evidence. Both review servers and the preview server were stopped. No real user records were renamed or replaced, and no login startup or global settings were changed.

Raw local evidence under `evaluation/runs/publish-2026-09-14` retains prompts, responses, source snapshots, original and repaired apps, hashes, fault fixtures, receipts, and observations. Those local records are not included in the public download. The plan, tests, report, skill, and portable preview gallery are included.
