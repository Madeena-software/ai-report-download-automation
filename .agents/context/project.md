---
title: Repository Context Template
document_id: AGENT-CONTEXT-001
version: 1.1
status: approved-template
language: en-US
last_updated: 2026-08-10
scope:
  - repository-level AI orientation
  - repository authority mapping
  - delivery-state orientation
  - scoped-context routing
authority_note: This file is supporting, refreshable repository context. Approved repository authority governs intended behavior. Observed repository evidence governs claims about current implementation reality. Neither silently overrides the other, and this context replaces neither.
---

# Repository Context

This file is the repository-level context entrypoint for AI-assisted software delivery.

It provides a verified orientation map of the repository, identifies where authoritative information lives, summarizes the current delivery state, and routes agents to additional scoped context when needed.

It is not a replacement for authoritative repository artifacts.

Keep this file concise enough to serve as an orientation layer. Prefer references to authoritative documents over duplicating their full contents.

## Repository identity

**Name:**  
`ai-report-download-automation`

**Repository type:**  
`application`

**Primary responsibility:**  
`Batch automation for downloading Chest DR AI image reports and viewport screenshots from YiZhun AI-PACS.`

## Purpose

Automate discovery, viewport screenshot capture, and AI image report PDF downloads for Chest DR studies on YiZhun AI-PACS using browser automation, structured patient-name-based file naming, and JSONL manifest tracking.

## Current repository state

**Current state:**  
`active development`

**Relevant summary:**  
`The PACS batch automation tool has implemented and verified full study discovery, patient-name-based safe file naming, non-scrolling viewport screenshot capture, PDF validation, error retries, and manifest tracking. All 11 unit tests pass.`

## Intended authority map

### Business sources and decisions

- `docs/superpowers/specs/2026-08-10-pacs-batch-download-design.md`

### Product / PRD authority

- `docs/superpowers/specs/2026-08-10-pacs-batch-download-design.md`

### Requirements and matrices

- `docs/pacs-batch-requirements-and-architecture.md`

### Architecture and repository policy

- `docs/pacs-batch-requirements-and-architecture.md`
- `.agents/AGENTS.md`

### Delivery planning

- `.agents/tasks/pacs-batch-screenshot-and-report-download.md`

### Release policy

- `.agents/software-workflow.md` (Section 20: Separate Release Gate)

## Observed implementation evidence map

### Source and configuration

- `pacs_batch.py`
- `.env`
- `credential.txt` (local non-committed)

### Data and migrations

- `reports/manifest.jsonl`
- `diagnostics/`

### Tests and verification

- `test_pacs_batch.py` (11 unit tests passing)
- `python3 pacs_batch.py --help`

### Version control and CI

- Git repository on branch `main` (`6c39e2c4a145e4a11b0ec573f96e66902f09a12c`)

### Runtime and operational evidence

- Local Python 3.12 + Playwright Chromium browser environment.

## Top-level architecture and boundaries

Monolithic Python CLI automation script (`pacs_batch.py`) utilizing Playwright for browser interactions against PACS web interface. Standard-library `unittest` suite (`test_pacs_batch.py`). Local file output for PDFs, PNG viewport screenshots, and JSONL manifests.

## Scoped context

None currently required beyond repository level.

## Delivery state

### Current delivery objective

`PACS batch output completion`

### Current Work Package / MVP / delivery slice

`PACS batch screenshot capture and report download`

### Quality-gate state

| Gate | Status | Evidence / authority |
|---|---|---|
| B0 — Business Framing | `passed` | `docs/superpowers/specs/2026-08-10-pacs-batch-download-design.md` |
| P1 — Product Definition | `passed` | `docs/superpowers/specs/2026-08-10-pacs-batch-download-design.md` |
| R2 — Requirements Traceability | `passed` | `docs/pacs-batch-requirements-and-architecture.md` |
| A3 — Architecture Clarity | `passed` | `docs/pacs-batch-requirements-and-architecture.md` |
| D4 — Delivery Readiness | `passed` | PACS batch screenshot and report download objective bounded |
| T5 — Task Readiness | `passed` | `.agents/tasks/pacs-batch-screenshot-and-report-download.md` @ `d2490677d839c7a2044a3948174517858a9f3a98` |
| E6 — Execution Verification | `passed` | 11 unit tests passed, CLI help verified, git diff check clean |
| V7 — Implementation Review | `passed` | Review verdict ACCEPTED for commit `6c39e2c4a145e4a11b0ec573f96e66902f09a12c` |
| R8 — Remediation Closure | `not_applicable` | No remediation required |
| A9 — Baseline Acceptance | `passed` | `6c39e2c4a145e4a11b0ec573f96e66902f09a12c` |
| G10 — Release Approval | `pending` | Separate Release Gate under `.agents/software-workflow.md` |

**Earliest unmet or materially unreliable gate:**  
`G10 — Release Approval (Separate Release Gate)`

### Active task(s)

- `.agents/tasks/pacs-batch-screenshot-and-report-download.md` @ `d2490677d839c7a2044a3948174517858a9f3a98` (Status: `Accepted`)

### Blocking items

- None.

## Accepted baseline

**Accepted baseline:**  
`6c39e2c4a145e4a11b0ec573f96e66902f09a12c`

**Accepted scope:**  
`PACS batch screenshot capture, safe patient-name-based file naming, PDF validation, JSONL manifest logging, and 11 unit tests.`

**Evidence reference:**  
`Unit tests passed (11/11), CLI verification passed, git diff check clean, review verdict ACCEPTED.`

## Known gaps and open decisions

### Blocking

- None.

### Non-blocking

- Production release/deployment approval remains open under separate Release Gate (G10).

## Repository conventions

- Python 3.12 with standard library + `playwright`.
- `pacs_batch.py` is the single CLI executable.
- `test_pacs_batch.py` contains unit tests runnable via `python3 -m unittest -v test_pacs_batch`.
- `reports/` directory stores PDFs, PNG screenshots, and `manifest.jsonl`.
- Credentials kept strictly local in `credential.txt` / `.env` and never logged or committed.

## Context verification

**Last verified:**  
`2026-08-10`

**Verified against repository revision:**  
`6c39e2c4a145e4a11b0ec573f96e66902f09a12c`

**Verified sources:**  
- `.agents/AGENTS.md`
- `.agents/software-workflow.md`
- `.agents/tasks/pacs-batch-screenshot-and-report-download.md`
- `pacs_batch.py`
- `test_pacs_batch.py`

**Known verification limitations:**  
- None known.
