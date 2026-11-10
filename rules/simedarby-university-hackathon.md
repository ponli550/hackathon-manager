# Sime Darby Property University Hackathon -- "Township of Tomorrow"

Sources (all fetched 2026-09-15, real HTTP GETs via `hackager fetch`, no
scraping stack -- all three are plain static pages except where noted; the
raw HTML lives in ../../SimeDarby/docs/reference/, with the entry it is for):
- /universityhackathon/ -- 137,941 bytes (landing page: theme, timeline,
  prizes, FAQ)
- /universityhackathon/register -- 20,692 bytes (registration; its actual
  FORM is client-rendered JS, see note below -- the surrounding copy is not)
- /universityhackathon/terms-and-conditions -- 196,466 bytes (full legal
  terms; this is where the IP-assignment clause lives, not on the landing page)

Extracted verbatim/paraphrased from the live pages -- not filled in from
assumption. Re-fetch and diff before relying on this close to any deadline;
pages, and terms, change (the T&Cs themselves reserve SDP's right to amend
at any time, clause 1.6).

## Theme
"How might we reimagine the Township of Tomorrow where people, businesses and
nature thrive together through innovation, technology and sustainable living?"

Two tracks -- **pick exactly one**, submitting the same idea to both is
grounds for disqualification on repeat:

- **People** -- community wellbeing, safety & security, accessibility &
  inclusion, mobility, digital living, feeling connected, healthy lifestyles.
- **Planet** -- waste management, circular economy, energy efficiency, water
  conservation, green transport, biodiversity, climate resilience.

## Eligibility
University students in Malaysia (citizens, PR, work visa, or student visa --
currently based in Malaysia). Any discipline. Teams of **3-5**, one team
leader submits on behalf of the team; every member must accept the team
invite before the submission finalizes. No fee.

## Timeline (2026)
| phase | date |
|---|---|
| Official launch | 11 September |
| Registration | 11 September -- 8 October |
| Challenge briefing | 9 October |
| **Proposal submission** | **23 October** |
| Judging rounds | 24-28 October |
| Top 10 announced | 28 October |
| Mentoring sprint | 2-6 November |
| **Final submission** | **11 November** |
| Grand finale | 14 November |
| Innovation Day | December |

## Prizes
Champion RM6,000 -- 1st runner-up RM3,000 -- 2nd runner-up RM1,500 --
consolation (4th-10th) RM500 each. Plus: an internship path, mentorship, and
consideration for SDP's Management Associate Programme.

## Submission format -- the two-part pitch
Not the generic pitch card shape `hackager pitch` currently produces
(one-liner/problem/why-not-a-wrapper/market/open-source/demo-script). This
hackathon asks for exactly two sections:

- **Mechanism** -- what the solution is, how it works, who benefits, why it
  creates value for the township.
- **Enabler** -- how technology enables the solution, enhances the user
  experience, and supports implementation at township scale.

Prototype must be a working, demoable thing -- at least one team member must
be able to code. Examples given: mobile/web app, AI assistant, smart
device/IoT, dashboard, service prototype, physical model, smart
infrastructure, digital experience.

## Intellectual property -- read before deciding what to submit
Fetched separately from /universityhackathon/terms-and-conditions (196,466
bytes, real static legal text, not JS-rendered -- unlike the register page,
see note below). Clause 11.1, verified against the raw fetched HTML directly
(not just the earlier summary): IP in any Participant Submission or Developed
IP "shall automatically and immediately vest in SDP upon creation" --
ownership passes the moment it exists, not on submission. 11.2 is a fallback
assignment for anything that does not auto-vest by operation of law, and 11.3
spells that assignment out as **perpetual, worldwide, irrevocable,
royalty-free, fully transferable, sublicensable**. No royalty, revenue share, or compensation
beyond whatever prize is awarded (11.5). SDP may use, modify, commercialise,
or combine it with anything else, without further consent (11.4). Moral
rights are waived. Clause 8: anything SDP provides (challenge statements,
datasets, branding) stays SDP's -- that direction was already expected;
Clause 11 is the one that matters for what a team decides to build and how
much of their own prior/independent work ("Background IP", explicitly
carved out and NOT assigned) they fold into the submission.

Practical read: treat what you submit as something you are giving away
outright, not licensing. Keep genuinely proprietary or reusable-elsewhere
work out of the Programme Submission itself, or accept that SDP owns it
after.

## Eligibility, beyond the FAQ summary
- Participants under 18 need a parent/guardian's prior written consent, on
  request (3.6) -- the landing page's FAQ doesn't mention a minimum age at
  all.
- SDP can verify eligibility at any time and request supporting documents;
  registering confers no right to progress, be shortlisted, or receive
  anything (3.9-3.11). Its eligibility decisions are final, "no
  correspondence entertained."

## Registration form -- a real limitation, not filled in
/universityhackathon/register was fetched too (20,692 bytes) but its actual
form fields are rendered client-side (a Next.js component, no embedded
__NEXT_DATA__ in the static HTML) -- a plain GET genuinely cannot see them.
The FAQ's own description (full team roster, contact details, a short
introduction, one track selection, each member accepting an invite) is the
most complete picture available without running an actual browser.

## Judging criteria
Innovation and original thinking; business viability; technical execution of
the prototype; how directly it addresses the theme.

## Why this is stored separately, not wired into readiness/pitch defaults
The six projects hackager is currently tracking (DeepTech/Maid, LabHack/
FinVerify, VeriPay, XYZ/Sidecar, Xendit/Consent Vault, Docs-of-Agents) have no
relation to townships or sustainability -- they read as a different
hackathon's submissions (agent tooling, fintech, health). Overwriting TRACKS
or the pitch template to match Sime Darby's People/Planet tracks and
Mechanism/Enabler structure would misconfigure the tool for the real work it
is already managing. If a project IS being built for this specific
hackathon, its own hackathon.json can carry `"track": "People"` or
`"Planet"` (TRACKS would need those two options added), and its pitch card
should be hand-written or drafted to the Mechanism/Enabler shape above rather
than `hackager pitch`'s current generic one.
