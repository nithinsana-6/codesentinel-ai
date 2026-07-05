"""Make local src-layout imports work before editable installation.

Python automatically imports ``sitecustomize`` when it is present on
``sys.path``. Keeping this tiny helper at the repository root lets contributors
run ``python -m unittest discover -s tests`` immediately after cloning.
"""

from __future__ import annotations

import sys
from pathlib import Path


SRC = Path(__file__).resolve().parent / "src"
if SRC.exists() and str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
