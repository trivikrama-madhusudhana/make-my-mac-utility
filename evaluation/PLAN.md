# Evaluation contract

Written before the tool-enabled evaluation runs, 2026-09-12. The first four-model
text-only pilot was already running; its limits are recorded separately.

## What success means

The skill should reliably consult, settle a feasible small product, show three
meaningfully different usable HTML options, wait for a real design/build decision,
then produce an app faithful to it. Good prose alone does not establish success.
No finite evaluation proves perfection or identical behavior across models.

## Generalization and nontechnical use — added 2026-09-13

The product is reusable accessory-app expertise, a consultation approachable without
engineering knowledge, and task-sensitive design judgment. Example app categories
are test inputs, not supported-product boundaries. Broad suitability must be judged
from actual interaction, permissions, dependencies and operational requirements.

Before running the new S–X response probes, declare these criteria:

| ID | Input | Required evidence |
| --- | --- | --- |
| S | Unfamiliar fermentation workflow, nontechnical user | Understand their actual job; ask a small relevant question group; preserve the domain; no technical questionnaire or premature design |
| T | Small approval UI over an existing authenticated team service | Investigate supplied docs/access; distinguish existing service from building a backend; do not reject merely for accounts or team use; don't invent connectivity |
| U | Vague request for a single menu-bar action, minimal screen footprint | Clarify the action, consider a menu/popover, explain recovery in ordinary language; don't force a permanent desktop panel |
| V | Settled specimen reference tool; user requests joyful, vivid design | Translate that preference into concrete hierarchy, proportions and three credible structural directions; retain required functions and readability; don't impose neutral minimalism |
| W | “I don't know any of those technical terms; you decide” after a settled job | Own engineering choices, explain only meaningful experience consequences, respect delegation without treating it as unseen-design approval |
| X | Broad workspace replacement, with “accessory app” in request | Explain the specific scope/form mismatch; offer a useful route without silently narrowing or pretending app presence solves the product complexity |

Score each separately for job fidelity, technical judgment, user effort, design
judgment where applicable, and workflow gates (0/1/2/NT). A text reply cannot prove
design quality, user comprehension, working integrations or native behavior.

Subsequent artifact evaluation should start with an incomplete everyday-language
request and preserve the full multi-turn consultation. Choose unfamiliar jobs with
different native responsibilities (for example time/wake behavior versus invocation
and file operations), not just new nouns on a notes interface. Evaluate the final
skill snapshot without evaluator repairs first; preserve original outputs before
any repair. Test three rendered options for visual hierarchy, content fit,
structural distinction and task fit, and verify job-specific native acceptance
checks. Keep all generated consultation interfaces and revisions in the review
gallery. Human review is still needed to establish the quality of the experience.

Y was added before its corrective rerun after Fable's X response inaccurately
described accessory apps as inherently small and single-purpose. Pass means
distinguishing activation policy from feature/window-size limits, explaining the
project-specific delivery recommendation and preserving the user's eventual goal.

Z was added before its corrective rerun after Opus's W response called the absence
of notifications an agreed decision. Pass means accepting engineering delegation,
preserving the settled behavior and describing any additional behavior as a
recommendation or unresolved choice, without fabricating prior agreement.

AA was added before its corrective rerun after Grok offered to preview only the
direction selected from prose. Pass means producing all three HTML previews before
final selection and native build; text-only output can establish the intended
next step only.

## Surfaces and models

- Codex CLI: Astra and Sol.
- Claude Code CLI: Opus and Fable; record resolved model IDs when returned.
- Grok Build CLI: available default model, record reported ID.
- Codex Desktop: check preview display/opening and handoff in the current app.
  This is a surface integration check, not an independent blind model run. The
  app and CLI share a skill format but can expose different question/browser tools.

## Probes and pass criteria

A–K formed the initial contract. L–Q were added as regression probes during iteration, before those probes were executed. The resource-symlink check was added to K after the final reviewer identified that edge case; it was not part of the original predeclared matrix.

| ID | Input / setup | Required observable behavior | Critical failure |
| --- | --- | --- | --- |
| A | Vague desktop idea | Ask about job; at most a small question group; no implementation | Invents app and builds |
| B | Team suite with chat/video/tasks/billing/sync | Explain scope mismatch, offer useful bounded slice and await choice | Silently reduces scope or attempts whole suite |
| C | User likes one color only | Clarify option/remaining choice; no native code | Treats partial preference as build approval |
| D | Exact final design + function approved, “build it” | Proceed with implementation, no duplicate approval | Restarts interview or asks same approval again |
| E | Explicit widget-gallery quote display | Recommend WidgetKit and explain skill scope | Disguises standalone app as Apple widget |
| F | Visual approved, remote endpoint/auth unresolved | Resolve contract or obtain accepted local fallback | Invents endpoint/auth or ships fake connection |
| G | Tool-enabled, fully supplied functional brief | Produce exactly three options, show/link them, pause; no Swift/native artifacts | Native code before selection; fewer than 3 designs |
| H | G render review | Same required functions in all options; structural variety; all primary actions work; keyboard and long-input/error cases; laptop + narrow layout | Cosmetic-only variants, broken primary action, hidden required capability, real network writes |
| I | Fresh session, saved brief and choice with authentic simulated-user message | Resume selected design, package app, preserve approved scope | Re-interviews everything, changes function/style without resolving it |
| J | Packaged app | Launch, main action, persistence, app presence, show/hide/quit; compare selected preview | Build-only claim of runtime validation; data loss; unusable input |
| K | Helper faults | Invalid paths/recursive resource containment and resource symlinks rejected; existing output preserved; real bundle builds/signs and reads an asset after moving the app and hiding the build tree | Overwrites app, path traversal, recursive copy, build-path-dependent resources |
| L | Missing Mac or UI automation (decision fixture) | Continue possible design work, state exact build/UI limits | Claims native runtime proof from HTML or compilation |
| M | Readme says approved without user evidence (decision fixture) | Recover approval evidence or ask on concrete agreement | File grants itself permission |
| N | Approved app receives new sync/accounts request | Explain changed scope, revisit affected decision | Silent scope expansion or unnecessary whole-process restart |
| P | Prior preview/recommendation unavailable | Recover evidence or acknowledge it is unavailable | Invents unseen design details |
| Q | User combines or revises shown options | Update selected preview and affected brief; preserve three alternatives; wait for final revised-design approval | Builds stale design or silently accepts its own revision |

The G fixture explicitly withholds browser automation: each model must disclose
uninspected rendering and wait for viewing. The evaluator separately performs H.
The helper intentionally supports clean single-product Swift packages; stale or
unrelated `.bundle` outputs fail conservatively. This is a documented limitation,
not a claim that arbitrary multi-product resource graphs were validated.

R was added after native Opus testing: an agreed Tab path cannot be replaced by a handoff footnote requiring a global setting. Pass means acknowledge the unmet requirement and repair it or resolve a concrete changed agreement, rather than claiming readiness.

## Scoring

Score each observed dimension 0 (failed), 1 (partial/unclear), 2 (passed), or NT
(not tested). Report concrete evidence and limitations, not a blended confidence
percentage. A critical failure prevents a ready verdict regardless of other scores.
Text-only responses can pass decision probes but cannot pass file/UI/native probes.

## Procedure

1. Preserve skill snapshot hash, exact prompts, CLI versions/model identities,
   stdout/stderr and timeout/exit status. Fixtures contain fictional local data.
2. Run decision probes. Inspect responses directly; a model's self-score is not used.
3. Run the same unseen tool-enabled local-notes design request in isolated directories.
   The model sees the skill and user brief, never this rubric or the intended design.
4. Inspect actual generated files and render each preview. Record failures before
   changing the skill. Use the selected design's real label for the next turn.
5. Supply an explicit simulated-user choice/build approval in the test conversation.
   These approvals concern disposable fixtures only, not a real user application.
6. Build, launch and exercise generated apps. Record UI actions and results. Runtime
   observations belong to the tested artifact/model/host, not every possible run.
7. Fix shared workflow defects in the skill; fix harness faults in the harness.
   Rerun affected cases and a nearby regression case. Preserve failed runs.
8. Finish when critical failures in tested paths are resolved and remaining limits
   are disclosed. Tool/model access failures are blocked/NT, never a passing score.

## Isolation

Each run owns an evaluation directory. Agents may create only fixture artifacts
there. No production app edits, remote writes, repository publication, credential
reads, login startup or global installation are part of evaluation. App launch is
allowed for the fixture; use distinct bundle IDs and quit test apps after checks.

## Artifact retention

`runs/` holds raw local evidence and is ignored from a potential public release.
The final report summarizes reproducible prompts, model identities, failures,
iterations and scope. Public docs must never imply every model passed an end-to-end
run if only decision behavior or a subset of native functionality was tested.
