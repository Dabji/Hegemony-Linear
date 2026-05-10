"""Launcher for the Hegemony Streamlit application.

This file supports two entry modes:
1. ``python app.py``: boots Streamlit using the current interpreter when
   possible, or falls back to the known pgAdmin Python installation.
2. ``streamlit run app.py``: renders the app directly inside Streamlit.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
TARGET_APP = PROJECT_ROOT / "hegemony_calculator" / "ui" / "app.py"
FALLBACK_PYTHON = Path(r"C:\Program Files\PostgreSQL\18\pgAdmin 4\python\python.exe")


def _ensure_project_root() -> None:
    """Ensure the project root is available for local imports."""

    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))


def _running_inside_streamlit() -> bool:
    """Return whether this file is being executed by Streamlit."""

    return any(module_name.startswith("streamlit.runtime") for module_name in sys.modules)


def _run_with_streamlit_cli() -> int:
    """Launch Streamlit programmatically with the current interpreter."""

    from streamlit.web import cli as stcli

    sys.argv = ["streamlit", "run", str(TARGET_APP)]
    return stcli.main()


def _run_with_fallback_python() -> int:
    """Launch Streamlit with the known pgAdmin Python interpreter."""

    if not FALLBACK_PYTHON.exists():
        return 1

    command = [str(FALLBACK_PYTHON), "-m", "streamlit", "run", str(TARGET_APP)]
    completed = subprocess.run(command, check=False)
    return completed.returncode


def main() -> None:
    """Run the app either as a Streamlit page or via the Streamlit CLI."""

    _ensure_project_root()

    if _running_inside_streamlit():
        from hegemony_calculator.ui.app import main as streamlit_main

        streamlit_main()
        return

    if importlib.util.find_spec("streamlit") is not None:
        raise SystemExit(_run_with_streamlit_cli())

    fallback_code = _run_with_fallback_python()
    if fallback_code == 0:
        raise SystemExit(0)

    message = (
        "Streamlit no esta instalado en el Python actual y no se pudo usar "
        "el Python alternativo de pgAdmin. Ejecuta:\n"
        f'"{FALLBACK_PYTHON}" -m pip install --user -r requirements.txt\n'
        f'"{FALLBACK_PYTHON}" -m streamlit run app.py'
    )
    raise SystemExit(message)


if __name__ == "__main__":
    main()
