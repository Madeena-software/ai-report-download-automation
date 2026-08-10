# PACS Batch Screenshot and Report Download Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add one pre-report viewer-viewport PNG and patient-name-based PNG/PDF names to every successful Chest DR batch download.

**Architecture:** Keep the existing single-file Playwright flow. Split the current viewer navigation from report clicking so the viewport can be captured after the viewer is ready but before **Generate Report**; derive both filenames from one safe study stem and retain the existing PDF validation, retry, diagnostics, and JSONL manifest.

**Tech Stack:** Python 3.12 standard library, existing Playwright runtime, `unittest`.

## Global Constraints

- Implementation baseline: `411f3ce147a4ebe9489d3fe4025d2069067b1395`.
- Reuse `pacs_batch.py`; do not add a framework, API integration, or dependency.
- Process all discovered Chest DR studies by direct viewer URL; do not click list rows or export the list.
- Capture exactly one visible viewport PNG before **Generate Report** for each completed study.
- Name both outputs `<safe-patient-name>__sid-<sid>__ai-<aiCalcId>.<ext>`; retain `CR-<sid>-AI-<aiCalcId>` when the patient name is absent.
- Keep credentials, browser state, outputs, and diagnostics local. Never print credentials.
- Preserve three retries, later-study continuation, PDF validation, and non-zero exit after failures.
- Do not install dependencies, commit, push, deploy, or access PACS until separately authorized by the governing published task.

## File Structure

- Modify: `pacs_batch.py` — shared output naming, viewer readiness/navigation, viewport capture, retry/skip/manifest integration.
- Create: `test_pacs_batch.py` — stdlib-only offline tests using a fake Playwright page/browser.
- Modify: `docs/pacs-batch-requirements-and-architecture.md` only if execution evidence reveals an approved-authority discrepancy; otherwise leave it unchanged.

---

### Task 1: Define and verify output names

**Files:**
- Create: `test_pacs_batch.py`
- Modify: `pacs_batch.py:255-262`

**Interfaces:**
- Consumes: `Study(sid: int, ai_calc_id: int, patient_id: str = "", patient_name: str = "")` and `safe_filename(value: str) -> str`.
- Produces: `study_output_stem(study: Study) -> str`, `report_filename(study: Study) -> str`, and `screenshot_filename(study: Study) -> str`.

- [ ] **Step 1: Write the failing filename tests**

```python
import unittest

from pacs_batch import Study, report_filename, screenshot_filename


class OutputNameTests(unittest.TestCase):
    def test_patient_name_prefix_and_stable_suffix(self):
        study = Study(33, 48, patient_name="02-WCI-02B_Thorax_PA")
        self.assertEqual(report_filename(study), "02-WCI-02B_Thorax_PA__sid-33__ai-48.pdf")
        self.assertEqual(screenshot_filename(study), "02-WCI-02B_Thorax_PA__sid-33__ai-48.png")

    def test_missing_patient_name_keeps_identifier_fallback(self):
        study = Study(33, 48)
        self.assertEqual(report_filename(study), "CR-33-AI-48.pdf")
        self.assertEqual(screenshot_filename(study), "CR-33-AI-48.png")
```

- [ ] **Step 2: Run the focused test to verify the missing helper fails**

Run: `python3 -m unittest -v test_pacs_batch.OutputNameTests`

Expected: ERROR because `screenshot_filename` is not defined.

- [ ] **Step 3: Implement the shared filename stem**

```python
def study_output_stem(study: Study) -> str:
    if study.patient_name:
        return safe_filename(f"{study.patient_name}__sid-{study.sid}__ai-{study.ai_calc_id}")
    return safe_filename(f"CR-{study.sid}-AI-{study.ai_calc_id}")


def report_filename(study: Study) -> str:
    return f"{study_output_stem(study)}.pdf"


def screenshot_filename(study: Study) -> str:
    return f"{study_output_stem(study)}.png"
```

- [ ] **Step 4: Run the focused test to verify it passes**

Run: `python3 -m unittest -v test_pacs_batch.OutputNameTests`

Expected: both tests pass.

- [ ] **Step 5: Record the test evidence without committing**

Run: `git diff --check`

Expected: no whitespace errors. Do not commit without separate authorization.

### Task 2: Capture the ready viewer viewport before report generation

**Files:**
- Modify: `pacs_batch.py:654-703`
- Modify: `test_pacs_batch.py`

**Interfaces:**
- Consumes: `PacsBrowser._require_page()`, `build_viewer_url(base_url: str, study: Study) -> str`, `screenshot_filename(study: Study) -> str`, and a Playwright page with `goto()` and `screenshot()`.
- Produces: `PacsBrowser.open_viewer(study: Study) -> None` and `PacsBrowser.capture_viewport(study: Study, output_dir: str | Path) -> Path`; `PacsBrowser.download_report(study: Study) -> bytes` assumes `open_viewer` has already completed.

- [ ] **Step 1: Add a failing viewport-capture test with a fake page**

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from pacs_batch import PacsBrowser


class FakePage:
    def __init__(self):
        self.screenshot_calls = []

    def screenshot(self, *, path, full_page):
        self.screenshot_calls.append((path, full_page))
        Path(path).write_bytes(b"png")


class ViewportCaptureTests(unittest.TestCase):
    def test_capture_viewport_writes_only_the_visible_page(self):
        browser = PacsBrowser.__new__(PacsBrowser)
        browser.page = FakePage()
        study = Study(33, 48, patient_name="02-WCI-02B_Thorax_PA")
        with TemporaryDirectory() as directory:
            path = browser.capture_viewport(study, directory)
            self.assertEqual(path.name, "02-WCI-02B_Thorax_PA__sid-33__ai-48.png")
            self.assertEqual(path.read_bytes(), b"png")
        self.assertEqual(browser.page.screenshot_calls[0][1], False)
```

- [ ] **Step 2: Run the focused test to verify it fails**

Run: `python3 -m unittest -v test_pacs_batch.ViewportCaptureTests`

Expected: ERROR because `capture_viewport` is not defined.

- [ ] **Step 3: Implement viewer opening and viewport capture, then remove viewer navigation from report download**

```python
def open_viewer(self, study: Study) -> None:
    page = self._require_page()
    page.goto(build_viewer_url(self.base_url, study), wait_until="domcontentloaded")
    page.get_by_role("button", name="Generate Report", exact=False).wait_for(
        state="visible", timeout=self.timeout_ms
    )

def capture_viewport(self, study: Study, output_dir: str | Path) -> Path:
    target = Path(output_dir) / screenshot_filename(study)
    self._require_page().screenshot(path=str(target), full_page=False)
    return target
```

Delete `page.goto(build_viewer_url(self.base_url, study), wait_until="domcontentloaded")` from `download_report`; retain its existing report-dialog and PDF capture logic.

- [ ] **Step 4: Run the focused test to verify it passes**

Run: `python3 -m unittest -v test_pacs_batch.ViewportCaptureTests`

Expected: one PNG is written with `full_page=False`.

- [ ] **Step 5: Record the test evidence without committing**

Run: `git diff --check`

Expected: no whitespace errors. Do not commit without separate authorization.

### Task 3: Integrate screenshot output with retry, skip, and manifest records

**Files:**
- Modify: `pacs_batch.py:312-331`
- Modify: `pacs_batch.py:726-776`
- Modify: `test_pacs_batch.py`

**Interfaces:**
- Consumes: `PacsBrowser.open_viewer(study)`, `PacsBrowser.capture_viewport(study, output_dir) -> Path`, `PacsBrowser.download_report(study) -> bytes`, `atomic_save_pdf(target: Path, data: bytes) -> None`, and `validate_pdf_bytes(data: bytes) -> None`.
- Produces: `download_with_retries(browser: PacsBrowser, study: Study, *, output_dir: str | Path, retries: int, overwrite: bool) -> dict[str, Any]` records with existing `output` plus a `screenshot` filename field.

- [ ] **Step 1: Write failing retry and skip tests**

```python
class FakeBrowser:
    def __init__(self):
        self.calls = []

    def open_viewer(self, study):
        self.calls.append("open")

    def capture_viewport(self, study, output_dir):
        self.calls.append("screenshot")
        path = Path(output_dir) / screenshot_filename(study)
        path.write_bytes(b"png")
        return path

    def download_report(self, study):
        self.calls.append("download")
        return b"%PDF-1.4\\n%%EOF"

    def capture_diagnostic(self, study, attempt, error):
        raise AssertionError("diagnostics are not expected")


class DownloadIntegrationTests(unittest.TestCase):
    def test_success_records_pdf_and_viewport_outputs(self):
        study = Study(33, 48, patient_name="02-WCI-02B_Thorax_PA")
        browser = FakeBrowser()
        with TemporaryDirectory() as directory:
            record = download_with_retries(browser, study, output_dir=directory, retries=3, overwrite=False)
        self.assertEqual(browser.calls, ["open", "screenshot", "download"])
        self.assertEqual(record["status"], "succeeded")
        self.assertEqual(record["output"], "02-WCI-02B_Thorax_PA__sid-33__ai-48.pdf")
        self.assertEqual(record["screenshot"], "02-WCI-02B_Thorax_PA__sid-33__ai-48.png")

    def test_valid_pdf_and_nonempty_png_skip_without_browser_calls(self):
        study = Study(33, 48, patient_name="02-WCI-02B_Thorax_PA")
        browser = FakeBrowser()
        with TemporaryDirectory() as directory:
            output_dir = Path(directory)
            (output_dir / report_filename(study)).write_bytes(b"%PDF-1.4\\n%%EOF")
            (output_dir / screenshot_filename(study)).write_bytes(b"png")
            record = download_with_retries(browser, study, output_dir=output_dir, retries=3, overwrite=False)
        self.assertEqual(browser.calls, [])
        self.assertEqual(record["status"], "skipped")
        self.assertEqual(record["screenshot"], "02-WCI-02B_Thorax_PA__sid-33__ai-48.png")
```

- [ ] **Step 2: Run the focused test to verify it fails**

Run: `python3 -m unittest -v test_pacs_batch.DownloadIntegrationTests`

Expected: FAIL because the current retry flow calls only `download_report` and records no `screenshot` field.

- [ ] **Step 3: Implement the smallest integration change**

```python
def build_manifest_record(
    study: Study,
    *,
    status: str,
    output: str | None,
    screenshot: str | None,
    size: int | None,
    attempts: int,
    error: str | None,
) -> dict[str, Any]:
    return {
        "sid": study.sid,
        "aiCalcId": study.ai_calc_id,
        "patientId": study.patient_id,
        "patientName": study.patient_name,
        "status": status,
        "output": output,
        "screenshot": screenshot,
        "size": size,
        "attempts": attempts,
        "error": error,
    }

for attempt in range(1, retries + 1):
    try:
        browser.open_viewer(study)
        screenshot = browser.capture_viewport(study, output_dir)
        data = browser.download_report(study)
        atomic_save_pdf(target, data)
        return build_manifest_record(
            study,
            status="succeeded",
            output=target.name,
            screenshot=screenshot.name,
            size=len(data),
            attempts=attempt,
            error=None,
        )
```

Make an existing output skippable only when both its PDF validates and its expected PNG exists and is non-empty. Include the screenshot name in succeeded and skipped records; use `None` for a failed record that has no completed output pair.

- [ ] **Step 4: Run the full offline suite**

Run: `python3 -m unittest -v test_pacs_batch`

Expected: all filename, viewport, retry, and skip tests pass.

- [ ] **Step 5: Run static and command-interface checks**

Run: `python3 pacs_batch.py --help && git diff --check`

Expected: help exits successfully and no whitespace errors are reported.

- [ ] **Step 6: Record the test evidence without committing**

Run: `git status --short`

Expected: only the planned source, test, and authorized planning-document changes are present. Do not commit without separate authorization.

### Task 4: Run authorized PACS verification and provide review evidence

**Files:**
- Modify: `pacs_batch.py` only if actual PACS behavior exposes a defect that remains inside this task's approved scope.
- Modify: `test_pacs_batch.py` only for an offline regression check covering that bounded defect.

**Interfaces:**
- Consumes: local `credential.txt`, existing Playwright/Chromium runtime, the authorized PACS account, and `main(argv) -> int`.
- Produces: local one-study and all-study output evidence; no PACS mutation, repository commit, upload, or release.

- [ ] **Step 1: Confirm the approved runtime is present without reading credentials**

Run: `python3 -m pip show playwright && python3 -c "import playwright; print('playwright import ok')"`

Expected: Playwright is installed and importable. Stop for authorization rather than installing it if absent.

- [ ] **Step 2: Run an authorized headed one-study check**

Run: `python3 pacs_batch.py --headed --study 33:48 --output reports`

Expected: one non-empty viewport PNG is saved before report generation, one valid PDF is saved, and one manifest record reports both output names.

- [ ] **Step 3: Inspect the one-study result without exposing patient content in logs**

Run: `python3 -c "from pathlib import Path; import json; p=Path('reports/manifest.jsonl'); r=json.loads(p.read_text(encoding='utf-8').splitlines()[-1]); assert r['status'] in {'succeeded','skipped'}; assert r['output'].endswith('.pdf'); assert r['screenshot'].endswith('.png'); print(r['status'], r['attempts'])"`

Expected: prints only status and attempt count; the manifest references both outputs.

- [ ] **Step 4: Run the authorized all-studies command only after the one-study result passes**

Run: `python3 pacs_batch.py --all --output reports`

Expected: every discovered study is processed; later studies continue after a failure; a non-zero exit accurately signals any failures.

- [ ] **Step 5: Hand off factual evidence for Reviewer evaluation**

Report the exact working-tree state, all commands actually run, discovered/completed/failed counts, test results, any selector or runtime gaps, and confirmation that no credentials were printed. Do not claim acceptance, commit, push, upload, or release.

## Plan Self-Review

- PACS-BATCH-001 and PACS-BATCH-002 remain preserved by the existing discovery and direct URL path; Tasks 2–4 verify that path.
- PACS-BATCH-003 is implemented and tested in Tasks 2–3, then browser-verified in Task 4.
- PACS-BATCH-004 is preserved and runtime-verified in Task 4.
- PACS-BATCH-005 is implemented and offline-tested in Task 1.
- PACS-BATCH-006 is preserved and tested in Task 3, then observed in Task 4.
- The plan contains no unresolved placeholders; interfaces in Tasks 2–3 use the names defined in Tasks 1–2.

## Execution Handoff

This plan is Draft planning material, not an executable repository task. Before execution, publish the companion task at `.agents/tasks/pacs-batch-screenshot-and-report-download.md` at an immutable revision and obtain the task's stated side-effect authorization.
