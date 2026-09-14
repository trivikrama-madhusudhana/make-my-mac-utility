# Make My Mac Utility

I built this skill to turn an app idea into a native Mac utility through a consultation, three interactive design options, and an agreed build brief. It runs in Claude Code or Codex and includes Python helpers for collecting design choices and packaging a local Swift app.

## A choice needs context

Clicking A means little if the design has changed since you saw it. The review helper freezes the preview and brief, hashes both, and attaches the choice to that version. It rejects stale or conflicting submissions and saves a receipt before confirming success in the browser. If directory sync fails after replacement, it retains the written choice and asks for an identical retry. A surviving receipt can be replayed, but a failed sync cannot establish durability across power loss.

You can choose A, B, C, or None of these, with optional feedback. A local server delivers the receipt to the agent's active wait command. No external webhook or account is involved. The generated preview runs in a sandboxed frame, separate from the selection token. If the agent session has ended, the choice stays on disk for retrieval; the helper cannot wake the session.

Selecting a design also isn't permission to build. The skill records that direction, resolves the remaining behavior, and checks the user's build agreement before implementation starts.

## The native app has to survive actual use

HTML can establish layout and interaction, but it can't establish native focus, window behavior, or persistence. The skill requires separate checks on the packaged app, including mouse click followed by typing, keyboard commands, quit and relaunch, and failures that could lose pending work.

During evaluation, a knitting counter passed its initial logic checks but failed native shortcuts and could discard a pending increment after a save failure. Those failures led to repairs and more specific skill instructions. The [validation report](evaluation/PUBLISH-VALIDATION-RESULTS.md) distinguishes original output, observed repairs, and retests. A passing generated test suite alone doesn't make an app ready.

Packaging has its own boundary. The helper copies the executable and resources into an app bundle and applies local ad-hoc signing. It doesn't provide public signing or notarization.

## Running it

Copy `skills/make-my-mac-utility` from this repository into your client's skill directory, checking for an existing copy first. Then ask for `make-my-mac-utility`, or ask the agent to read its `SKILL.md` if discovery hasn't refreshed. Describe the job you want the app to do; the consultation works out its form and behavior with you.

| Requirement | Detail |
| --- | --- |
| Codex skill directory | `~/.agents/skills/` |
| Claude Code skill directory | `~/.claude/skills/` |
| Design review | A browser; Python 3.10 or newer for the optional local choice helper |
| Native build | A Mac with a compatible Swift toolchain and macOS SDK |
| Helper dependencies | Python standard library; no third-party Python packages |
| Client capabilities | File access and command execution; GUI testing needs available browser and native interaction tools |

The same skill folder is used by both clients. Chat selection remains available when localhost tools or persistent execution aren't available. Generated apps use SwiftUI/AppKit; these are standalone apps, not WidgetKit widgets.

## Development and evaluation

Run the complete helper suite on a Mac with Swift and `codesign`:

```sh
python3 -m unittest discover -s evaluation -p 'test_*.py' -v
```

For the review bridge alone, without building a native app:

```sh
python3 -m unittest discover -s evaluation -p 'test_design_review.py' -v
```

The current suite has 14 bridge tests and four packager tests. [Earlier evaluations](evaluation/RELEASE-CANDIDATE-RESULTS.md) cover Astra and Sol in Codex, and Opus and Fable in Claude Code. The September 14 follow-up adds a knitting-counter build and browser-to-agent delivery in Codex. It does not establish a fresh four-model pass after every final edit, or verify Claude Code's background notification route.

All native evaluation used one Apple silicon Mac. Intel hardware, another Mac, older macOS runtimes, VoiceOver, and the full Spaces and sleep/wake behavior remain unverified. Grok output is retained as historical evidence and is outside the supported release scope.

## Repository and generated files

| Path | Contents |
| --- | --- |
| `skills/make-my-mac-utility/` | Installable skill, references, review page, and helper scripts |
| `evaluation/` | Plans, scenario fixtures, tests, and reports |
| `review/` | Preserved HTML design galleries; download or clone and open locally |
| `examples/pocket-notes/` | A fictional notes-app consultation example |
| `package-metadata.json` | Source distribution metadata, not a package-manager installer |
| `design/brief.md` in a generated project | Behavior, data contract, selected design, agreement, and acceptance checks |
| `design/options.html` in a generated project | Interactive design options |

Runtime app storage is agreed during consultation rather than imposed by the skill. Review state contains a local selection token and is private working data. Raw agent runs, local build artifacts, and screenshots are excluded from this repository. The [evaluation index](evaluation/README.md) explains which evidence is included and which was retained locally.

Build source and skill archives with `python3 evaluation/package_release.py`. Outputs go to the ignored `dist/` directory.

## License and attribution

MIT, copyright 2026 Trivikrama Madhusudhana. The [license](LICENSE) is also included in the standalone skill folder.

I used Matt Pocock's [Writing Great Skills reference](https://github.com/mattpocock/skills) while writing the instructions. It isn't a runtime dependency or bundled content.
