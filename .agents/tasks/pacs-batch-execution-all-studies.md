---
title: PACS Batch All-Studies Download Execution
document_id: AGENT-TASK-PACS-BATCH-EXEC-002
version: 1.0
status: validated-published
language: en-US
last_updated: 2026-08-10
---

# Executable Task

## Task identity

**Task title:** `PACS Batch All-Studies Download Execution`

**Task path:** `.agents/tasks/pacs-batch-execution-all-studies.md`

**Task contract state:** `Validated/Published`

**Delivery objective / Work Package / MVP:** `PACS batch live execution`

**Owner / designated planning authority:** `User explicit authorization in conversation on 2026-08-10`

## Delivery context

The PACS batch automation tool has been implemented and verified with unit tests. This task governs the live execution run to discover all Chest DR studies on YiZhun AI-PACS, capture pre-report viewport PNG screenshots, download valid AI Image Report PDFs, use safe patient-name-based file names, and append structured records into `reports/manifest.jsonl`.

## Baseline and task revision

**Implementation baseline:** `8719bde2f91dbf8a709edbd94747ebc798032aa3`

**Task revision:** `resolved by the Git commit that publishes this task`

## Objective

**Objective:** Execute `python3 pacs_batch.py --all` using authorized local credentials to discover and download all Chest DR studies, saving one viewport screenshot PNG and one valid AI Image Report PDF per study into `reports/`, logging manifest records into `reports/manifest.jsonl` until all studies complete.

## Authoritative inputs

### Governing authority

- `docs/superpowers/specs/2026-08-10-pacs-batch-download-design.md`
- `docs/pacs-batch-requirements-and-architecture.md`
- User explicit request to run live batch download until all studies complete.

### Requirement traceability

- `PACS-BATCH-001` through `PACS-BATCH-006` → `docs/pacs-batch-requirements-and-architecture.md`

## Scope

### In scope

- Execute `python3 pacs_batch.py --all` (with `--retries 3` and `--timeout-ms 30000`).
- Process all discovered Chest DR studies until completion or explicit stopping criteria.
- Store outputs in `reports/` (`.png` screenshots, `.pdf` reports, `manifest.jsonl`).
- Preserve error diagnostics in `diagnostics/` on per-study retries.

### Out of scope

- Code modifications to `pacs_batch.py` or `test_pacs_batch.py`.
- PACS server-side modifications, patient data export outside local `reports/` folder, Git pushes, or remote deployments.

### Preserved behavior

- Existing discovery, direct viewer URLs, PDF binary validation, 3 retries per study, skipped existing valid outputs, and non-zero exit on unrecoverable study failures.
- Secret credentials must never be printed, logged, or committed.

## Dependencies and assumptions

### Dependencies

- Local Python 3.12, Playwright package, Chromium executable, network connectivity to PACS origin (`http://124.225.183.175:8361`), and local `credential.txt`.

### Approved assumptions

- `credential.txt` exists locally or is provided by the user with `AI_PACS_USERNAME` and `AI_PACS_PASSWORD`.
- PACS origin is reachable and list endpoint is accessible.

### Remaining approval requirements

- User must provide/verify `credential.txt` locally if not present.
- Deployment and remote release remain unauthorized (governed by separate Release Gate G10).

## Required capabilities

- Repository read/write, shell command execution, local Python execution, browser execution.

## Execution constraints

- Do not print or log passwords/credentials.
- Perform atomic saves (`.part` temporary files replaced on completion).
- Continue processing later studies if an individual study fails after retries.

## Acceptance criteria

- [ ] All Chest DR studies on PACS are discovered and processed.
- [ ] For each study, exactly one viewport screenshot (`.png`) and one report PDF (`.pdf`) are saved in `reports/` using safe patient-name filenames.
- [ ] `reports/manifest.jsonl` contains structured JSON records for all processed studies with status (`succeeded`, `skipped`, or `failed`).
- [ ] Complete run reports final discovered/completed/failed summary cleanly without credentials leakage.

## Verification requirements

### Required checks

- `python3 pacs_batch.py --probe-only`
- `python3 pacs_batch.py --all`
- `ls -la reports/`
- `wc -l reports/manifest.jsonl`

### Required evidence

- Output counts (discovered vs completed vs failed).
- Manifest file path and size.
- Exact non-credential console summary.

## Stop conditions

- `credential.txt` is missing or invalid.
- PACS origin is unreachable.
- Playwright or Chromium runtime fails to launch.
- Unrecoverable network or authentication error.

## Side-effect authorization

### Explicitly authorized side effects

- Execution of `pacs_batch.py --all` on authorized local machine.
- Local creation/writing of screenshot PNGs, report PDFs, and `manifest.jsonl` in `reports/`, and diagnostic files in `diagnostics/`.

Git commits, pushes, secret disclosure, remote deployments, or remote PACS data mutation remain unauthorized.

## Expected terminal outcome

### Review Required

The Executor completes the batch run, verifies `reports/` outputs and `manifest.jsonl`, and submits terminal evidence for Reviewer evaluation.
