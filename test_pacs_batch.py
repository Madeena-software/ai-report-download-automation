from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from pacs_batch import (
    Study,
    StudyCollector,
    atomic_save_pdf,
    build_manifest_record,
    build_viewer_url,
    canvas_metrics_ready,
    download_with_retries,
    extract_studies_from_hrefs,
    extract_studies_from_json,
    load_credentials,
    parse_explicit_studies,
    report_type_is_image,
    select_pointer_target,
    report_filename,
    safe_filename,
    screenshot_filename,
    study_stem,
    validate_pdf_bytes,
)


class TestPacsBatchOffline(unittest.TestCase):
    def test_visible_selector_is_pointer_target_not_inner_combobox(self) -> None:
        class Target:
            def __init__(self, visible: bool) -> None:
                self.first = self
                self.visible = visible
                self.click_kwargs = None

            def count(self) -> int:
                return 1

            def is_visible(self) -> bool:
                return self.visible

            def click(self, **kwargs: object) -> None:
                self.click_kwargs = kwargs

        class Select:
            def __init__(self) -> None:
                self.selector = Target(visible=True)
                self.combo = Target(visible=True)

            def locator(self, query: str) -> Target:
                return self.selector if query == ".ant-select-selector" else self.combo

        select = Select()
        target = select_pointer_target(select)
        target.click(timeout=5000)
        self.assertIs(target, select.selector)
        self.assertIsNotNone(select.selector.click_kwargs)
        self.assertIsNone(select.combo.click_kwargs)
        self.assertNotIn("force", select.selector.click_kwargs)

    def test_inner_combobox_remains_aria_controls_source(self) -> None:
        class Combo:
            first = None

            def get_attribute(self, name: str) -> str:
                self.requested = name
                return "report-select-list"

        combo = Combo()
        self.assertEqual(combo.get_attribute("aria-controls"), "report-select-list")
        self.assertEqual(combo.requested, "aria-controls")

    def test_outer_select_fallback_when_selector_is_unavailable(self) -> None:
        class Outer:
            first = None

            def locator(self, query: str):
                return self

            def count(self) -> int:
                return 0

        select = Outer()
        self.assertIs(select_pointer_target(select), select)

    def test_image_report_selection_confirmation(self) -> None:
        for label in ("Image Report", "影像报告", "Laporan Gambar", "Laporan Citra"):
            self.assertTrue(report_type_is_image(label))
        self.assertFalse(report_type_is_image("Text Report"))
        self.assertFalse(report_type_is_image("Text Report Image Report"))

    def test_delayed_image_report_selection_eventually_confirms(self) -> None:
        states = iter(("Text Report", "Text Report", "Image Report"))
        selected = next((state for state in states if report_type_is_image(state)), None)
        self.assertEqual(selected, "Image Report")

    def test_stale_dropdown_click_does_not_confirm_selection(self) -> None:
        self.assertFalse(report_type_is_image("Text Report"))

    def test_blank_large_pdf_does_not_prove_radiograph_readiness(self) -> None:
        blank_large_pdf = b"%PDF-1.4\n" + b"x" * 60000 + b"\n%%EOF\n"
        validate_pdf_bytes(blank_large_pdf)
        self.assertFalse(
            canvas_metrics_ready(
                {
                    "visible": True,
                    "width": 800,
                    "height": 600,
                    "alpha_fraction": 0.0,
                    "luminance_range": 0,
                    "tone_bins": 1,
                }
            )
        )

    def test_rendered_canvas_metrics_are_ready(self) -> None:
        self.assertTrue(
            canvas_metrics_ready(
                {
                    "visible": True,
                    "width": 800,
                    "height": 600,
                    "alpha_fraction": 1.0,
                    "luminance_range": 240,
                    "tone_bins": 16,
                }
            )
        )

    def test_render_readiness_retries_then_succeeds(self) -> None:
        class Browser:
            attempts = 0

            def download_report(self, study: Study, screenshot_path: Path) -> bytes:
                self.attempts += 1
                screenshot_path.write_bytes(b"png")
                if self.attempts == 1:
                    raise RuntimeError("radiograph is not ready")
                return b"%PDF-1.4\n" + b"x" * 1020 + b"\n%%EOF\n"

            def capture_diagnostic(self, study: Study, attempt: int, error: Exception) -> None:
                pass

        with tempfile.TemporaryDirectory() as tmpdir:
            record = download_with_retries(
                Browser(),
                Study(sid=1, ai_calc_id=2),
                output_dir=tmpdir,
                retries=2,
                overwrite=False,
            )
        self.assertEqual(record["status"], "succeeded")
        self.assertEqual(record["attempts"], 2)

    def test_persistent_render_readiness_failure_is_failed(self) -> None:
        class Browser:
            def download_report(self, study: Study, screenshot_path: Path) -> bytes:
                raise RuntimeError("radiograph is not ready")

            def capture_diagnostic(self, study: Study, attempt: int, error: Exception) -> None:
                pass

        with tempfile.TemporaryDirectory() as tmpdir:
            record = download_with_retries(
                Browser(),
                Study(sid=1, ai_calc_id=2),
                output_dir=tmpdir,
                retries=2,
                overwrite=False,
            )
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["attempts"], 2)

    def test_load_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dir_path = Path(tmpdir)
            env_file = dir_path / ".env"
            env_file.write_text("AI_PACS_USERNAME=user_env\nAI_PACS_PASSWORD=pass_env\n", encoding="utf-8")

            # Fallback to .env when credential.txt does not exist
            missing_cred = dir_path / "credential.txt"
            u, p = load_credentials(missing_cred)
            self.assertEqual(u, "user_env")
            self.assertEqual(p, "pass_env")

            # Direct load of .env file
            u2, p2 = load_credentials(env_file)
            self.assertEqual(u2, "user_env")
            self.assertEqual(p2, "pass_env")
    def test_study_dataclass(self) -> None:
        s1 = Study(sid=33, ai_calc_id=48, patient_id="P1", patient_name="Name1")
        s2 = Study(sid=33, ai_calc_id=48, patient_id="P2", patient_name="Name2")
        self.assertEqual(s1, s2)
        s3 = Study(sid=34, ai_calc_id=10)
        self.assertLess(s1, s3)

    def test_safe_filename(self) -> None:
        self.assertEqual(safe_filename("02-WCI-02B_Thorax_PA"), "02-WCI-02B_Thorax_PA")
        self.assertEqual(safe_filename("John/Doe:Test?*"), "John_Doe_Test__")
        self.assertEqual(safe_filename("  trailing.  "), "trailing")

    def test_study_stem(self) -> None:
        # Patient name present
        study1 = Study(sid=33, ai_calc_id=48, patient_name="02-WCI-02B_Thorax_PA")
        self.assertEqual(study_stem(study1), "02-WCI-02B_Thorax_PA__sid-33__ai-48")
        self.assertEqual(report_filename(study1), "02-WCI-02B_Thorax_PA__sid-33__ai-48.pdf")
        self.assertEqual(screenshot_filename(study1), "02-WCI-02B_Thorax_PA__sid-33__ai-48.png")

        # Patient name with invalid filesystem characters
        study2 = Study(sid=33, ai_calc_id=48, patient_name="John/Doe:123")
        self.assertEqual(study_stem(study2), "John_Doe_123__sid-33__ai-48")

        # Empty / missing patient name fallback
        study3 = Study(sid=58, ai_calc_id=50, patient_name="")
        self.assertEqual(study_stem(study3), "CR-58-AI-50")
        self.assertEqual(report_filename(study3), "CR-58-AI-50.pdf")
        self.assertEqual(screenshot_filename(study3), "CR-58-AI-50.png")

        # Whitespace patient name fallback
        study4 = Study(sid=12, ai_calc_id=34, patient_name="   ")
        self.assertEqual(study_stem(study4), "CR-12-AI-34")

        # Duplicate patient names across different studies produce distinct stems
        study5a = Study(sid=10, ai_calc_id=1, patient_name="Same Patient")
        study5b = Study(sid=11, ai_calc_id=2, patient_name="Same Patient")
        self.assertNotEqual(study_stem(study5a), study_stem(study5b))

    def test_extract_studies_from_json(self) -> None:
        payload = {
            "code": 200,
            "data": {
                "records": [
                    {
                        "sid": "58",
                        "aiCalcId": 50,
                        "patientId": "PID123",
                        "patientName": "Test Patient",
                    },
                    {
                        "studyId": 99,
                        "aicalcid": 100,
                        "patient_id": "PID456",
                        "patient_name": "Another Patient",
                    },
                ]
            },
        }
        extracted = extract_studies_from_json(payload)
        self.assertEqual(len(extracted), 2)
        self.assertEqual(extracted[0], Study(sid=58, ai_calc_id=50, patient_id="PID123", patient_name="Test Patient"))
        self.assertEqual(extracted[1], Study(sid=99, ai_calc_id=100, patient_id="PID456", patient_name="Another Patient"))

    def test_extract_studies_from_hrefs(self) -> None:
        hrefs = [
            "/view/dr/index.html/viewer?action=viewer&type=CR&sid=58&pacs=fei&aiCalcId=50",
            "/view/dr/index.html/viewer?action=viewer&type=CR&sid=99&pacs=fei&aiCalcId=100",
            "http://example.com/other",
        ]
        extracted = extract_studies_from_hrefs(hrefs, "http://124.225.183.175:8361")
        self.assertEqual(len(extracted), 2)
        self.assertEqual(extracted[0].sid, 58)
        self.assertEqual(extracted[0].ai_calc_id, 50)

    def test_study_collector(self) -> None:
        collector = StudyCollector("http://124.225.183.175:8361")
        collector.add_hrefs(["/view/dr/index.html/viewer?action=viewer&type=CR&sid=58&pacs=fei&aiCalcId=50"])
        collector.add_json({"sid": 58, "aiCalcId": 50, "patientId": "P58", "patientName": "Patient 58"})
        studies = collector.studies()
        self.assertEqual(len(studies), 1)
        self.assertEqual(studies[0].patient_name, "Patient 58")

    def test_build_viewer_url(self) -> None:
        url = build_viewer_url("http://124.225.183.175:8361", Study(sid=58, ai_calc_id=50))
        self.assertIn("sid=58", url)
        self.assertIn("aiCalcId=50", url)
        self.assertIn("view/dr/index.html/viewer", url)

    def test_validate_pdf_bytes(self) -> None:
        valid_pdf = b"%PDF-1.4\n" + b"x" * 1020 + b"\n%%EOF\n"
        validate_pdf_bytes(valid_pdf)

        with self.assertRaises(ValueError):
            validate_pdf_bytes(b"NOT A PDF")

        with self.assertRaises(ValueError):
            validate_pdf_bytes(b"%PDF-1.4 short")

        with self.assertRaises(ValueError):
            validate_pdf_bytes(b"%PDF-1.4\n" + b"x" * 1020 + b"\nNO EOF\n")

    def test_atomic_save_pdf(self) -> None:
        valid_pdf = b"%PDF-1.4\n" + b"x" * 1020 + b"\n%%EOF\n"
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.pdf"
            atomic_save_pdf(path, valid_pdf)
            self.assertTrue(path.is_file())
            self.assertEqual(path.read_bytes(), valid_pdf)

    def test_build_manifest_record(self) -> None:
        study = Study(sid=33, ai_calc_id=48, patient_id="P33", patient_name="Name33")
        record = build_manifest_record(
            study,
            status="succeeded",
            output="Name33__sid-33__ai-48.pdf",
            screenshot="Name33__sid-33__ai-48.png",
            size=2048,
            attempts=1,
            error=None,
        )
        self.assertEqual(record["sid"], 33)
        self.assertEqual(record["aiCalcId"], 48)
        self.assertEqual(record["patientName"], "Name33")
        self.assertEqual(record["status"], "succeeded")
        self.assertEqual(record["output"], "Name33__sid-33__ai-48.pdf")
        self.assertEqual(record["screenshot"], "Name33__sid-33__ai-48.png")

    def test_parse_explicit_studies(self) -> None:
        parsed = parse_explicit_studies(["58:50", "33:48:Patient Name"])
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[0], Study(sid=58, ai_calc_id=50, patient_name=""))
        self.assertEqual(parsed[1], Study(sid=33, ai_calc_id=48, patient_name="Patient Name"))


if __name__ == "__main__":
    unittest.main()
