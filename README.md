# hackager — hackathon manager

A readiness board for a folder of hackathon projects, plus the commands to
take one project from nothing to submittable: scaffold, fix, pitch, slides,
PDF, and a fetcher for the hackathon's own rules pages. Two commands wrap an
LLM (Claude Sonnet, headless, confirmed before spending); everything else is
free and deterministic.

The project is the unit of submission, so **every output lands in the
project's own `docs/`** — never under this folder. This folder holds the tool,
`BOARD.md`, `rules/` (hand-written notes on specific hackathons), and
`prompts/` (gitignored internals: the exact prompt sent and the raw reply).

## For an LLM (or anyone) driving it

```
hackager doctor               preflight: every dependency, what it blocks, how to fix it
hackager schema --json        the contract: every command, what it writes, what it costs
hackager next <proj>          the ONE next command for this project, and why (--json)
```

Run `doctor` first. Every check in it exists because that thing actually broke
during this tool's own development — pip refusing system Python (PEP 668), no
PDF engine on the machine at all, `vhs` needing ffmpeg and ttyd — and each
failure reports what it blocks and the command that fixes it. Found here it
costs nothing; found mid-workflow it costs the LLM steps already paid for.

`next` is a state machine over the project's files. Run what it prints, run
`next` again. It stops with `needs_human: true` at the things no tool can
produce — the hackathon URL, owning the idea, the demo video, the final form.
Exit `2` everywhere means a valid "no" (cancelled, nothing to do, done); `1`
is an error. Proven on a real Devpost entry: `fetch --follow → rules → verify
→ review → pitch → submission → slides → pdf → commit → publish` with no
hand-edits in between.

## Commands

```
hackager scan    <dir>      discover projects, extract signals (--json)
hackager report  <dir>      readiness board, one line per project
hackager check   <dir>      exit 1 if any project is not submission-ready (CI)
hackager board   <dir>      regenerate BOARD.md (--stdout to print)

hackager new     <name>     git init, LICENSE, README, hackathon.json, docs/PITCH.md
hackager init    <proj>     hackathon.json only, source/demo auto-detected
hackager fix     <proj>     add only what is mechanically safe and missing
hackager set     <proj> k=v manifest fields: one_liner problem market track event demo …

hackager fetch   <url> <proj> [--follow]   -> docs/reference/*.html + .txt
                                              --follow also grabs rules/terms/dates/faq pages
hackager read    <proj> [page]             print a fetched page as text
hackager rules   <proj>     LLM  -> docs/RULES.md      the event's rules, distilled, quoted
hackager ideas   <proj>     LLM  -> docs/IDEAS.md      5 candidate ideas; the tool does not rank them
hackager pick    <proj> <n> copies one idea into the manifest (no n: lists them)
hackager brief   <proj>     LLM  -> docs/BRIEF.md      build spec for the idea you picked
hackager build   <proj>     LLM  (opus) builds from BRIEF.md, unattended, --budget/--max-turns
hackager verify  <proj>     free  runs the project's own build/tests/lint/typecheck
                            gates -- npm scripts, or pyproject's [tool.ruff]/[tool.mypy]
hackager review  <proj>     LLM  -> docs/REVIEW.md     judged against RULES.md, with evidence
hackager pitch   <proj>     LLM  -> docs/PITCH.md      (docs/PITCH.draft.md if one is filled in)
hackager submission <proj>  LLM  -> docs/SUBMISSION.md the platform's form, field by field
hackager learn   <proj>     LLM  -> docs/INSIGHTS.md   how the git history says it was built
hackager demo    <proj>     LLM writes docs/demo.tape from the project's REAL commands,
                            then vhs renders docs/media/demo.mp4 + .gif (rendering is free)
hackager narrate <proj>     LLM -> docs/NARRATION.md  spoken script, cued to the tape's
                            own arithmetic timings (not guessed)
hackager slides  <proj>     free -> docs/<name>.pptx   one slide per ## in PITCH.md
hackager pdf     <proj|md>  free -> PITCH.pdf beside the markdown; --slides -> docs/<name>-slides.pdf
                            (16:9, one page per ##, images, ::stamp WORD and ::cat mood directives)
hackager rehearse <proj>    free  say the pitch out loud, timed, with a judge drill -> docs/REHEARSAL.md
                            fails if the first 30 s mention a screen or a tool; next gates on it
hackager judges  <proj>     the panel as data (--add 'Name | Role | lens') -> docs/reference/judges.json
hackager archive <proj> <label>  snapshot every out/ as evidence -> runs/NN-<date>-<label>/
hackager commit  <proj> [-m] git add -A && commit (exit 2 if clean)
hackager publish <proj>     gh repo create + push, confirms first; fills manifest source
hackager deploy  <proj>     runs the project's OWN deploy script; records the URL it prints
hackager score   <proj>     runs the project's OWN grader against submission.json
```

All LLM commands run `claude -p` with **no tools and no MCP servers** (a
document generator has no business holding a Gmail connector), ask
`proceed? [y/N]` before spending, and refuse to save a reply that does not
have the shape of the document asked for. `build` is the exception: Opus,
Read/Edit/Write/Bash allowed *inside the project directory only*, hard
dollar and turn caps passed to claude itself, and it refuses to start on a
dirty tree so its commits are attributable.

## What the Hackerdorm loss taught the tool

A finished, working entry did not place; the judges asked "tell us more about the problem". The
pitch had opened on the mechanism. So the tool now encodes the lesson instead of relying on memory:

- `pitch` writes a problem-first card (the person, the loss with a number, why now) and puts its
  coaching in `docs/PITCH.notes.md`, never on a slide; `next` refuses to advance a card whose
  slide 2 is not about who hurts or whose first two slides name the machinery.
- `rehearse` makes someone say it out loud, timed, before `publish`; `next` gates on a rehearsal
  newer than the script with the verdict `ready`.
- `deadline` is a manifest field with a timezone; `next` prints time left first, red under two
  hours, because the agent driving the tool misread the clock for hours that night.
- `judges` records the panel; `pitch` and `rehearse` read it.
- `rules` reads PDFs and screenshots in `docs/reference/`; `archive` keeps an agent run's `out/` as
  numbered evidence; `commit` warns when untracked files look like an agent's scratch.

## Choosing what to build

`ideas` reads the distilled rules and proposes **five** genuinely different
mechanisms — not five skins on one idea. Each carries the hardest technical
part, why a judge would call it creative rather than obvious (quoting the
rules' own wording), and **one honest reason not to pick it**. Risk is spread
deliberately: at least one certain to finish, at least one that might not.

It does not rank them and does not argue for one. `pick <n>` copies the chosen
idea into the manifest — which removes the last place the "strictly hackager"
workflow silently needed a text editor, since the alternative was retyping a
json block out of a doc by hand.

This replaced `brief` proposing a single idea. One suggestion invites a rubber
stamp; five force a choice. That matters legally, not just editorially — Sime
Darby's terms vest IP in the sponsor on creation and most events require the
submission to be the entrant's own work, so `next` marks this step
`needs_human` and stops.

## What "submission-ready" means

Six gates, all derived from the project itself, none from a manifest field
you could just type in: a `README.md` with a one-liner, a submission doc
(`PITCH.md`/`SUBMISSION.md`/… in root or `docs/`), a demo link, a LICENSE,
source (a `source` URL or a git remote), and a clean git tree. `check` fails
if any project misses one.

"Clean" is opinionated: a fresh `pitch` or `pdf` dirties the tree until you
commit it. That is the point — an uncommitted deliverable is not submitted.

## LLM wrapper

```
hackager pitch ~/Projects/Hackathon/TenTen-Tencent
hackager learn ~/Projects/Hackathon/TenTen-Tencent --model opus
hackager pitch <proj> -y        # skip the confirm (scripts only; real cost)
```

Runs `claude -p --model sonnet --output-format json` with the project as cwd,
prints `proceed? [y/N]` with the exact destination first, and prints the cost
after. `pitch` overwrites `docs/PITCH.md` only while it is still the blank
skeleton `new`/`fix` wrote; once a human has edited it, the draft goes to
`docs/PITCH.draft.md` beside it and you merge.

## Business manifest — `hackathon.json`

```json
{
  "name": "sidecar",
  "one_liner": "",
  "problem": "",
  "market": "",
  "track": "agent",
  "source": "https://github.com/you/repo",
  "demo": "https://youtu.be/...",
  "status": "draft"
}
```

`report`/`board` merge these fields; the pitch prompt embeds them.

## The demo video

Pattern taken from `Xendit/docs`, which does it properly. `demo` writes a
[VHS](https://github.com/charmbracelet/vhs) tape and renders it: the tape runs
the project's **real** commands in a headless terminal, so re-rendering can
never drift from what the code does — unlike a screen capture, which has to be
re-shot by hand every time the code changes. The tape is tracked; the render is
gitignored (`docs/media/.gitignore` is written for you) because the video
belongs on YouTube, not in a repo someone has to clone.

Needs `brew install vhs` (pulls ffmpeg + ttyd). Two honest limits:

- **A terminal recording is only the demo if the project runs in a terminal.**
  `demo` warns when the project mentions Fire TV, Ring, a mobile or browser
  target — for those, rules asking for footage "on the device for which it was
  built" are not satisfied by an asciicast, and shipping one looks finished
  while failing the requirement.
- **Check the result before submitting.** A tape that recorded an error, an
  expired credential or an empty balance renders just as happily as one that
  worked. `demo` therefore also writes `docs/media/demo-contact.jpg` — nine
  frames sampled across the video and tiled into one image, with their
  timestamps printed — an idea taken from `umcares/inspect.py`, whose point is
  that contact sheets exist "so a vision-capable model can literally look at
  the footage". That matters here: "watch the video" is an instruction an LLM
  driving this tool cannot follow, and it was the last step of the workflow.
  It paid for itself on the first run — the sheet caught ShelfLife's tape
  ending on `ls: shelflife.db: No such file or directory`, which a frame-by-
  frame spot check had missed.

`narrate` then writes the spoken script. Its cue times are computed from the
tape's own `Sleep` and `TypingSpeed` values — arithmetic, not an LLM guess — so
they match the file that actually gets rendered.

## Deployment

The `demo` gate takes a URL, and there are two kinds. A CLI or a server gets a
video (above). A deployable web app gets a link a judge can open, and `next`
now tells them apart by asking the project instead of assuming: if it has a
`deploy` script, or a `wrangler`/`vercel` config, its demo is a deployment.

`deploy` reimplements no platform. It runs **the project's own deploy script**
— the same principle as `verify` running the project's own tests — and reads
the URL out of what that command printed. If no URL appears in the output it
says so and stops, rather than composing one from a project name and a guessed
domain. It confirms first: this is outward-facing and spends your account's
quota, not a model's tokens.

It refuses, with exit 2, when nothing in the project says how it is meant to
be deployed. That is the honest answer for most entries — across eleven real
projects here, four are deployable and seven want a video.

## Slides / PDF

`slides` needs the venv: `python3 -m venv .venv && .venv/bin/pip install
python-pptx weasyprint` (system Python refuses per PEP 668). It builds a 16:9
deck from the project's `docs/PITCH.md` and always runs a dense-slide review
(>60 words) on the result. `pdf` is `pandoc --pdf-engine weasyprint`.

## panvim

`ln -s …/hackathon-manager/hackager ~/.local/bin/hackager`; one popup,
`hackager`, is registered in `~/.config/panvim/popups.conf` — the board as a
live nvim buffer refreshed every 5 min. Global keys `r c b n`; row keys
`p l v f s d F` act on the project under the cursor. Config in
`~/.config/panvim/hackager/{keys,syntax}.tsv`.
