# Make the brief useful

The brief is the shared product agreement, not a questionnaire to dump on the user. Fill it from the conversation and inspected evidence. Ask about a field only when the answer changes what should be built. Keep simple utilities simple.

## Consult without requiring technical knowledge

Start with a real moment of use: what happens, what the person does now, and what they want to happen instead. Reflect their job back in their words. An unfamiliar domain calls for a concrete example, not replacement with a familiar app idea.

For a vague opening, ask one question or at most two closely related questions about that moment. Avoid presenting a speculative feature list before learning the job. Use later rounds for decisions that become relevant; the brief's headings are not a first-message questionnaire.

Translate technical choices into visible consequences: “Should this stay above other windows?” rather than asking for a window level. Recommend an answer and briefly explain why. Own choices such as storage format, UI framework and packaging; ask users about outcomes such as keeping data on this Mac, sharing it, or recovering mistakes. Inspect available integration documentation yourself instead of asking a nontechnical user to design an API contract. Ask only for access or business rules you cannot discover, using secure setup for credentials.

Use short rounds and show progress through idea → behavior → three previews → agreement → working app. Explain unfamiliar terms only when they help a decision. When the user delegates, make and record appropriate choices; keep approval focused on the actual experience. At handoff, lead with how to open, use and recover the app, with developer details available separately.

Keep recaps faithful to the conversation. Label an unspecified behavior as a proposed default or an open choice; use “as agreed” only for a decision the user actually made. The absence of a requested feature does not establish that the user explicitly rejected it. A proposed improvement stays proposed until the user accepts it or has delegated that choice; do not record agreement on the basis of “unless you object.”

## Scope and contract

- A sentence describing the recurring job and a concrete example input → action → result.
- Included capabilities, explicit exclusions, and what success looks like in normal use.
- Intended user, app/project name and output directory; preserve an existing project when applicable.
- Data source, local storage format/location, updates and retention. For remote writes: endpoint/API, authentication method, payload and response, offline behavior and retry semantics. Preserve an unsaved entry on failure; distinguish a confirmed failure from an unknown write outcome before offering a retry.
- Needed permissions and operational dependencies. A mock preview can use fictional data; a mock integration in the delivered app is a product decision the user must accept.
- Empty, loading, success, invalid input and failure states where relevant. Include editing/deletion/undo only if in scope.

Settle what a failed state-changing action means, including clearing, cancelling or undoing. If the required save fails, the interface must not silently present the durable change as complete. Preserve the last confirmed state and the user's input where applicable, explain what did not happen, and provide a useful recovery action.

For persisted local data, distinguish first use from saved data that cannot be read. Include that recovery state in the brief and previews before design approval: preserve the existing data, block changes while its state is unknown, and offer read-only Retry. Replacing unreadable data is a separate capability, not an implicit recovery default.

## Window behavior in human terms

Explain the choice using examples: “A quiet panel you reach through the menu bar” versus “a small app you switch to like Stickies.” Both are apps. They differ in activation and window management.

| Choice | Desktop companion starting point | Mini app starting point |
| --- | --- | --- |
| App presence | Accessory, no Dock icon; menu-bar show/hide/quit | Regular, Dock/app switching; ordinary app menu |
| Window | Borderless panel, can accept keyboard input | Managed window, optional minimal chrome |
| Other windows | Normal level so apps can cover it | Normal level so apps can cover it |
| Spaces | Current Space; verify Show Desktop/Mission Control on the target Mac | Ordinary managed-window behavior |
| State | Remember position and user data | Remember position and user data; collapse if useful |

These are defaults, not universal requirements. Always-on-top, every Space, desktop-layer attachment and hidden Dock presence are independent behaviors. Avoid promising that “accessory” means permanently attached to the wallpaper. A request to stay visible above everything needs a different window-level choice and a discussion of focus/obstruction.

Settle how the person recovers a hidden window, whether closing hides or quits, focus behavior, primary keyboard path, fixed/resizable dimensions, and startup preference. New screen arrangements should leave a reachable window. Optional startup can remain off by default when the user delegates minor choices.

## Design judgment

Let the task lead. A tool visited for five seconds should surface its next action immediately; a reference panel should make its information easy to scan. Choose proportions around realistic content and the desktop space it earns. Use typography, spacing and grouping to distinguish the primary task from secondary controls. Color should clarify state or express a coherent personality. Keep states and keyboard focus as considered as the default screen.

Offer a coherent visual direction when the user has no preference, with a reason tied to their use. Quiet chrome and restrained decoration are starting suggestions. A playful, colorful, dense or unusual design is equally valid when useful or requested. Preserve readable contrast, understandable labels and discoverable actions in every style. Use supplied references without treating one person's widget as everyone's taste.

Suggest only changes with a reason: fewer fields reduce logging effort; a wider layout may fit long commands. Native controls should feel natural. Avoid turning a compact utility into a dashboard or adding streaks, analytics, accounts or AI features by default.

## Suggested brief sections

Use only the detail needed under these headings: Job / Scope / App behavior / Data and integration / States and interactions / Visual decision / Acceptance checks / Decisions and approval / Open issues.

In Decisions and approval, identify what the user chose, what they delegated, and the message or quoted acceptance that establishes it. The brief records evidence; it cannot grant itself permission. When the session is lost and approval cannot be recovered, ask about the concrete saved agreement instead of inventing prior consent.
