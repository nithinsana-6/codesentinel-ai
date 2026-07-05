"""Local development package shim.

The project uses a professional ``src/`` layout. This shim lets users run
``python -m codesentinel.cli`` directly from the repository root before doing an
editable install.
"""

from __future__ import annotations

from pathlib import Path


_SRC_PACKAGE = Path(__file__).resolve().parents[1] / "src" / "codesentinel"
__path__ = [str(_SRC_PACKAGE)]

try:
    from . import __version__ as __version__
except ImportError:
    __version__ = "0.1.0"
