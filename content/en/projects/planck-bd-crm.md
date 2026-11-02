---
title: A CRM built with no engineers
subtitle: The web app that runs a start-up's business-development pipeline, built with AI coding assistants
period: Jun 2026 – present
year: 2026
role: Designer, builder and owner
org: Planck Technologies AS
tags: [Building with AI, Software, Business development]
featured: true
order: 1
status: In daily use
summary: Planck's commercial pipeline lived in a spreadsheet. I built the web application that replaced it, with Claude Code and no engineering resource. The team works from it every day.
art_caption: "A schematic of the pipeline board: companies move through stages, each with a fit score, and a status line confirms every save. No real data."
---
## The problem

Planck Technologies is a Norwegian deep-tech start-up that applies AI to materials design for CO₂ capture. Its engineers build the materials-discovery platform, which is the product. Nobody was free to build internal tools, and the commercial pipeline lived in spreadsheets that drifted out of date the moment two people edited them.

## What I built

An internal CRM for the client pipeline, and later a second one for investors. Companies enter through a fit score, move through stages, carry contacts, notes and an activity log, and feed dashboard, pipeline, outreach and reporting views. The weekly report to management comes straight out of it. Scale: 500+ organisations screened, about 60 in active follow-up.

## How it works

The architecture is unusual, and deliberately so.

- A React app written as a single JSX file, compiled by a Python script into one standalone HTML file. No Node, no npm, no server. People open it by double-clicking.
- State lives in the browser. For the team, one shared JSON file sits in a folder OneDrive already syncs, and each browser reads and writes it through the File System Access API.
- Merging is per record and per field. Every record carries a timestamp and who wrote it, so if I change a prospect's stage while a colleague changes its owner, both edits survive. Deletes leave a tombstone, so a record deleted on one machine isn't resurrected by the next sync.
- Companies are scored out of 100 across eight weighted criteria (use-case fit, urgency, warmth, decision speed, revenue potential, proximity, partner complementarity, build-versus-buy risk), with a cut-off for entering the catalogue. The weights are judgement, not fitted to outcomes, because there weren't yet enough closed outcomes to fit anything to. I'd rather say that than defend them.

The trade-off: nothing to provision, secure or pay for, and a non-engineer can ship and maintain it alone. The costs: a few seconds of compile on first load, a file-sync product used as a database, and no real authentication. Right for a team of two. It starts to bite at six.

## What went wrong

The expensive bug wasn't a crash. For a while, a failed save looked exactly like a successful one, and the work was simply gone on the next reload. The fix was not clever: a status line that says *All changes saved* or *Saving…*, and a red banner across the top when a write fails. Never let a failure path look like a success path.

A smaller one: dates built in UTC slid back a day in Norwegian summer time. Every date helper now works in local time.

## How I work on it

Specify before prompting. Back up before changing, with timestamped snapshots. Rebuild, run a parse check, then use it and see what is actually wrong. The assistant writes most of the code. I decide the structure, read it, test it and answer for it.

## What I'd change next

Split the single 7,500-line file into modules so someone else can contribute. Precompile instead of compiling in the browser. Replace file sync with a proper backend. And add real identity before people I haven't met start editing shared state.

*The app is internal, so there is no public link, and I don't share pipeline contents or commercial relationships.*
