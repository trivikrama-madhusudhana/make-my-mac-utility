# Evaluation summary

**Assessment: ready for an initial beta within the tested workflow.** The repository remains private pending the author's review. Generated apps still need their own verification; these evaluations do not establish reliability across every idea, coding agent, or Mac.

## What was checked

| Area | Evidence and result |
| --- | --- |
| Consultation and design | Four supported model/client combinations completed consultation, interactive previews, revisions, and an agreed native build. Later instruction changes received targeted response checks, not a fresh complete run of every model. |
| Native apps | Notes, tea timers, photo renaming, and a knitting counter exercised different jobs on one Apple silicon Mac. Testing found real defects in keyboard focus, layout, file recovery, and pending changes; repairs and retests are recorded separately from initial output. |
| Browser choice delivery | Actual browser selections reached an active Codex wait command. The helper saves revision-bound choices and handles None, stale previews, conflicts, and storage failures. It cannot restart an ended agent session. |
| Automated helpers | The last release-preparation run passed all 18 tests: 14 review-bridge tests and four app-packager tests, including moved-app resource loading and receipt-persistence failures. |

The supported evaluation matrix is Astra and Sol in Codex, and Opus and Fable in Claude Code. Earlier Grok results are historical and outside the supported release scope. The new browser handoff was exercised in Codex; Claude Code's background notification route was not separately verified.

## Limits that matter

Native testing used one Apple silicon Mac. A second Mac, Intel hardware, older macOS runtimes, VoiceOver, and full Spaces, external-display, menu-bar, and sleep/wake coverage remain unverified. Local app packaging and ad-hoc signing were checked; public signing and notarization were not supplied. Small scenario samples and generated assertions are not a general reliability percentage.

## Supporting records

| Record | Why keep it |
| --- | --- |
| [September 14 validation](PUBLISH-VALIDATION-RESULTS.md) | Browser-to-agent handoff, fresh knitting-counter build, observed repairs, and final helper regressions. |
| [Four-model evaluation](RELEASE-CANDIDATE-RESULTS.md) | Model-specific consultation, native behavior, fixes, and evidence limits. |
| [Pocket Notes sprint](POCKET-NOTES-RESULTS.md) | Earlier notes-app runs and the failures that informed later instructions. |
| [Initial plan](PLAN.md), [four-model plan](RELEASE-CANDIDATE-PLAN.md), [follow-up plan](PUBLISH-VALIDATION-PLAN.md) | The intended checks and scope, separate from the reported outcomes. |

The scenario fixtures, rubrics, and runner scripts support future regression work. Historical preview-check and gallery-builder scripts are retained for reproducing local experiments; they require their matching run artifacts and are not general-purpose graders. The generated galleries and raw run data are excluded from the repository. The standalone [Pocket Notes example](../examples/pocket-notes/README.md) is unchanged.

## Run the helper checks

On a Mac with Python 3.10 or newer, Swift, and `codesign`:

```sh
python3 -m unittest discover -s evaluation -p 'test_*.py' -v
```

To check only the browser-choice helper without a native build:

```sh
python3 -m unittest discover -s evaluation -p 'test_design_review.py' -v
```

Fresh model runs require authenticated client CLIs and available models. Their commands and manual verification steps are in the supporting reports. `package_release.py` builds the source and skill ZIPs into the ignored `dist/` directory.
