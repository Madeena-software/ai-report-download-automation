# PACS Batch Requirements and Architecture

**Status:** Approved by the user on 2026-08-10

**Upstream product authority:** [PACS Batch Screenshot and Report Download Design](superpowers/specs/2026-08-10-pacs-batch-download-design.md), approved by the user on 2026-08-10.

## Requirements

| ID | Statement | Owner | Verification |
| --- | --- | --- | --- |
| PACS-BATCH-001 | The command discovers every study available through the authorized Chest DR list, retaining its `sid`, `aiCalcId`, and patient-name value when available. | `pacs_batch.py` | Authorized headed run reports the discovered count and manifest records. |
| PACS-BATCH-002 | The command opens each discovered study through its viewer URL without table-row clicking. | `PacsBrowser` | Focused URL-construction check and authorized headed run. |
| PACS-BATCH-003 | Before generating a report, the command stores exactly one screenshot of the visible viewer viewport for each completed study. | `PacsBrowser` | Authorized headed run produces one non-empty PNG per completed study. |
| PACS-BATCH-004 | The command generates and downloads the AI Image Report as a valid PDF for each completed study. | `PacsBrowser` | Authorized headed run produces one PDF with a valid header and EOF marker per completed study. |
| PACS-BATCH-005 | Output PNG and PDF filenames use a filesystem-safe patient-name prefix with `sid` and `aiCalcId` suffixes; identifier-only names are used when the patient name is unavailable. | `pacs_batch.py` | Offline filename tests cover normal, invalid, missing, and duplicate-name cases. |
| PACS-BATCH-006 | A failed study is retried three times, recorded in the manifest, and does not prevent later studies from running; credentials are never printed. | `pacs_batch.py` | Offline retry/manifest checks and authorized run evidence. |

## Architecture and boundaries

- Reuse the existing single-file Python and Playwright design. `PacsBrowser` owns browser interaction, `Study` carries identifiers and patient metadata, and `main` coordinates batch execution.
- The PACS list and viewer remain the source of truth. The script is a local read-and-download client; it must not export lists, modify PACS data, upload files, or change credentials.
- The local credential file and browser storage state are sensitive. The downloaded images, PDFs, manifest, and diagnostics remain on the authorized local machine and must not be written to logs.
- Patient-name prefixes are display metadata only. `sid` and `aiCalcId` remain the stable identity and collision guard.

## Delivery objective

Deliver the missing successful-study viewport PNG output and patient-name-based output naming while preserving existing direct viewer navigation, PDF validation, retry, and manifest behavior.

## Planning state

- Observed implementation: `pacs_batch.py` at `411f3ce147a4ebe9489d3fe4025d2069067b1395` is an unreviewed legacy implementation with no governing task or accepted-baseline record.
- Implementation baseline approved for first-task planning: `411f3ce147a4ebe9489d3fe4025d2069067b1395`. This records the starting implementation only; it is not acceptance, release approval, or execution authority.
- A Draft task and implementation plan may now be prepared. Execution remains blocked until the task has an immutable published revision and the applicable side-effect authority.
