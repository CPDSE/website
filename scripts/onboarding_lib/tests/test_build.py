"""End-to-end tests against the real models checkout (skipped when it is not available)."""
import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

import build_onboarding as B  # noqa: E402
from onboarding_lib import BuildError, check  # noqa: E402

WEBSITE = Path(__file__).resolve().parents[3]
MODELS = Path(os.environ.get("CPDSE_REFERENCE_MODELS", WEBSITE.parent / "cpdse-reference-models"))
EXAMPLES = WEBSITE / "reference-models" / "_src" / "examples.json"


@unittest.skipUnless((MODELS / "vocab" / "stages.csv").is_file(), "cpdse-reference-models checkout not found")
class BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.files, cls.site, cls.warnings = B.build(str(MODELS), "reference-models", None, allow_dirty=True)

    def test_counts(self):
        c = self.site.counts()
        self.assertEqual((c["substeps"], c["domains"], c["subareas"], c["cs"], c["trumps"]), (14, 7, 30, 4, 6))
        self.assertGreaterEqual(c["competencies"], 100)

    def test_every_page_and_asset_is_checked_clean(self):
        errors, _ = check.run(self.files, self.site.config["external_allow"])
        self.assertEqual(errors, [])

    def test_no_bytecode_left_in_models_repo(self):
        self.assertFalse(list(MODELS.rglob("__pycache__")))

    def test_duplicate_competency_names_get_distinct_urls(self):
        self.assertIn("what/statistics/hypothesis-testing/index.html", self.files)
        self.assertIn("what/analysis/hypothesis-testing/index.html", self.files)

    def test_deterministic(self):
        again, _, _ = B.build(str(MODELS), "reference-models", None, allow_dirty=True)
        self.assertEqual(sorted(again), sorted(self.files))
        self.assertTrue(all(again[k] == self.files[k] for k in again))

    def _bad_examples(self, mutate):
        data = json.loads(EXAMPLES.read_text(encoding="utf-8"))
        data = copy.deepcopy(data)
        mutate(data["examples"][0])
        tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
        json.dump(data, tmp)
        tmp.close()
        self.addCleanup(os.unlink, tmp.name)
        with self.assertRaises(BuildError) as ctx:
            B.build(str(MODELS), "reference-models", tmp.name, allow_dirty=True)
        return str(ctx.exception)

    def test_unknown_stage_suggests(self):
        msg = self._bad_examples(lambda ex: ex["anchor"].__setitem__("stages", ["lead-identifcation"]))
        self.assertIn("lead-identification", msg)

    def test_wrong_competency_name(self):
        msg = self._bad_examples(lambda ex: ex["targets"][0].__setitem__("competency", "Model assessment"))
        self.assertIn("is not a competency", msg)

    def test_target_on_not_applicable_level(self):
        def mutate(ex):
            ex["targets"][0].update({"subarea": "statistics", "competency": "Descriptive statistics", "today": 2, "target": 5})
        self.assertIn("does not apply", self._bad_examples(mutate))

    def test_illustrative_is_required(self):
        self.assertIn("illustrative", self._bad_examples(lambda ex: ex.__setitem__("illustrative", [])))


if __name__ == "__main__":
    unittest.main()
