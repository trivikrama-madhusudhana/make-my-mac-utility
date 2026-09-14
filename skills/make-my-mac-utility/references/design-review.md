# Browser choice delivery

Use the bundled Python standard-library helper to connect the three-option preview to the agent's active tool call. The user clicks **Choose A**, **Choose B**, **Choose C**, or **None of these** in a separate review bar below the preview. The buttons and receipt appear before the optional feedback field; enter any feedback before clicking a choice. The preview height is bounded so the choice controls stay visible on ordinary laptop screens, and the preview scrolls independently. Feedback is optional for every choice. Nothing is preselected. A receipt records a design direction and feedback; it does not grant blanket permission to build. None always returns to design consultation. If it has no feedback, ask what should change.

## Prepare and start

Keep `options.html` self-contained: inline CSS and scripts, inline SVG or data images, and local sample data. Label its three options A, B and C consistently. The helper shows this existing file inside a sandboxed iframe; the trusted selection controls live outside that iframe. Remote fonts, network calls, external scripts, file navigation and popups are intentionally unavailable in the preview. Generate a new HTML revision if the layout depends on those features.

Resolve the script relative to the installed skill directory. Example commands below use `SKILL_DIR` for that directory and `PROJECT_DIR` for the agreed project. Quote both paths. Create the project's `design` directory if needed. Every review round needs a fresh state path, even when an earlier server was stopped. Do not reuse, overwrite or delete a prior round to make a new review start.

```sh
python3 "$SKILL_DIR/scripts/design_review.py" serve \
  --html "$PROJECT_DIR/design/options.html" \
  --brief "$PROJECT_DIR/design/brief.md" \
  --state "$PROJECT_DIR/design/review-001.json" \
  --revision "Round 1"
```

`serve` prints one JSON line with the live `url`, `review_id`, and absolute HTML, brief and state paths, then stays running. It binds `127.0.0.1` to an OS-assigned port. Open the **complete URL**, including its `#token` fragment, in the browser on the same machine. The fragment is not sent in HTTP requests or passed into the preview. Treat the link and private state file as local credentials; do not publish them or commit the state file. The helper does not launch a browser or modify the HTML/brief.

Keep this server command alive using the host client's supported long-running execution. A yielded tool session is suitable; in a client with background shell jobs, use its background execution facility and retain the job handle. Do not assume a foreground command will survive a tool timeout or the agent turn ending. Use another tool call for waiting.

## Keep the current agent waiting

After showing the review link and explaining the options, run:

```sh
python3 "$SKILL_DIR/scripts/design_review.py" wait \
  --state "$PROJECT_DIR/design/review-001.json" --timeout 30
```

The wait returns structured JSON when a choice is saved, an input becomes stale, the server stops, or the bounded timeout expires. A saved result contains `choice`, `feedback`, review ID, revision, HTML/brief paths and SHA256 hashes, timestamp, and `build_authorized: false`. On retrieval, the waiting CLI acknowledges the receipt. Pending timeout is ordinary: issue another bounded wait while retaining the active turn. Do not end the turn with a final answer and assume the browser can wake it later.

- **Codex:** run `serve` through the execution tool with a short yield; retain the returned process/session handle. Run `wait` in a separate execution call. If that call yields, resume the actual returned execution handle until it completes, then inspect its JSON. Reissue `wait` on `pending`. A process session handle and a functions execution cell ID are different handles; use each only with its own tool. This requires no Codex-specific server code.
- **Claude Code:** start `serve` with the client's background execution facility. Run `wait` as a background Bash task if the client can notify the current session when that task finishes; inspect its output when notified. Otherwise use the same foreground bounded waits. Background-task notification is a client capability, not something this server promises to provide across ended sessions.

A server receipt is evidence that the browser submitted a choice to this local review. The UI separately reports whether a client is currently waiting and whether a client acknowledged retrieval. It never claims the agent has started a build. A closed, disconnected or ended client can retrieve a saved result later, but the server cannot restart or wake an ended agent session. An agent must not submit a selection through the HTTP API on the user's behalf to manufacture acceptance. Synthetic selections are appropriate only for clearly labeled disposable tests.

Before acting on the selection, inspect its revision and both hashes. `stale` blocks further use of that round: retain it as history and start a new review after finalizing updated HTML and brief. A previously saved selection is historical evidence, not approval of subsequently changed files. For A/B/C, carry feedback into the final agreement; resolve requested revisions and apply the skill's exact build agreement gate. For None, ask or use the provided feedback and produce revised choices. The helper intentionally never authorizes a build.

## Inspect, stop and recover

```sh
python3 "$SKILL_DIR/scripts/design_review.py" status --state "$PROJECT_DIR/design/review-001.json"
python3 "$SKILL_DIR/scripts/design_review.py" stop --state "$PROJECT_DIR/design/review-001.json"
```

Stop sends an authenticated local request; it never kills a PID from a file. Stop the server when this round has been consumed or abandoned. The state and receipt remain for replay; no input files are removed. `wait` also replays an existing selection immediately, including from disk when the server is unavailable. Offline replay rechecks both source hashes and reports changed or missing inputs as stale. Authentication failures are explicit errors, not an offline success. `connection: server_unavailable` means no live session was verified. A crash can leave `lifecycle: running` in the file: the connection field, rather than that historical value, tells whether the server answered.

A duplicate submission with identical choice and feedback returns the same receipt. A conflicting second submission is rejected and requires a new review. Changing either source file invalidates the round. The preview is the exact HTML snapshot read at startup; it is not silently refreshed when the source changes. The helper saves state atomically with mode 600 before acknowledging a selection. It accepts only the exact loopback Host and Origin, checks a session token and review ID, bounds request bodies and feedback, and exposes only the wrapper and its named `/preview` snapshot. The preview has an opaque sandbox origin and cannot read the parent's token, send selection requests, open windows or navigate the top-level page. These controls isolate generated preview content; they do not protect against a malicious process already running as the same OS user.

If Python, loopback networking, a persistent execution tool, or a same-machine browser is unavailable, use the manual fallback: open the HTML directly or deliver it as an artifact, explain A/B/C/None, and ask the user to reply in chat with a choice and optional feedback. Record that chat message as the evidence. Do not present a dead review link as an automatic delivery channel. A browser launch or unconfirmed click is not receipt evidence.

## Verification

From the repository root:

```sh
python3 -m unittest discover -s evaluation -p test_design_review.py -v
```

The tests use temporary fixtures and local ephemeral ports. They cover an active CLI waiter receiving a choice, replay after server stop, duplicate/conflicting submissions, None with and without feedback, source invalidation, token/Host/Origin checks, route and payload bounds, sandbox policy, private state, existing-file preservation, timeout without selection, authenticated cleanup, and a failed disk write without a false receipt. Separately inspect the real review in a browser: choose an option while an actual waiter is active, verify the receipt and waiter output, and exercise a disposable None round. Browser appearance and interaction are not established by the HTTP tests alone.

## Storage-sync failures

If writing fails before replacement, the previous receipt stays intact and the browser can retry. If directory sync fails after replacement, the new receipt already exists: the helper retains that choice, returns an error, and exposes `storage_warning` in live state. Only an identical choice may be retried; a successful write clears the warning. Do not describe a live warning as confirmed durable delivery. Acknowledgement failures also preserve the last state actually written rather than silently erasing a previous delivery timestamp.

Offline replay reports the receipt that is present on disk. It cannot reconstruct an interrupted server response or establish survival across power loss after a failed directory sync. `delivered_at` records the acknowledgement timestamp written by the helper, not proof that the agent completed downstream work. Design selection remains separate from build authorization.
