---
name: make-my-mac-utility
description: Build native Mac accessory apps through a consultation for nontechnical users. Use when someone wants a desktop tool, widget-like panel, menu-bar utility or compact app; assess fit, recommend behavior and show three HTML designs before implementation.
---

# Make My Mac Utility

Bring native Mac accessory-app expertise and design judgment to the user's own idea. The subject and functionality are open-ended; assess whether this app form serves the job. Consult first, show three designs, agree the product, then build. Guide nontechnical people through choices about their experience while handling engineering decisions yourself.

This workflow uses ordinary files, HTML, a browser, and native macOS tools. It works in Claude Code and Codex without requiring another skill, a particular model, a connector, or a proprietary question tool. Resolve bundled references and scripts relative to this SKILL.md. Use the host's question UI when available, otherwise ask in conversation.

## 1. Understand the job and assess fit

Read [consultation.md](references/consultation.md) before the first consultation response.

If the idea is missing, ask what they want to build and what repeated task it would help with. Otherwise use the supplied context and ask only about unresolved choices. Keep each round to one decision or a small group of closely related questions; recommend a sensible answer with its trade-off.

Identify the trigger, main action, input, useful output, intended user, and where data lives. Inspect supplied or readily discoverable relevant code/examples before asking the user for information those artifacts contain. Assess scope before drawing screens:

- **Fits:** the requested experience works as a focused, readily accessible Mac utility. Judge its interaction, data, permissions and operating needs, not whether its subject matches a familiar example. An existing service, account, AI capability or local automation can be part of a suitable utility.
- **Needs investigation or narrowing:** an essential capability is uncertain, or delivering the requested experience requires substantial additional systems. Investigate the concrete dependency; explain what is feasible and offer a useful first slice only when needed. Let the user accept or revise any scope change.
- **Different product:** the essential experience needs another form, such as Apple's widget gallery or a full workspace application. Explain the specific mismatch and recommend a suitable route. Offer a companion only if it preserves a useful part of their goal; proceed after they choose it.

When the user asks for a widget or the app category is ambiguous, explain the architecture in plain language: these are standalone native apps, not WidgetKit extensions. WidgetKit suits glanceable information and simple actions; rich text entry, search, and custom window behavior motivate this approach. Accessory mode controls app presence, not resource efficiency or a technical limit on features and window size. Explain scope concerns in terms of the requested experience and delivery dependencies; a complex product is not made simple by hiding its Dock icon. A gallery widget request deserves a WidgetKit recommendation rather than a disguised app.

**Complete when:** the user has supplied or accepted a bounded job, its success condition, and the intended app category. If narrowing is needed, wait for their choice before designing it.

## 2. Settle behavior and feasibility

Create `design/brief.md` in the agreed project directory. Record the job, included/excluded capabilities, window behavior, data contract, states, appearance preferences, constraints, and observable acceptance checks. Mark proposals and unanswered questions explicitly.

Recommend the app presence and window behavior that fit the job. A **desktop companion** and a **mini app** are starting points, not a two-template limit; a menu-only utility, popover or shortcut-invoked panel may fit better. Explain how it feels, then settle Dock/app switching, covering versus floating, Spaces, hide/reopen/quit, placement, keyboard interaction, persistence and startup only to the detail relevant to this app. Record visual preferences and size constraints here; final dimensions, layout and style are chosen through the previews. Offer defaults; a user's explicit delegation of these choices is valid and should be recorded.

Check the development environment and integration feasibility before promising behavior. A missing service contract or unsupported macOS feature is a decision to resolve, not an implementation detail to invent. Read-only checks and disposable non-UI feasibility probes are allowed here; native UI implementation starts after Step 4. On a non-Mac, consultation and HTML can proceed, but agree a Mac build/verification handoff.

**Complete when:** the functional contract and technical route are settled, including a user-accepted fallback or deferred integration where necessary. Visual choices remain open for the next step.

## 3. Show three HTML designs

Read [html-designs.md](references/html-designs.md). Create `design/options.html` containing exactly three distinct options for the agreed app. All three implement the same agreed capabilities with safe local sample data. Vary meaningful layout, density, information hierarchy or interaction—not just color.

Render and show the HTML using available browser tools or open the local file. Provide the file link too. Inspect the rendered result when tools permit, exercise the primary interaction and relevant error/empty states, and fix clipping or broken controls before presenting. Report which checks were observed. HTML illustrates app appearance and interaction; it does not prove native window behavior.

Explain differences you can actually inspect, recommend one with a task-specific reason, and invite the user to select or combine options. If a preview or prior recommendation is unavailable, recover it before describing its layout. Use the bundled [design review bridge](references/design-review.md) when localhost tools are available: show A/B/C and “None of these” buttons, and keep an agent wait active so the deliberate browser submission returns to this session automatically. Optional feedback accompanies the choice. With no local server, provide a copyable choice summary and receive it in conversation.

A received review event records the user's design selection only for its matching preview and brief revision. “None of these” calls for revised options, not a build. Defaults, localStorage, stale events, and automated evaluation clicks do not constitute user approval. Record test submissions as test evidence. Selecting a design does not by itself authorize native implementation; apply the build agreement below.

**Complete when:** all three options have been shown; render/interaction checks have per-option results or are explicitly uninspected for the user to check; and the user has selected a direction and resolved visual revisions after viewing it. A browser launch alone is not user acceptance. While waiting, keep work to previews and the brief.

## 4. Record the build agreement

Update `design/brief.md` with the selected option, final dimensions/layout/style, capabilities and states, integration details, all behavior choices, acceptance checks, and the user's approval evidence. Derive the recap from that agreement; familiar extras such as editing, export or a queue are new capabilities until accepted. Preserve the unselected alternatives as history, not as implementation scope. Present a short final recap and ask for approval only if the user's latest message did not already approve that exact design and behavior.

**Build gate:** every product-facing choice is resolved or explicitly delegated, no unresolved integration blocker remains, the final preview matches the agreement, and the user has authorized building it. Silence, a default selection, approval of color alone, or an agent-written status field is not approval. Trace the design choice to the user's message or matching review event, and build authorization to the user's instruction. Continue immediately when that evidence already exists; do not ask twice.

The user can explicitly revise this workflow. Record any requested exception and its consequences; distinguish an exception from an assumption or incidental wording. On resume, read the brief and approval evidence and continue from the earliest unfinished step.

## 5. Build and verify the agreed utility

Only after the build gate, read [native-build.md](references/native-build.md). Build the selected SwiftUI/AppKit app in the agreed directory, preserving existing work. Use the approved HTML as the visual reference, not as an embedded web app. Keep native implementation decisions with the agent unless they affect the agreed experience.

When a discovery changes behavior, scope or appearance, explain the concrete impact, revise the affected preview/brief, and resolve that decision before continuing dependent implementation. Routine bug fixes do not reopen the whole consultation.

Verify the actual packaged `.app` against every acceptance check, including relevant window behavior and failures. Report implemented, observed, and unverified separately. Deliver editable source, the app path, build/run instructions, data location, and how to hide, reopen and quit it. Install or enable login startup only within the user's agreed scope.

**Complete when:** the approved utility is built, the checks have results, any material verification limits are explicit, and the user can launch and maintain it. If blocked by missing Mac access or credentials, deliver the completed artifacts and the exact remaining step without claiming the app was tested.
