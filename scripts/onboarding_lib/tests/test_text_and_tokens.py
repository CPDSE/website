import sys
import unittest

sys.dont_write_bytecode = True

from onboarding_lib.text import inline_md, rel, slugify, strip_md  # noqa: E402
from onboarding_lib.tokens import contrast  # noqa: E402


class SlugifyTest(unittest.TestCase):
    def test_ampersand_and_punctuation(self):
        self.assertEqual(slugify("Model Building & Assessment"), "model-building-and-assessment")
        self.assertEqual(slugify("What can AI be used for? What can it not be used for?"),
                         "what-can-ai-be-used-for-what-can-it-not-be-used-for")

    def test_cut_at_word_boundary(self):
        slug = slugify("Design of experiments (DOE). Nonsampling error, biases, confounding, and causal inference")
        self.assertLessEqual(len(slug), 60)
        self.assertFalse(slug.endswith("-"))
        self.assertTrue(slug.startswith("design-of-experiments-doe"))

    def test_accents(self):
        self.assertEqual(slugify("Vibe Café"), "vibe-cafe")


class RelTest(unittest.TestCase):
    def test_root_to_page(self):
        self.assertEqual(rel("", "where/lead-identification/"), "where/lead-identification/")

    def test_page_to_root(self):
        self.assertEqual(rel("what/statistics/hypothesis-testing/", ""), "../../../")

    def test_sibling_with_fragment(self):
        self.assertEqual(rel("what/statistics/", "what/levels/#l3"), "../levels/#l3")

    def test_same_page_fragment(self):
        self.assertEqual(rel("what/statistics/", "#l3"), "#l3")
        self.assertEqual(rel("what/", "what/#statistics"), "#statistics")

    def test_file(self):
        self.assertEqual(rel("how/4cs/concepts/", "assets/site.css"), "../../../assets/site.css")


class InlineMdTest(unittest.TestCase):
    def test_escapes_before_markup(self):
        self.assertEqual(inline_md("a <b> & **bold**"), "a &lt;b&gt; &amp; <strong>bold</strong>")

    def test_code_protects_asterisks(self):
        self.assertEqual(inline_md("use `a*b*c` and *this*"), "use <code>a*b*c</code> and <em>this</em>")

    def test_strip(self):
        self.assertEqual(strip_md("**Recognise** the *concept* in `code`"), "Recognise the concept in code")


class ContrastTest(unittest.TestCase):
    def test_known_ratios(self):
        self.assertAlmostEqual(contrast("#FFFFFF", "#000000"), 21.0, places=1)
        self.assertLess(contrast("#FFFFFF", "#B39540"), 3.0)  # the prototype's white-on-gold failed AA


if __name__ == "__main__":
    unittest.main()
