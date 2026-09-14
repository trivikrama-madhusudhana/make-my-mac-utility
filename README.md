# Make My Mac Utility

A skill that brings Mac accessory-app expertise, design judgment and a friendly consultation to your app idea. No technical knowledge required to describe what you want.

Describe the job. The agent assesses whether it fits a desktop utility, settles the behavior with you, and shows **three interactive HTML design options**. After you select and approve the design and functionality, it builds the native app.

Choose **A, B, C, or None of these** in the browser, with optional feedback. The bundled local review server sends that choice to the waiting agent session automatically. No external webhook or account is needed. The agent must keep its wait active; a saved choice can be retrieved later, but the helper cannot wake an ended session. Where localhost tools are unavailable, you can reply with your choice in chat. Choosing a design records your direction; the exact build agreement still determines when implementation begins.

The app's job is yours to define. The skill recommends a suitable form: a quiet desktop companion, menu-bar popover, shortcut-invoked panel, or compact regular app you can switch to like Stickies. These are possibilities, not a catalog of templates. If the essential experience needs another kind of application, it explains why and helps you choose a route.

These are standalone SwiftUI/AppKit apps, not Apple WidgetKit widgets. Rich text entry, search and custom window behavior can motivate that choice; it is not a claim of lower memory or battery use. The agent handles engineering choices and explains decisions in terms of how the app will feel and work.

## Use in Claude Code or Codex

The identical skill folder is used across clients. It has no required plugin, other skill, model-specific API, or browser connector. A browser is used for design review; a Mac with a compatible Swift toolchain is needed to build and test the native result.

Copy `skills/make-my-mac-utility` into your agent's skill directory:

- Claude Code: `~/.claude/skills/` for personal use, or `.claude/skills/` in a project.
- Codex: `~/.agents/skills/` for personal use, or `.agents/skills/` in a project.

Then ask for `make-my-mac-utility`, or explicitly ask the agent to read its `SKILL.md` if your client has not refreshed skill discovery. Claude Code also supports `/make-my-mac-utility`; Codex supports `$make-my-mac-utility`.

Example:

> Use make-my-mac-utility. I want a little panel where I can log what I worked on without opening a spreadsheet. Help me decide the smallest useful version.

The skill asks for missing decisions rather than forcing a long questionnaire. You can delegate minor choices. If you want an Apple widget from the widget gallery, it will explain the difference and recommend that route instead.

Design judgment is part of the consultation: proportions that fit your content,
clear hierarchy, considered typography and spacing, and a visual personality suited
to the job. Each of the three options offers a real layout choice. You can ask for
quiet, vivid, playful or dense; the agent recommends a direction and explains why.

The release targets Astra and Sol in Codex, and Opus and Fable in Claude Code.
See the [four-model review gallery](review/release-candidate/index.html) to compare the actual consultations and revisions. The [earlier sprint archive](review/index.html) and [Pocket Notes example](examples/pocket-notes/options.html) are preserved too. Grok is outside the supported release scope.

## What you get

- `design/brief.md`: scope, behavior, data contract, selected design, approval and acceptance checks.
- `design/options.html`: three designs and the revised selected option, viewable offline.
- Editable native source and a launchable local `.app` after the build agreement.
- Build/run instructions and an honest record of what was tested.

HTML is a design prototype. Native window behavior and integrations are checked separately. Public signing/notarization is a later distribution step; the included packager performs local ad-hoc signing.

## Evaluation and provenance

The [September 14 publish validation](evaluation/PUBLISH-VALIDATION-RESULTS.md) covers a fresh knitting-counter build, observed native repairs, paired response probes, and browser-to-agent choice delivery. Its [preserved preview gallery](review/publish-validation/index.html) shows both design revisions. The skill folder and standalone download include the MIT license.

See [the release evaluation](evaluation/RELEASE-CANDIDATE-RESULTS.md) for model runs, observed results, repairs and limitations. Model compatibility means a shared workflow, not identical design output. Codex Desktop uses the same skill instructions; its preview, question and automation tools may differ from the CLI.

Written using Matt Pocock's *Writing Great Skills* principles: checkable completion criteria, progressive disclosure, and pruning repeated instructions. The locally installed `matt-pocock-writing-skills` reference was consulted; it is not bundled or required to run this skill. Upstream: [mattpocock/skills](https://github.com/mattpocock/skills).

The window patterns come from personal native desktop tools. Examples and evaluation fixtures use fictional local data; the package does not contain their client integrations or credentials.
