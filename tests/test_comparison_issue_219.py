"""Unit tests for issue #219 RustChain comparison submission."""

import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from bounties.issue_219_rustchain_comparison.validator import (
    ComparisonValidator,
    ValidationResult,
)


class TestRustChainComparisonIssue219(unittest.TestCase):
    """Test suite validating compliance with bounty issue #219 stipulations."""

    @classmethod
    def setUpClass(cls) -> None:
        """Establish paths and shared validator instance."""
        cls.base_dir = BASE_DIR
        cls.doc_path = (
            cls.base_dir
            / "bounties"
            / "issue_219_rustchain_comparison"
            / "comparison.md"
        )
        cls.checklist_path = (
            cls.base_dir
            / "bounties"
            / "issue_219_rustchain_comparison"
            / "STIPULATIONS_CHECKLIST.md"
        )
        cls.validator = ComparisonValidator(cls.doc_path)

    def test_document_exists(self) -> None:
        """Verify the comparison markdown file is present on disk."""
        self.assertTrue(
            self.doc_path.exists(),
            f"Comparison document does not exist at {self.doc_path}",
        )
        self.assertGreater(
            self.doc_path.stat().st_size,
            0,
            "Comparison document is empty",
        )

    def test_stipulations_checklist_exists(self) -> None:
        """Verify the stipulations checklist file is present and populated."""
        self.assertTrue(
            self.checklist_path.exists(),
            f"Checklist document does not exist at {self.checklist_path}",
        )
        content = self.checklist_path.read_text(encoding="utf-8")
        self.assertIn("STIP-01", content)
        self.assertIn("COMPLIANT", content)

    def test_word_count_boundaries(self) -> None:
        """Verify that document word count is strictly between 300 and 800 words."""
        count = self.validator.calculate_word_count()
        self.assertGreaterEqual(
            count,
            300,
            f"Word count {count} is less than required 300 words.",
        )
        self.assertLessEqual(
            count,
            800,
            f"Word count {count} exceeds maximum allowed 800 words.",
        )

    def test_required_sections_present(self) -> None:
        """Verify that all required comparative sections exist in the document."""
        missing = self.validator.verify_required_sections()
        self.assertEqual(
            missing,
            [],
            f"Missing required sections: {missing}",
        )

    def test_required_technical_concepts(self) -> None:
        """Verify all essential blockchain concepts are analyzed."""
        missing = self.validator.verify_required_terms()
        self.assertEqual(
            missing,
            [],
            f"Missing essential technical terms: {missing}",
        )

    def test_honest_critique_of_rustchain(self) -> None:
        """Verify the document provides an honest assessment of RustChain limitations."""
        content = self.validator.read_content().lower()
        self.assertIn("limitations", content)
        self.assertIn("throughput", content)
        self.assertIn("latency", content)
        self.assertIn("sybil", content)

    def test_validator_full_success(self) -> None:
        """Verify the comparison document passes overall validation with zero errors."""
        result: ValidationResult = self.validator.validate(min_words=300, max_words=800)
        self.assertTrue(result.is_valid, f"Validation failed with errors: {result.errors}")
        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.missing_sections), 0)
        self.assertEqual(len(result.missing_terms), 0)

    def test_validator_detects_underflow(self) -> None:
        """Verify validator flags content beneath minimum word thresholds."""
        result = self.validator.validate(min_words=1000, max_words=2000)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("below minimum requirement" in e for e in result.errors))

    def test_validator_detects_overflow(self) -> None:
        """Verify validator flags content exceeding maximum word thresholds."""
        result = self.validator.validate(min_words=50, max_words=100)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("exceeds maximum allowance" in e for e in result.errors))


if __name__ == "__main__":
    unittest.main()
