import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True

from onboarding_lib import BuildError  # noqa: E402
from onboarding_lib.competence import level_state, resolve_tag  # noqa: E402
from onboarding_lib.parse_pedagogy import parse as parse_pedagogy  # noqa: E402
from onboarding_lib.parse_rubric import parse as parse_rubric  # noqa: E402
from onboarding_lib.parse_value_chain import parse as parse_value_chain  # noqa: E402
from onboarding_lib.vocab import Vocab  # noqa: E402

STAGES_CSV = """id,display_name,tier,order,aliases
clinical-pharmacology,Clinical Pharmacology,Clinical development,1,Clin Pharm|popPK
formulation-drug-product,Formulation & Drug Product Development (CMC),Clinical development,2,CMC
"""
VALUE_CHAIN_MD = """# Pharma Value Chain Model
# Version: v9.9.9 (AI-drafted, pending MO review)
# Last updated: 2026-05-25
---

# Tier 1 · Step 2 — CLINICAL DEVELOPMENT

## Substep: Clin Pharm

*A scope note that wraps
onto a second line.*

### Primary DS question
How does the drug behave in the body (PK) and what is the relationship
between exposure and effect (PD)?

### Key questions
- What dose and schedule produce the target exposure?
- How does PK vary across patients (covariates: weight, renal/hepatic
  function)?

### Established DS methods and tools
**Population PK/PD (conventional)**
- NONMEM (industry standard for popPK)

**NABM-specific (nucleic acid-based medicines)**
Note: Standard popPK/PD tools are not well-suited to mechanistic NABM
modelling. Key approaches:
- Multi-scale modelling approaches (biophysical → cellular → tissue) [BEYOND REFERENCE — oligo-specific, not yet standard]

---

## Substep: Formulation & Drug Product Development (CMC)

### Primary DS question
How do we make it?

### Key questions
- Which excipients?

### Established DS methods and tools
- Oligonucleotide-specific: LNP and GalNAc delivery-system formulation; liver-
  tropism and tissue-targeting design [BEYOND REFERENCE — oligo delivery, not yet standard]

## Coverage status
| ignored | table |
"""


def make_vocab(tmp: Path) -> Vocab:
    (tmp / "vocab").mkdir()
    (tmp / "vocab" / "stages.csv").write_text(STAGES_CSV)
    (tmp / "vocab" / "domains.csv").write_text("id,display_name,order\nmath-stats,Mathematics & Statistics,1\n")
    (tmp / "vocab" / "subareas.csv").write_text("id,display_name,domain_id,order\nstatistics,Statistics,math-stats,1\n")
    (tmp / "vocab" / "crosswalk.csv").write_text(
        "canonical_tool,type,aliases,stage_id,pds_domain,pds_subarea,weight,confidence,source,flag,notes\n"
        "NONMEM,tool,,clinical-pharmacology,math-stats,statistics,1.0,high,x,,\n")
    return Vocab(tmp)


class ValueChainParserTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.vocab = make_vocab(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_full_substep(self):
        vc = parse_value_chain(VALUE_CHAIN_MD, self.vocab)
        self.assertEqual(vc["version"], "v9.9.9")
        self.assertEqual(vc["status"], "AI-drafted, pending MO review")
        st = vc["stages"]["clinical-pharmacology"]
        self.assertEqual(st["notes"], ["A scope note that wraps onto a second line."])
        self.assertTrue(st["primary_question"].endswith("between exposure and effect (PD)?"))
        self.assertEqual(st["key_questions"][1], "How does PK vary across patients (covariates: weight, renal/hepatic function)?")
        groups = st["method_groups"]
        self.assertEqual([g["title"] for g in groups], ["Population PK/PD (conventional)", "NABM-specific (nucleic acid-based medicines)"])
        self.assertIn("Key approaches:", groups[1]["notes"][0])
        item = groups[1]["items"][0]
        self.assertEqual(item["flag"], "oligo-specific, not yet standard")
        self.assertNotIn("BEYOND", item["text"])

    def test_wrapped_hyphen_and_flag_on_continuation(self):
        vc = parse_value_chain(VALUE_CHAIN_MD, self.vocab)
        item = vc["stages"]["formulation-drug-product"]["method_groups"][0]["items"][0]
        self.assertIn("liver-tropism", item["text"])
        self.assertEqual(item["flag"], "oligo delivery, not yet standard")
        self.assertEqual(item["lead"], "Oligonucleotide-specific")

    def test_wrong_tier_fails(self):
        bad = VALUE_CHAIN_MD.replace("CLINICAL DEVELOPMENT", "ON-MARKET")
        with self.assertRaises(BuildError):
            parse_value_chain(bad, self.vocab)

    def test_unknown_heading_fails(self):
        with self.assertRaises(BuildError):
            parse_value_chain(VALUE_CHAIN_MD.replace("## Substep: Clin Pharm", "## Substep: Nope"), self.vocab)


class CsvOverflowTest(unittest.TestCase):
    def test_unquoted_comma_in_alias_is_rejoined(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            vocab = make_vocab(tmp)
            (tmp / "vocab" / "stages.csv").write_text(STAGES_CSV.replace("CMC\n", "Preclinical (DMPK, tox)|DMPK\n"))
            vocab = Vocab(tmp)
            self.assertEqual(vocab.stage_by_id["formulation-drug-product"]["aliases"], ["Preclinical (DMPK, tox)", "DMPK"])


class CompetenceHelpersTest(unittest.TestCase):
    def test_level_state(self):
        self.assertEqual(level_state("Recognise it."), ("ok", "Recognise it."))
        self.assertEqual(level_state("—"), ("na", ""))
        self.assertEqual(level_state("— *(merges with Big Data Systems (Application) at this level)*"),
                         ("na", "merges with Big Data Systems (Application) at this level"))
        self.assertEqual(level_state("  "), ("missing", ""))

    def test_resolve_tag(self):
        comps = [{"name": "Hypothesis testing"},
                 {"name": "Design of experiments (DOE). Nonsampling error, biases, confounding, and causal inference"}]
        self.assertIs(resolve_tag("hypothesis  Testing", comps), comps[0])
        self.assertIs(resolve_tag("Design of experiments (DOE)...", comps), comps[1])
        self.assertIsNone(resolve_tag("Design of experiments (DOE)", comps))


RUBRIC_MD = """# Rubric
| Dimension | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| **Autonomy** | a1 | a2 | a3 | a4 | a5 |
| **Context** | c1 | c2 | c3 | c4 | c5 |
| **Judgment** | j1 | j2 | j3 | j4 | j5 |
| **Effect on others** | e1 | e2 | e3 | e4 | e5 |
""" + "".join(
    f"\n## L{n} — Name{n}\n\n> *Quote {n}.*\n\nA person at L{n} can:\n\n- **Do** thing {n}.\n\n"
    + (f"Cannot yet (reliably): stuff {n}.\n\n**Promotion signal to L{n + 1}:** signal {n}.\n" if n < 5 else "A closing note.\n")
    for n in range(1, 6)
) + "\n## How to write a competency entry\n- ignored\n"


class RubricParserTest(unittest.TestCase):
    def test_parse(self):
        r = parse_rubric(RUBRIC_MD)
        self.assertEqual([d["name"] for d in r["dimensions"]], ["Autonomy", "Context", "Judgment", "Effect on others"])
        self.assertEqual(r["levels"][2]["cannot_qualifier"], "reliably")
        self.assertEqual(r["levels"][0]["promotion"], "signal 1.")
        self.assertEqual(r["levels"][4]["notes"], ["A closing note."])
        self.assertEqual(r["levels"][1]["can"], ["**Do** thing 2."])


PEDAGOGY_MD = """# Pedagogic Practices
# Version: v0.1.1 (AI-drafted, pending MO review)
---

## What this is

Core premise: **the person doing the work is the person doing the learning.**

## The 4Cs — instructional design map

Intro to the 4Cs.

1. **Connections** — Learners connect.
   *Examples:* opening round.

2. **Concepts** — Learners take in.
   *Examples:* short input.

3. **Concrete Practice** — Learners practise.
   *Examples:* gap cards.

4. **Conclusions** — Learners commit.
   *Examples:* read-back.

## The Six Trumps — brain-based principles

""" + "".join(f"{n}. **Trump {n} trumps other** — Body {n}.\n   *Apply:* apply {n}.\n\n" for n in range(1, 7)) + """
## How CPDSE uses this

| Workshop 1 block | 4C |
|---|---|
| Open | **Connections** |
| Gaps | **Concepts + Concrete Practice** — anchor |
"""


class PedagogyParserTest(unittest.TestCase):
    def test_parse(self):
        p = parse_pedagogy(PEDAGOGY_MD)
        self.assertEqual([c["id"] for c in p["cs"]], ["connections", "concepts", "concrete-practice", "conclusions"])
        self.assertEqual(p["cs"][2]["examples"], "gap cards.")
        self.assertEqual(p["trumps"][0]["apply"], "apply 1.")
        self.assertEqual(p["workshop"][1]["cs"], ["concepts", "concrete-practice"])
        self.assertTrue(p["premise"].startswith("**the person doing the work"))

    def test_missing_c_fails(self):
        with self.assertRaises(BuildError):
            parse_pedagogy(PEDAGOGY_MD.replace("4. **Conclusions**", "4. **Closing**"))


if __name__ == "__main__":
    unittest.main()
