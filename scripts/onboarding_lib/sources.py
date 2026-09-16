"""Locate the reference-models checkout and record where the data came from."""
from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

from . import BuildError

SOURCE_FILES = {
    "value_chain": "pharma-value-chain-model/Pharma_Value_Chain_Model.md",
    "competence": "competency-model/PDS_Competence_Model_Full_Rethought.md",
    "rubric": "competency-model/Level_Rubric.md",
    "pedagogy": "pedagogic-practices/Pedagogic_Practices.md",
    "vocab": "vocab",
}


@dataclass
class Provenance:
    repo: str
    sha: str
    short_sha: str
    commit_date: str
    dirty: bool
    files: dict = field(default_factory=dict)  # key -> {"path", "commit", "date"}


def resolve_models_path(arg: str | None, website_root: Path) -> Path:
    raw = arg or os.environ.get("CPDSE_REFERENCE_MODELS") or str(website_root.parent / "cpdse-reference-models")
    path = Path(raw).expanduser().resolve()
    if not (path / "vocab" / "stages.csv").is_file():
        raise BuildError(
            f"No cpdse-reference-models checkout at {path}. "
            "Pass --models PATH or set CPDSE_REFERENCE_MODELS."
        )
    return path


def _git(repo: Path, *args: str) -> str:
    try:
        res = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        raise BuildError(f"git {' '.join(args)} failed in {repo}: {exc}") from exc
    return res.stdout.strip()


def provenance(repo: Path, allow_dirty: bool) -> Provenance:
    sha = _git(repo, "rev-parse", "HEAD")
    status = _git(repo, "status", "--porcelain")
    if status and not allow_dirty:
        raise BuildError(
            f"{repo} has uncommitted changes, so the output could not be traced to a commit.\n"
            f"{status}\nCommit them, or rebuild with --allow-dirty for a local preview."
        )
    prov = Provenance(
        repo="CPDSE/cpdse-reference-models",
        sha=sha,
        short_sha=sha[:7],
        commit_date=_git(repo, "log", "-1", "--format=%cs"),
        dirty=bool(status),
    )
    for key, rel_path in SOURCE_FILES.items():
        out = _git(repo, "log", "-1", "--format=%h %cs", "--", rel_path)
        commit, _, date = out.partition(" ")
        prov.files[key] = {"path": rel_path, "commit": commit, "date": date}
    return prov


def run_vocab_validator(repo: Path) -> None:
    script = repo / "scripts" / "validate-vocab.py"
    if not script.is_file():
        raise BuildError(f"Missing {script}")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, env=env)
    if res.returncode != 0:
        raise BuildError(f"validate-vocab.py failed in the models repo:\n{res.stdout}{res.stderr}")
