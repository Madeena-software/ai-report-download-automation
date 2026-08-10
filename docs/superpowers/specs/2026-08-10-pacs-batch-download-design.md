# PACS Batch Screenshot and Report Download Design

**Status:** Approved by the user on 2026-08-10

**Source:** User direction in this conversation on 2026-08-10.

## Goal

Run a local Python command that processes every Chest DR study available to the authorized PACS account, saving one viewer viewport screenshot and one AI Image Report PDF for each study.

## Scope

1. Read PACS credentials from a local env-style credential file.
2. Authenticate, load the Chest DR user list, and discover the `sid`, `aiCalcId`, and patient-name value for each study.
3. Navigate directly to each study's viewer URL rather than clicking table rows.
4. After the viewer is ready and before selecting **Generate Report**, save one viewport screenshot that includes the visible PACS viewer UI.
5. Select **Generate Report**, use the AI Image Report, and download the resulting PDF.
6. Save the PNG and PDF with a filesystem-safe patient-name prefix and stable identifiers, for example:

   ```text
   02-WCI-02B_Thorax_PA__sid-33__ai-48.png
   02-WCI-02B_Thorax_PA__sid-33__ai-48.pdf
   ```

7. Record every result in a JSONL manifest so successes, skips, and failures are auditable.

## Constraints and safeguards

- Preserve the existing Playwright-based script; do not introduce an API integration or another framework.
- Never log the password. Keep the saved browser login state and downloaded patient material local.
- Sanitize the patient-name portion of filenames. If it is unavailable, use the existing stable identifier-only filename.
- Keep the `sid` and `aiCalcId` suffixes to avoid silently overwriting duplicate patient names.
- Retry a failed study three times, retain a diagnostic screenshot, continue processing later studies, and exit non-zero when any study fails.

## Acceptance criteria

- The all-studies command discovers all studies reachable from the Chest DR list for the authorized account.
- Each completed study produces exactly one viewport PNG before report generation and one valid PDF downloaded through the report dialog.
- Each successful pair uses the patient-name-based filename pattern above, with safe fallback and no name collision overwrite.
- The manifest identifies the study, patient name when available, outputs, attempt count, and final status.
- The command never prints PACS credentials.

## Verification

- Run focused, offline checks for URL construction, study metadata extraction, filename generation, and PDF validation.
- Run an authorized headed browser check for one study to confirm the viewer screenshot and report download sequence.
- Run the all-studies command only after the one-study check succeeds; report the observed manifest and any failures truthfully.

## Out of scope

- Clicking every table row instead of direct viewer navigation.
- Exporting the user list, altering PACS studies or reports, uploading files, deployment, or release.
- Changing PACS credentials or account permissions.
