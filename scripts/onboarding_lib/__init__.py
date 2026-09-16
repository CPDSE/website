"""Build library for the CPDSE Reference Models onboarding site.

The site lives in ``reference-models/`` in the website repo and is generated
from a local checkout of the private ``CPDSE/cpdse-reference-models`` repo by
``scripts/build_onboarding.py``. Everything here is stdlib-only and runs on
Python 3.9.
"""


class BuildError(Exception):
    """A problem in the source data or hand-authored inputs that must stop the build."""
