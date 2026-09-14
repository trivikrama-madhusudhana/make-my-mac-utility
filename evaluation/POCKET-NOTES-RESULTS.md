# Pocket Notes sprint and scope evaluation

Latest follow-up: [September 14 publish validation](PUBLISH-VALIDATION-RESULTS.md), including the browser choice bridge and a fresh native app with real fault-injection checks. Earlier reports below retain their original scope and model coverage.

For the current Claude Code/Codex four-model release, start with [the release evaluation](RELEASE-CANDIDATE-RESULTS.md). The record below preserves the earlier five-model Pocket Notes sprint and subsequent scope probes; Grok is historical, not supported release coverage.

Evaluation ran September 12–13, 2026. The skill is ready for review and use within the tested workflow. All five models produced three-option consultations and native apps; the evidence below distinguishes original output, repairs, test instrumentation and remaining coverage. This is not a claim of perfection or complete macOS certification.

The test contract is in [PLAN.md](PLAN.md). The important checks were defined before artifact runs: scope assessment, three meaningful previews, a real approval boundary, resuming an approved brief, and testing the packaged app. Regression probes were added when review or execution revealed a specific weakness.

## September 13 scope and consultation revision

The current skill explicitly supplies accessory-app expertise, consultation for
nontechnical users and adaptable design judgment for user-defined jobs. It assesses
fit by interaction, dependencies and operating needs, supports different app
surfaces, and treats sample apps as examples rather than a supported-category list.
The earlier native builds below predate this revision. Their final skill hashes
are preserved in `pocket-notes-sprint-skill.sha256`; `final-skill.sha256` identifies
the current package, not a retroactive snapshot of those builds.

New text-only S–X probes used fermentation tracking, an existing studio approval
service, a menu-only morning action, vivid specimen reference design, engineering
delegation and a full studio platform. The fixtures and acceptance criteria were
written before execution. Raw evidence and per-stage skill hashes are retained
locally under `runs/generalization-r1` and the corrective run directories.

Observed results from the first run:

| Dimension | Astra | Sol | Opus | Fable | Grok |
| --- | --- | --- | --- | --- | --- |
| Preserve unfamiliar job and ask relevant plain-language questions (S) | 2 | 2 | 1 | 2 | NT |
| Existing service fit and proposed documentation investigation (T) | 2 | 1 | 2 | 2 | NT |
| Consider menu surface and clarify actual task (U) | 2 | 2 | 2 | 2 | NT |
| Concrete, distinct, vivid design directions in prose (V) | 2 | 2 | 2 | 2 | NT |
| Own engineering choices and preserve actual agreement (W) | 2 | 2 | 1 | 2 | NT |
| Explain platform scope without silently narrowing (X) | 2 | 2 | 1 | 1 | NT |

These are evaluator judgments about the actual replies, not model self-scores.
Opus's S reply prematurely stated local/no-account storage; its W reply described
the absence of notifications as agreed when it was not. Sol's T reply recognized
the existing service but moved to UI questions without explicitly prioritizing
the supplied documentation. Fable and Opus's X replies described accessory apps
as inherently small and focused; the revision clarifies that activation policy
does not impose a feature or window-size limit. The consultation guide also makes
the distinction between proposed defaults and actual agreement explicit.

All four completed model runs offered structurally distinct specimen designs with
concrete visual treatments. This establishes design reasoning in prose only;
rendered visual quality, human usability and generalization in native builds are
not tested by these probes. Existing HTML snapshots remain unchanged.

Corrective probes: Fable passed Y in `runs/scope-explanation-r2`, distinguishing
activation policy from the recommendation about platform scope. Opus passed Z in
`runs/delegation-recap-r2`, taking engineering responsibility without inventing a
prior notification decision. These are targeted response regressions, not fresh
end-to-end runs of every model against the final package.

Grok's first S–X attempt hit its five-turn limit while repeatedly trying to read
files in the text-only harness. It authenticated successfully; this was not an
account failure. The retry in `runs/generalization-grok-r2` used an explicit inline-
content instruction and returned all six replies, but still began with a file-read
announcement. Its S/T/U/W/X content met the response criteria. V supplied concrete
design directions but proposed previewing only the direction chosen from prose,
violating the three-HTML-options requirement. That is a failed workflow gate,
regardless of the design prose. The HTML guide was clarified and AA added as a
targeted corrective probe. Neither attempt constitutes an artifact pass.

The AA retry in `runs/three-preview-grok-r3` again exhausted the five-turn limit
without a case answer. The corrective instruction is in the final skill, but its
Grok regression remains NT due to the harness failure. No passing score is inferred
from that edit. Further Grok validation should use a working isolated interactive
or tool-enabled fixture rather than repeatedly retry this text-only configuration.

## Models and surfaces

| Coding agent | Requested model | Reported primary model | Observed result |
| --- | --- | --- | --- |
| Codex CLI 0.153.4 | Astra | `gpt-6-astra` | Three previews, native app, observed core flow and quit/relaunch persistence |
| Codex CLI 0.153.4 | Sol | `gpt-5.6-sol` | Three previews, palette revision, native app, repaired visuals and observed storage-failure recovery |
| Claude Code 2.1.269 | Opus | `claude-opus-5` | Three previews, native app, observed core flow and evaluator-repaired keyboard contract |
| Claude Code 2.1.269 | Fable | `claude-fable-5-1` | Three previews and native app; keyboard-access repair retested successfully |
| Grok Build 1.0.3 | Grok 4.6 | `grok-4.6-build` | Authenticated inference, three previews and native app; core flow observed with an evaluator-only launch hook |
| Codex Desktop | Current evaluator | Surface check, not another blind model run | Opened and exercised generated HTML and native apps using available browser/accessibility tools |

Claude's usage metadata also lists Haiku housekeeping calls. Those were not the primary evaluation model. Codex and Claude share the same skill files; their available browser and question tools can differ. The Desktop check establishes preview display and interaction in this app, not equivalence of every App/CLI configuration or an independent sixth generation run.

Native host: macOS 26.5.1, ARM64, Swift 5.10, Command Line Tools. The default 14.4 SDK was incomplete/incompatible; an installed 13.3 SDK passed the AppKit/SwiftUI probe and was explicitly selected for builds. Global toolchain configuration was not changed.

## Preserved interfaces

The local sprint archive retains all 15 original designs, labeled by coding agent and model, with later revisions and snapshot hashes. The gallery is excluded from the repository; the [Pocket Notes example](../examples/pocket-notes/options.html) remains available.

These are actual generated consultation outputs, not curated replacements. They all implement the same fictional local notes brief: capture, timestamps, search, delete and undo. Layouts vary between a column, a split view and a retrieval-led or collapsible view. The gallery's selections are review controls, not build authorization.

## Decision probes

Scores are 0 = failed, 1 = partial, 2 = passed, NT = not tested. They apply only to the observed dimension. A text response never earns a native-app or file-generation pass.

| Probe group | Astra | Sol | Opus | Fable | Grok |
| --- | --- | --- | --- | --- | --- |
| A–F: next action for vague idea, excessive scope, partial preference, exact approval, WidgetKit gallery, unresolved integration | 2 | 2 | 2 | 2 | 2 |
| L/M/N/P: non-Mac handoff, false approval field, scope expansion, unavailable prior preview | 2 | 2 | 2 | 2 | 2 |
| G: actual three-option HTML, no native UI before user choice | 2 | 2 | 2 after resume | 2 | 2 |
| H: rendered behavior and states | 2 | 2 | 2 | 1 | 1 |
| Q: actual combined-design revision, brief updated, build still waiting | NT | 2 | NT | NT | NT |
| R: unmet keyboard agreement cannot be handed off as ready | NT | NT | 2 | 2 | NT |

The pilot's main next-action decisions were correct, but Opus and Fable embellished some underspecified agreements. The skill was tightened to recover an unavailable preview before describing it and to recap only agreed capabilities. The missing-preview and scope regressions then passed. Grok also respected the build boundary, although its color-only response recommended the whole option on a weak rationale; aesthetic judgment still benefits from human review. This is a one-run-per-case decision sample, not a reliability percentage.

Astra and Sol's previews passed save, search, delete/undo, keyboard save, failed-input retention and empty validation in all three options; their automated browser checks reported no script errors or HTTP requests. Opus passed the same main loop and failed-save retention through the Desktop browser. Fable and Grok passed the main loop in all three, with failure-state checks concentrated on their first option; their H score remains partial rather than extrapolating one option's result to all three. Narrow-window checks retained the intended native dimensions with internal scrolling where necessary. IAB viewport zoom and occasional tiled screenshots were treated as harness limitations, not automatically as product defects.

## Native evidence

- **Astra:** launched the packaged app, saved and searched a note, deleted/restored it, quit with Command-Q, relaunched and found the saved note. Input/search were readable and the selected layout was recognizable. Command-Q termination was also confirmed by process absence. Generated logic checks and packaged non-GUI persistence checks passed.
- **Sol:** saved, searched, deleted and restored a note. Runtime review caught unreadable search text and extra window chrome; the model repaired both and the evaluator inspected focused/unfocused text in the rebuilt app. A process restart retained notes. Replacing only the fixture's storage-directory path temporarily with a file produced a real save error; the draft remained, and retry succeeded after restoring storage. A permissions-only attempt had not caused a failure and was not counted as one. Menu Quit was not observed, so process restart is not described as a Quit test.
- **Fable:** native save/search and readable input observed. Initial Tab navigation skipped a hover-only Delete control, which was also absent from the accessibility tree. The repair exposed Delete at rest and provided a focus cycle that works under the actual system settings. Tab from Search selected Delete with a visible ring; Return deleted the note and selected Undo; Return restored it. Quit/relaunch preserved the saved note. A simulated native write failure showed an error and retained the draft. Command-Q and the visible app-menu Quit both terminated the test app. The build reported 78 logic checks before repair and 111 afterward, all passing.
- **Grok:** built the app after a 1,072.24-second resume and reported 47 passing logic checks. Its default startup is menu-only, which the native CUA surface could not inspect without a window. The evaluator added a `--show-on-launch` flag calling the existing Show method; the original source is preserved and default startup is unchanged. With that hook and an isolated data argument, native save/search/delete/undo, readable controls and Command-Q/relaunch persistence passed. The original status-menu interaction remains unverified. Both the original app archive and instrumented archive passed strict verification after fresh extraction.
- **Opus:** completed its native build in 1,493.23 seconds and reported 73 passing logic checks. The original app passed save/search, pointer delete/undo and quit/relaunch persistence. All 73 logic checks passed again after the evaluator repair. Native Tab testing reproduced a dependence on a global setting despite the agreed contract. The evaluator repaired two button subclasses to preserve the existing key loop without changing system settings; Tab and Space then operated Save, Delete and Undo with visible focus. A real blocked-storage-path test retained the draft and showed a readable error; retry succeeded after restoration. Original source and both original/repaired verified app archives are retained. This was an evaluator repair, not an unassisted model pass.

Full menu-bar interactions, Spaces, Mission Control, Show Desktop, external-monitor removal and VoiceOver were not comprehensively exercised. No model receives an unqualified full J pass. The regular mini-app route is documented and grounded in existing native apps, but this fresh generated-app fixture used accessory mode. This evaluation does not establish fresh end-to-end coverage for both window categories on every model.

## Iterations that changed the skill

1. Made WidgetKit explanation conditional on a widget/ambiguous request, kept behavior decisions before design, and left final layout/dimensions for visual selection.
2. Made per-option render observations explicit; a browser launch or an agent-written approval status cannot authorize implementation.
3. Added recovery of unavailable preview evidence, scope-faithful recaps and a regression for combining two designs.
4. Corrected the resource-packaging approach. The small helper supports plain assets loaded through `Bundle.main`; it rejects unsupported SwiftPM `Bundle.module` layouts rather than shipping a build-directory-dependent app.
5. Added output/resource containment, symlink rejection and refusing an existing bundle. A real resource test moves the app and hides the Swift build tree before loading its asset.
6. Added an AppKit/SwiftUI preflight compile and explicit SDK override support.
7. Added focused/unfocused AppKit text checks, matching native chrome and keyboard/accessibility checks under actual system settings.
8. Added signature verification at the final bundle location. This workspace reattached Finder metadata to visible `.app` directories. Apple documents why such attributes invalidate signing. The guidance distinguishes a verified staging/archive result from a subsequently altered visible bundle. [Apple QA1940](https://developer.apple.com/library/archive/qa/qa1940/_index.html)

R additionally checks that an agreed keyboard contract cannot be replaced by a handoff caveat requiring a global system setting.

The independent Sol review found no blocking workflow defect after the earlier fixes. Its final resource-symlink observation became an additional regression, rather than being ignored as theoretical.

Fresh archives of all five models’ apps, including the repaired variants were independently extracted outside the synced project and passed strict code-signature verification. This verifies those archived contents; it does not make the visible synced `.app` directory immune to later metadata changes.

## Runtime and harness failures retained

- Opus's first and second high-effort design invocations each hit 720 seconds. The second fixture completed its preview in 394.76 seconds after a fresh medium-effort resume. They remain recorded as timeouts, not silently replaced by the successful run.
- Fable's native invocation hit 720 seconds after producing most artifacts. A medium-effort fresh resume completed review, packaging and documentation in 231.79 seconds. Native accessibility testing then required another repair.
- Grok's first native invocation hit 720 seconds. Its continued build completed in 1,072.24 seconds with the longer limit. The account itself works: both inference and artifact generation completed successfully.
- Grok's original text harness allowed only one turn and cancelled. Restricting its exposed tools explicitly and allowing five turns produced a completed four-case edge response. This was a harness failure, not an authentication failure or a passing test.
- Opus also wrote and then removed an early disposable XCTest probe in `/tmp`, outside its fixture-only instruction; this is recorded as an isolation deviation.
- During Fable's repair, a diagnostic read inspected extended attributes/signature status of sibling evaluation bundles despite the fixture-only instruction. It did not read their source or alter them, but this is an isolation deviation and that diagnostic phase should not be described as strictly isolated.
- Early runs retained prompts, outputs and local skill copies, but did not fingerprint every stage before execution; some reference files were refreshed for later stages. Later harness runs record stage-specific hashes. Final hashes must not be misrepresented as the exact initial inputs of every run.

## Installed discovery checks

The final skill is linked into the local Codex `~/.agents/skills` and Claude `~/.claude/skills` directories. A fresh Codex CLI invocation found and read the installed skill by name and asked about the recurring job. A fresh Claude Code invocation registered the skill, called its Skill tool, loaded the installed folder and began the consultation. Neither was given the skill path or contents in the prompt.

The first Claude discovery attempt disabled user settings, which also disabled its skill registry; it found the repository copy through a file search instead. That attempt is not counted as installed discovery. The corrected run enabled user settings while disabling hooks and external MCP configuration. Grok's automatic skill discovery was not separately evaluated.

## Reproduce and inspect

Run these from the package root after authenticating the relevant CLIs. Model IDs depend on account availability. The harness does not read or export credential files.

```sh
python3 evaluation/run_decisions.py --label decisions-new
python3 evaluation/run_decisions.py --label edge-new --cases-file evaluation/edge-cases.txt
python3 evaluation/run_artifact.py --model gpt-6-astra --label astra-new
python3 evaluation/run_artifact.py --model opus --label opus-new --effort medium
python3 evaluation/run_artifact.py --model grok-4.6 --label grok-new
python3 evaluation/test_packager.py
python3 evaluation/run_discovery.py --label discovery-new
python3 evaluation/build_review.py
```

Inspect the three actual previews before writing a fixture approval. Save a prompt that names the exact shown option, approved behavior and an isolated data path; then run:

```sh
python3 evaluation/run_artifact.py --model opus --label opus-new --existing --stage build --effort medium --prompt-file /path/to/fixture-approval.txt
```

The artifact harness defaults to a 1,800-second limit and accepts `--timeout`. Native apps require separate GUI evaluation after the headless run. `check_astra_preview.cjs` and `check_sol_preview.cjs` preserve the earlier locator-based browser checks for those exact outputs; use a locally installed Playwright or `PLAYWRIGHT_MODULE` when reproducing them in an environment that permits that browser route. They are not universal scorers for arbitrary generated markup.

Raw local evidence lives under `evaluation/runs/`: prompts, responses, metadata, snapshots, browser observations, generated source and `.app` builds. It is ignored from a potential public release; no production client code or credentials are needed for the examples. The design galleries are also retained locally and excluded from the repository. This report remains included.

The packaging helper’s four regression tests passed on the final implementation. A final native Grok test build also used the current helper with an explicit SDK and passed strict signature verification at its hidden output location before successful GUI launch. See `final-skill.sha256` for the delivered skill contents.
