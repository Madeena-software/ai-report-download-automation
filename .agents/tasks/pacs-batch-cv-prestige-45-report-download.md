---
title: CV Prestige 45-Study AI Report Download
document_id: AGENT-TASK-PACS-BATCH-CV-PRESTIGE-001
version: 1.0
status: validated-published
language: en-US
last_updated: 2026-09-01
---

# Executable Task

## Task identity

**Task title:** `CV Prestige 45-Study AI Report Download`

**Task path:** `.agents/tasks/pacs-batch-cv-prestige-45-report-download.md`

**Task contract state:** `Validated/Published`

**Delivery objective / Work Package / MVP:** `Targeted PACS report download`

**Owner / designated planning authority:** `Human authorization in the task-authoring handoff dated 2026-09-01`

## Delivery context

Download one valid AI Image Report PDF for exactly the 45 human-authorized CV
Prestige Chest DR studies. The target set is the private 45-MRN CV Prestige
target set supplied locally at execution time; it is not every Chest DR study
visible in PACS. This task uses the existing discovery, direct-viewer,
Generate Report, Image Report, PDF validation, retry, screenshot, and manifest
behavior in `pacs_batch.py`.

## Baseline and task revision

**Implementation baseline:** `21e062029e67f3ef7a59d01aecc11f042c2d68f6`

**Task revision:** `resolved by the Git commit that publishes this task`

The immutable governing task revision is the commit containing this exact task
content. Do not execute against a later task revision without republishing it.

## Objective

**Objective:** Reconcile the private authorized 45-MRN set against a private
PACS discovery, then download reports only for the resulting 45 explicit
`SID:AICALCID` selections into a private local operational workspace.

## Authoritative inputs

### Governing authority

- `docs/superpowers/specs/2026-08-10-pacs-batch-download-design.md`
- `docs/pacs-batch-requirements-and-architecture.md`
- Human authorization in the task-authoring handoff dated 2026-09-01

### Requirement traceability

- `PACS-BATCH-001` through `PACS-BATCH-006` → `docs/pacs-batch-requirements-and-architecture.md`
- Exact-target and privacy constraints → human authorization in the task-authoring handoff dated 2026-09-01

## Scope

### In scope

- Test reachability and authenticate with authorized local credentials.
- Discover Chest DR studies using the existing `--discover-only` mode.
- Reconcile `patientId` exactly against the private authorized 45-MRN target set.
- Run the existing downloader with exactly 45 explicit repeated `--study SID:AICALCID` selections.
- Save valid PDFs, supporting viewport screenshots, diagnostics, and JSONL
  manifest records in a private local workspace.
- Verify the exact target counts, mappings, outputs, and final statuses.

### Out of scope

- `python3 pacs_batch.py --all` or any broad/unfiltered study selection.
- Selecting by patient name or guessing an identity when `patientId` is absent.
- DICOM upload, PACS data mutation, account or credential changes, or any
  server-side action beyond the existing report-generation interaction.
- Repository implementation changes, repository output files, Google Drive
  publication, deployment, push, pull request, or issue writes.

### Preserved behavior

- Existing direct viewer navigation, report-generation flow, Image Report
  selection, PDF validation, retry behavior, screenshots, safe reruns, and
  manifest format.
- Credentials, browser state, patient material, and discovery data remain
  private and are never printed into shared logs or committed.

## Dependencies and assumptions

### Dependencies

- Current implementation at the stated baseline.
- Python 3.12, Playwright, a launchable Chromium runtime, network access to
  `http://124.225.183.175:8361`, and authorized local credentials.
- A human-authorized private target file outside Git containing exactly one
  MRN per line, for example:
  `/tmp/ai-pacs-cv-prestige-20260901/target/authorized-mrns.txt`.

### Approved assumptions

- `patientId` is the authoritative exact-match identity for this operation.
- The target file is human-authorized, private, contains exactly 45 unique
  non-empty MRNs, and is not copied into the repository.
- `--discover-only` output is treated as sensitive because it can include
  unrelated patients.

### Remaining approval requirements

- Confirm the private target file is human-authorized before execution.
- Keep any missing-target or ambiguity identities in the private workspace
  only; report only counts in shared execution evidence.
- No approval in this task authorizes DICOM upload, external publication,
  repository mutation, or release.

## Required capabilities

- Local repository read and command execution.
- Authorized PACS browser/network access and local credential access.
- Private local filesystem access for target, discovery, output, state, and
  diagnostics files.

## Execution constraints

- Use a private workspace outside the repository output tree, such as:

  ```text
  /tmp/ai-pacs-cv-prestige-20260901/
    target/authorized-mrns.txt
    discovery/raw.txt
    discovery/selected-studies.txt
    discovery/reconciliation-summary.json
    reports/pdf/
    reports/ss/
    reports/manifest.jsonl
    diagnostics/
    auth-state.json
  ```

- Protect target, credentials, browser state, discovery, reports, screenshots,
  and diagnostics with local filesystem permissions appropriate for patient
  data. Do not commit or upload them.
- Run `python3 pacs_batch.py --probe-only`, then `--discover-only` with its
  complete console output redirected to the private `discovery/raw.txt`.
  Do not paste or print the discovery dump into shared logs.
- Reconcile exact string `patientId` values only. Require all of the following
  before downloading: target count `45`, unique target count `45`, matched
  count `45`, missing count `0`, ambiguous count `0`, and exactly one unique
  `(sid, aiCalcId)` mapping for every target MRN.
- If a target MRN is missing, maps to multiple PACS studies, or lacks a usable
  `patientId`, stop before any report download. Keep identities private.
- Write the reconciled 45 `SID:AICALCID` values to the private selected-study
  file and invoke the existing CLI once with 45 repeated explicit `--study`
  arguments. Do not use `--all`; do not add patient names to process
  arguments; do not use `--overwrite` unless an authorized rerun explicitly
  requires replacing invalid outputs.
- Use explicit paths for `--output`, `--storage-state`, and `--diagnostics`.
  Retain the existing default retry behavior (`--retries 3`) and PDF
  validation behavior.
- Do not log credentials, full discovery output, real MRNs, patient names,
  report contents, screenshots, or private file contents in shared evidence.

## Acceptance criteria

- [ ] PACS origin is reachable and authentication succeeds without credential leakage.
- [ ] The private target set contains exactly 45 unique authorized MRNs.
- [ ] Discovery yields exactly one unambiguous `(sid, aiCalcId)` mapping for each target MRN: target `45`, matched `45`, missing `0`, ambiguous `0`.
- [ ] No unrelated study is selected; the download invocation contains exactly 45 explicit study mappings and does not use `--all`.
- [ ] Exactly 45 target report PDFs exist in the private output, each with a valid PDF header, existing EOF marker, non-truncated content, and existing non-empty supporting screenshot.
- [ ] The manifest's latest record for each of the 45 selected mappings identifies the intended target and has status `succeeded` or `skipped`; failed target count is `0`.
- [ ] The manifest provides complete target records and a rerun reuses valid existing outputs without uncontrolled duplicate files.
- [ ] No real patient identifier, patient name, report, screenshot, discovery dump, credential, or browser state is committed or externally published.
- [ ] No DICOM upload or PACS server-side mutation is performed.

## Verification requirements

### Required checks

- Record branch, HEAD, and status before execution; verify the implementation
  baseline matches this task.
- `python3 -m unittest -v test_pacs_batch`
- `python3 pacs_batch.py --help`
- `python3 pacs_batch.py --probe-only`
- Private discovery/reconciliation summary with target `45`, matched `45`,
  ambiguous `0`, and missing `0`.
- Exact selected-study argument count `45`, verified from the private mapping
  file and the actual invocation without exposing its values.
- Final private PDF count `45`, latest manifest target-record count `45`,
  failed target count `0`, per-file PDF validation, and output file sizes.

### Required evidence

The Executor must report only non-sensitive summaries: repository revision and
status, commands and observed results, target/matched/ambiguous/missing counts,
selected count, PDF count, manifest count, failed count, validation summary,
and private output paths. Do not return the raw discovery data, MRNs, patient
names, report content, screenshots, credentials, or browser state.

## Stop conditions

Stop before live download if credentials are unavailable or invalid, PACS is
unreachable, the browser cannot launch, discovery cannot expose `patientId`,
the target set is not exactly 45 unique MRNs, any target is missing or
ambiguous, safe exact selection cannot be established, the existing CLI cannot
run only the selected 45, the implementation baseline has materially drifted,
or DICOM upload/external mutation becomes necessary. A stop never authorizes
using `--all` or compensating with unrelated studies.

## Side-effect authorization

### Explicitly authorized side effects

- Authorized local PACS login, discovery, report generation, and report/PDF
  download for exactly the reconciled 45 studies.
- Local creation of the private target, discovery, report, screenshot,
  manifest, browser-state, and diagnostic files described above.

### Not authorized

- DICOM upload, unrelated patient processing, PACS data mutation, credential
  changes, external report publication, repository implementation changes,
  repository output mutation, GitHub remote mutation, deployment, or release.

## Expected terminal outcome

### Review Required

The Executor returns non-sensitive verification evidence and stops. A
Planner/Reviewer evaluates this exact published task revision and the private
execution evidence; task completion is not release authorization.

## Remediation — Blank Radiograph False-Positive Prevention

**Review basis:** `160b9d98fb9bf1f0c302403d62c034f87d0aac1b`

### Objective

A report MUST NOT return `succeeded` merely because the captured PDF is
structurally valid and larger than the current size threshold. Before clicking
Download Report, the automation MUST establish that the selected Image Report
contains an actually rendered radiograph. If readiness cannot be established,
the attempt MUST fail and use the existing retry and diagnostic mechanism.

### Required corrections

1. Image Report selection and readiness MUST fail closed. Failures to find or
   select Image Report, confirm the relevant report view, or establish
   radiograph render readiness MUST NOT be silently ignored.
2. Before download, require a visible radiograph canvas with meaningful
   dimensions; zero-size, hidden, placeholder-size, and uninitialized canvases
   MUST be rejected.
3. Before download, require conservative evidence of non-trivial rendered
   image content rather than a blank/default canvas. The detection method and
   threshold are Executor engineering decisions, MUST be supported by
   controlled valid-versus-blank evidence, and MUST document their rationale
   in implementation evidence. Arbitrary intuition-only thresholds are not
   sufficient.
4. Any readiness failure MUST raise into the existing retry path. Exhausted
   readiness failures MUST produce `failed`, never `succeeded`.
5. Preserve authentication, discovery, explicit target selection, Generate
   Report, Blob capture, PDF structural validation, atomic writes, manifest,
   screenshot/diagnostic behavior, and the targeted 45-study boundary. The
   >50 KB threshold MAY remain as a secondary sanity check, but MUST NOT be
   treated as evidence that the radiograph exists.

### Regression coverage

Automated coverage MUST prove that:

- a structurally valid PDF larger than 50 KB with a blank/unready radiograph
  is rejected and cannot return a successful report result;
- a valid rendered Image Report passes readiness and continues normal download;
- a temporary blank/unready render retries and may succeed on a later valid
  render;
- a persistently blank/unready render exhausts retries and is represented as
  `failed` in the manifest; and
- all existing non-remediation tests remain passing.

### Remediation implementation authorization

For the Blank Radiograph False-Positive Prevention remediation only, the
earlier task restrictions classifying repository implementation changes as out
of scope or not authorized are superseded to the minimum extent required to
implement and verify this remediation.

Authorized during the remediation implementation phase:

- bounded changes to `pacs_batch.py` necessary to make Image Report readiness
  fail closed;
- bounded changes to `test_pacs_batch.py` and directly related existing test
  fixtures/helpers necessary for regression coverage;
- local test and static-check execution;
- local diagnostics and fixtures that contain no real PHI; and
- one local implementation commit after successful verification, if otherwise
  permitted by repository workflow.

Preserve existing authentication, discovery, exact-target selection,
report-generation flow except for readiness validation, Blob capture, PDF
structural validation, retry/diagnostic behavior, manifest format, and privacy
boundaries.

Still NOT authorized during implementation:

- live PACS login or report rerun;
- Generate Report against real patients;
- real patient artifact download;
- Google Drive mutation;
- DICOM mutation or upload;
- MPIPS, date, or demographic remediation;
- unrelated refactoring;
- dependency installation unless separately approved;
- push, PR/issue mutation, deployment, or release.

The existing post-review two-case live PACS verification gate remains
unchanged and requires separate Planner/Reviewer authorization after
implementation review.

### Post-review real-PACS verification

Live PACS verification is deferred until implementation review accepts the
remediation. The later verification stage MUST first rerun only the two
previously confirmed blank-radiograph cases from private review evidence. For
each case, require a valid PDF, successful structural validation, and visual
evidence that the radiograph is present before accepting `succeeded`. If either
case still produces a blank radiograph, STOP and do not rerun all 45 studies.

Only after that two-case validation is accepted MAY a separately authorized
execution rerun or revalidate the complete 45-study target set. This task does
not automatically authorize that full-batch rerun.

### Additional acceptance criteria

- [ ] Image Report selection and readiness are fail closed.
- [ ] Blank or uninitialized radiograph canvases cannot reach `succeeded`.
- [ ] PDF byte size alone cannot establish report completeness.
- [ ] Non-trivial radiograph rendering is verified before download.
- [ ] Readiness failures use existing retry handling.
- [ ] Exhausted readiness failures produce `failed`.
- [ ] The >50 KB blank-report regression is rejected.
- [ ] A valid rendered-report regression passes.
- [ ] Existing report/PDF behavior remains compatible.
- [ ] No unrelated PACS, MPIPS, DICOM, demographic, date, or report-layout
  behavior is changed.

### Remediation verification requirements

Require current branch/HEAD/status, implementation diff inspection, focused
regression tests, `python3 -m unittest -v test_pacs_batch`, and the repository's
customary syntax/static checks, with exact observed results and no skipped
failing checks represented as PASS. Implementation MUST NOT begin if safe
radiograph detection requires a material architecture change, a new unjustified
heavy dependency, PACS server changes, or scope expansion into MPIPS/DICOM/date
remediation.
