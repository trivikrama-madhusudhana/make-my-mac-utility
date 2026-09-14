# Make My Mac Utility

This skill helps you turn an app idea or a repeated workflow into a native Mac utility through a consultative process. It works with Claude Code and Codex. Other coding agents may be able to follow the instructions, but the supported release has been evaluated with these two clients.

You might want a small panel to capture notes while you work, a knitting counter that remembers your place, or a menu-bar shortcut for a task you repeat throughout the day. Start with what you want to do. The agent helps you decide how the app should work, explores designs with you, then builds and tests it on your Mac.

You don't need to arrive with a specification or know how to build a Mac app. The skill gives the agent a consultation process and native Mac guidance, so it can recommend choices and explain what they mean for your experience.

## From an idea to an app you can use

The consultation starts with the job: what triggers it, what you do, and what a useful result looks like. The agent helps you choose a suitable form, such as a desktop companion, a menu-bar popover, or a compact app. It works through the behavior that matters for your idea, including how you open it, where it saves your work, and any services it needs to connect to. You can make those choices yourself or delegate them to the agent.

Once the behavior is understood, you get three interactive design options to try in your browser. These explore different layouts and ways of using the same app. You can compare them, choose a direction, combine elements, or explain what feels wrong.

Three designs are the starting point. Ask for more alternatives, request changes, or choose “None of these” to keep exploring. The consultation continues until you've settled on a design and behavior you want built. The browser offers A, B, C, and “None of these” buttons with optional feedback; you can also give feedback directly in the conversation.

When you're ready, the agent recaps the agreed app and builds it with your approval. It checks the packaged app against that agreement, repairs issues it finds, and tells you what it could and couldn't verify. You receive a local app you can launch, editable source code, and instructions for building, using, and maintaining it.

For an example, the [knitting-counter review](review/publish-validation/index.html) shows an initial set of designs and a revision that adds recovery for unreadable saved data. Download or clone the repository and open the HTML gallery locally to try the previews.

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

## How design feedback reaches the agent

The skill includes a local review helper that sends your browser choice to the agent while its wait command is active. No external webhook or account is needed. If that session has ended, the choice is saved for later retrieval; the helper cannot restart it. Chat feedback remains available.

Each choice belongs to the preview and brief you reviewed. The helper rejects stale or conflicting submissions, and changing direction starts a new review round. Choosing a design records your preference; the agent still follows your agreement about when to build. See the [review helper reference](skills/make-my-mac-utility/references/design-review.md) for setup, storage, and recovery details.

## Development and evaluation

The skill includes Python helpers for collecting design choices and packaging a local Swift app. The packager applies local ad-hoc signing; public signing and notarization are separate distribution work.

Testing includes more than the HTML previews. During evaluation, a knitting counter passed its initial logic checks but failed native shortcuts and could discard a pending increment after a save failure. The agent repaired those issues, and the skill gained more specific verification instructions. The [validation report](evaluation/PUBLISH-VALIDATION-RESULTS.md) records original output, repairs, retests, and remaining limits.

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
