"""The site model: every entity, its URL, and the typed links between them.

Rule enforced here: the value chain and the competence model are only ever
joined through two sources, the tool crosswalk (labelled "tool-based") and the
hand-authored examples. There is deliberately no stage→competency map.
"""
from __future__ import annotations

from collections import OrderedDict

from . import BuildError

RESERVED = {
    "what": {"levels"},
    "how": {"4cs", "six-trumps"},
}


class Site:
    def __init__(self, *, vocab, prov, value_chain, competence, rubric, pedagogy, examples, warnings):
        self.vocab = vocab
        self.prov = prov
        self.vc = value_chain
        self.comp = competence
        self.rubric = rubric
        self.ped = pedagogy
        self.examples = examples
        self.warnings = warnings
        self.tools = vocab.tools()

        for sa in competence["subareas"]:
            if sa["id"] in RESERVED["what"]:
                raise BuildError(f"Sub-area id '{sa['id']}' collides with a reserved URL segment")

        self.stages = [dict(s, **value_chain["stages"][s["id"]]) for s in vocab.stages]
        self.stage_by_id = {s["id"]: s for s in self.stages}
        self.tiers = []
        for t_csv, t_md in zip(vocab.tiers, value_chain["tiers"]):
            self.tiers.append({"id": t_csv["id"], "name": t_csv["name"], "step": t_md["step"], "stages": t_csv["stages"]})
        self.domain_by_id = {d["id"]: d for d in competence["domains"]}
        self.sub_by_id = {sa["id"]: sa for sa in competence["subareas"]}
        self.comp_by_key = {(c["subarea"], c["slug"]): c for c in competence["competencies"]}
        self.c4_by_id = {c["id"]: c for c in pedagogy["cs"]}
        self.trump_by_id = {t["id"]: t for t in pedagogy["trumps"]}
        self.example_by_id = {e["id"]: e for e in examples}

        self._tool_links()
        self._example_links()

    # ---- URLs (site paths: root-relative, no leading slash) -----------------
    @staticmethod
    def u_stage(sid: str) -> str: return f"where/{sid}/"
    @staticmethod
    def u_tier(tid: str) -> str: return f"where/#{tid}"
    @staticmethod
    def u_domain(did: str) -> str: return f"what/#{did}"
    @staticmethod
    def u_sub(said: str) -> str: return f"what/{said}/"
    @staticmethod
    def u_comp(said: str, slug: str) -> str: return f"what/{said}/{slug}/"
    @staticmethod
    def u_level(n: int) -> str: return f"what/levels/#l{n}"
    @staticmethod
    def u_c4(cid: str) -> str: return f"how/4cs/{cid}/"
    @staticmethod
    def u_trump(tid: str) -> str: return f"how/six-trumps/{tid}/"
    @staticmethod
    def u_example(eid: str) -> str: return f"examples/{eid}/"
    @staticmethod
    def u_tool(slug: str) -> str: return f"tools/#t-{slug}"

    # ---- tool-based links -----------------------------------------------------
    def _tool_links(self) -> None:
        self.stage_tools: dict[str, list] = {s["id"]: [] for s in self.stages}
        # stage -> domain -> sub-area (or None) -> [tool]
        self.stage_subs: dict[str, OrderedDict] = {s["id"]: OrderedDict() for s in self.stages}
        # sub-area -> stage -> [tool]
        self.sub_stages: dict[str, OrderedDict] = {sa["id"]: OrderedDict() for sa in self.comp["subareas"]}
        self.domain_only: dict[str, OrderedDict] = {d["id"]: OrderedDict() for d in self.comp["domains"]}

        for tool in self.tools:
            for link in tool["links"]:
                sid, did, said = link["stage"], link["domain"], link["subarea"]
                self.stage_tools[sid].append((tool, link))
                doms = self.stage_subs[sid].setdefault(did, OrderedDict())
                doms.setdefault(said, []).append(tool)
                if said:
                    self.sub_stages[said].setdefault(sid, []).append(tool)
                else:
                    self.domain_only[did].setdefault(sid, []).append(tool)

        dom_order = {d["id"]: d["order"] for d in self.comp["domains"]}
        sub_order = {sa["id"]: sa["order"] for sa in self.comp["subareas"]}
        stage_order = {s["id"]: s["order"] for s in self.stages}
        for sid in self.stage_subs:
            doms = self.stage_subs[sid]
            ordered = OrderedDict()
            for did in sorted(doms, key=dom_order.__getitem__):
                subs = doms[did]
                ordered[did] = OrderedDict((k, subs[k]) for k in sorted(subs, key=lambda k: (k is None, sub_order.get(k, 0))))
            self.stage_subs[sid] = ordered
        for said in self.sub_stages:
            subs = self.sub_stages[said]
            self.sub_stages[said] = OrderedDict((k, subs[k]) for k in sorted(subs, key=stage_order.__getitem__))

    # ---- example links --------------------------------------------------------
    def _example_links(self) -> None:
        self.stage_examples: dict[str, list] = {s["id"]: [] for s in self.stages}
        self.sub_examples: dict[str, list] = {sa["id"]: [] for sa in self.comp["subareas"]}
        self.comp_examples: dict[tuple, list] = {}
        self.c4_examples: dict[str, list] = {c["id"]: [] for c in self.ped["cs"]}
        self.trump_examples: dict[str, list] = {t["id"]: [] for t in self.ped["trumps"]}
        self.level_examples: dict[int, list] = {n: [] for n in range(1, 6)}

        for ex in self.examples:
            for i, sid in enumerate(ex["anchor"]["stages"]):
                self.stage_examples[sid].append((ex, "Anchored here" if i == 0 else "Also touches this substep"))
            for t in ex["targets"]:
                self.sub_examples[t["subarea"]].append((ex, t))
                self.comp_examples.setdefault((t["subarea"], t["slug"]), []).append((ex, t))
                self.level_examples[t["target"]].append((ex, t))
            for i, b in enumerate(ex["design"]["blocks"], start=1):
                self.c4_examples[b["c4"]].append((ex, b, i))
                for tr in b["trumps"]:
                    self.trump_examples[tr].append((ex, b, i))

    # ---- counts ---------------------------------------------------------------
    def counts(self) -> dict:
        return {
            "tiers": len(self.tiers),
            "substeps": len(self.stages),
            "domains": len(self.comp["domains"]),
            "subareas": len(self.comp["subareas"]),
            "competencies": len(self.comp["competencies"]),
            "levels": 5,
            "cs": len(self.ped["cs"]),
            "trumps": len(self.ped["trumps"]),
            "crosswalk_rows": len(self.vocab.crosswalk),
            "tools": len(self.tools),
            "examples": len(self.examples),
        }
