# Three options before native code

Make a self-contained `design/options.html` that works offline. Inline CSS/JS and use system fonts and local or inline assets. Use representative fictional content with long and short values. Render HTML through DOM-safe methods when interpolating user text. Preview actions change only local demo state; remote services, real credentials and actual command execution stay out of the preview.

## Comparison, not a landing page

Verbal design directions are preliminary. Create and show all three HTML options
before asking the user to choose a design; choosing from prose must not reduce
the deliverable to a preview of only one option.

Show three labeled candidates at plausible native window dimensions against a neutral desktop-like backdrop. Put explanatory controls outside the app frames. At narrow browser widths, stack the candidates or provide clear tabs while keeping all three accessible. Preserve the app's intended dimensions rather than accidentally presenting a mobile redesign.

Each candidate needs a meaningful difference, such as:

- A compact single-column form versus a horizontal quick-entry strip versus a collapsed summary that expands to the form.
- A searchable command list versus categorized cards versus a compact pinned list with search.

Choose differences appropriate to the agreed job. These examples are not three mandatory styles. Keep required functions in every candidate and show how a collapsed option reveals them. If an option changes a functional choice, label the trade-off and return that choice to the agreement.

Give each option a clear design rationale grounded in how the person will use it. All three should be credible recommendations, with intentional proportions, typography, spacing and treatment of secondary actions. Apply the user's visual preference across the alternatives while varying their structure. For a popover or menu-only app, visualize its opened surface and entry point rather than inventing a permanent window. Before presenting, check that a first-time user can identify the main action, read realistic content and understand the result without your narration. Correct these issues without adding unrequested features.

## Interaction and states

Make the primary action demonstrable in all three: form validation and a local saved entry, command filtering and a simulated copy result, or adding a sample goal. Provide controls for the relevant empty/loading/failure states outside the frame when reproducing them would otherwise be awkward. Keep typed text visible on a simulated submission failure.

Label simulated outcomes so they cannot be mistaken for actual writes or connectivity. Use semantic labels, keyboard-operable controls, visible focus and readable contrast. Honor reduced-motion preferences when animating.

Show a short name and one sentence explaining each option's benefit and cost. Recommend one based on the user's workflow. Use the [bundled review bridge](design-review.md) to wrap the offline preview with A/B/C and “None of these” buttons that deliver a deliberate choice and optional feedback to the waiting agent. Keep these controls outside the app frames. Each review is tied to the exact preview and brief; start a new review after either changes. A selection is a design choice, not blanket permission to build. When localhost is unavailable, use a copyable summary received in conversation. JavaScript localStorage is not an approval channel.

## Render review

Use an available browser to check all three candidates at ordinary laptop viewport size and a narrow viewport. Exercise their main actions, keyboard navigation and relevant states. Review screenshots if the environment provides them. Fix overflow, obscured controls, unrealistic dimensions and cosmetic-only variations.

Codex Desktop may open the file in its panel or browser; Claude Code may open it with the platform browser. Use tools actually available. When you can only create/open the file, report that the render wasn't inspected and let the user inspect it before approval. A rendered HTML preview still cannot validate Spaces, Mission Control, native focus, menu bars or actual connectivity.

For a revised selection, update the selected candidate to reflect the final combination, including affected states, before the build agreement. Keep a stable option label or revision so approval refers to the actual design being built.
