---
title: PACS Batch Screenshot and Report Download
document_id: AGENT-TASK-PACS-BATCH-001
version: 0.1
status: validated-published
language: en-US
last_updated: 2026-08-10
---

# Executable Task

## Task identity

**Task title:** `PACS Batch Screenshot and Report Download`

**Task path:** `.agents/tasks/pacs-batch-screenshot-and-report-download.md`

**Task contract state:** `Validated/Published`

**Delivery objective / Work Package / MVP:** `PACS batch output completion`

**Owner / designated planning authority:** `User approval in this conversation on 2026-08-10`

## Delivery context

The existing authorized PACS batch script downloads AI Image Report PDFs but does not retain the normal pre-report viewport screenshot or patient-name-based output filenames. This task adds those bounded local output behaviors for every selected Chest DR study.

## Baseline and task revision

**Implementation baseline:** `411f3ce147a4ebe9489d3fe4025d2069067b1395`

**Task revision:** `resolved by the Git commit that publishes this task`

The immutable governing task revision is the Git commit that publishes this exact task content.

## Objective

**Objective:** Process all authorized Chest DR studies through the existing direct viewer flow, saving one viewer-viewport PNG before report generation and one valid AI Image Report PDF per completed study using safe patient-name-based filenames.

## Authoritative inputs

### Governing authority

- `docs/superpowers/specs/2026-08-10-pacs-batch-download-design.md`, approved by the user on 2026-08-10.
- `docs/pacs-batch-requirements-and-architecture.md`, approved by the user on 2026-08-10.
- User authorization in this conversation to automate the PACS account and retain patient-identifiable local PNG/PDF outputs.

### Requirement traceability

- `PACS-BATCH-001` through `PACS-BATCH-006` → `docs/pacs-batch-requirements-and-architecture.md`.

## Scope

### In scope

- Add one non-scrolling viewport PNG before **Generate Report** after each direct viewer opens.
- Use a shared safe filename stem based on patient name plus `sid` and `aiCalcId`; retain identifier-only fallback when the name is unavailable.
- Include screenshot output in the JSONL manifest and preserve valid paired-output skips.
- Add standard-library offline regression tests and run an authorized headed one-study check before the all-studies run.

### Out of scope

- Table-row clicking, list export, PACS data/report changes, uploads, credential/account changes, deployment, release, and unrelated refactors.

### Preserved behavior

- Existing discovery, direct viewer URLs, PDF validation, three retries, diagnostics on failure, later-study continuation, and non-zero exit after failures.
- Credentials and sensitive local output must not be printed.

## Dependencies and assumptions

### Dependencies

- Existing local Python 3.12, Playwright package, compatible Chromium runtime, authorized PACS network access, and `credential.txt`.

### Approved assumptions

- The current list discovery yields `sid`, `aiCalcId`, and patient name where supplied by PACS.
- Patient name is display metadata; `sid` and `aiCalcId` are the stable collision guard.

### Remaining approval requirements

- A Planner must publish this exact task at an immutable revision before execution.
- A designated user must authorize any Git commit used to publish this task.
- Dependency installation, secret disclosure, uploads, deployment, release, and PACS behavior beyond the local authorized read/generate/download flow are not authorized.

## Required capabilities

- Repository read/write, shell commands, Python test execution, Codebase Memory MCP, and local browser/PACS access for the authorized runtime check.

## Execution constraints

- Modify the existing `pacs_batch.py`; use Python standard-library `unittest` for new offline coverage.
- Do not add dependencies or a new framework.
- Keep one screenshot filename and one PDF filename per completed study; screenshot with `full_page=False` before the report click.
- Keep patient-identifiable data and browser state on the authorized local machine and out of console output.

## Acceptance criteria

- [ ] All discovered Chest DR studies retain `sid`, `aiCalcId`, and patient name when PACS provides it.
- [ ] A completed study yields exactly one non-empty viewport PNG before **Generate Report** and one valid AI Image Report PDF.
- [ ] PNG and PDF names use safe patient-name prefixes plus stable identifier suffixes, with identifier-only fallback and no duplicate-name overwrite.
- [ ] Manifest records study metadata, status, PDF output, screenshot output, attempts, and errors; failures continue later studies and produce a non-zero overall exit.
- [ ] Focused offline tests and an authorized headed one-study browser run provide observed evidence without logging credentials.

## Verification requirements

### Required checks

- `python3 -m unittest -v test_pacs_batch`
- `python3 pacs_batch.py --help`
- `git diff --check`
- Authorized headed one-study command, then authorized all-studies command only if the one-study command succeeds.

### Required evidence

The Executor must report the exact working-tree state, all commands and observed results, tests changed, one-study and all-studies discovered/completed/failed counts, local artifact existence, known gaps, and any blocker. Local checks must not be described as CI; no credentials or patient material may be copied into logs.

## Stop conditions

- Playwright or Chromium is unavailable and would need installation.
- PACS authentication, selector, viewer-readiness, or report-download behavior requires a new product, privacy, security, or architectural decision.
- A required output cannot be produced with the approved direct viewer flow, or a change would expand into list export, PACS mutation, upload, account change, deployment, or release.
- The implementation baseline or immutable task revision no longer matches this task.

## Side-effect authorization

### Explicitly authorized side effects

- After publication, local source/test edits and local test execution within scope.
- After publication, the authorized PACS account's local browser read, report generation, and local PNG/PDF download flow described above.

Git commits, pushes, dependency installation, secret disclosure, uploads, deployments, releases, and PACS data/account mutation remain unauthorized.

## Expected terminal outcome

### Review Required

The Executor returns a reviewable working-tree state with the required evidence. A Reviewer evaluates it against this task's published immutable revision and does not treat local execution as release authorization.
