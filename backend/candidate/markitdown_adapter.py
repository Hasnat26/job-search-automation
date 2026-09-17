from __future__ import annotations

import os
import shlex
import subprocess
import sys
from pathlib import Path


class MarkItDownError(RuntimeError):
    pass


def _command() -> list[str]:
    """Resolve an external MarkItDown installation without embedding its code."""
    configured = os.getenv("MARKITDOWN_COMMAND")
    if configured:
        return shlex.split(configured, posix=False)

    root = os.getenv("MARKITDOWN_ROOT")
    if root:
        package_src = Path(root) / "packages" / "markitdown" / "src"
        if package_src.exists():
            return [sys.executable, "-m", "markitdown"]

    return ["markitdown"]


def convert_to_markdown(source: str | Path, output: str | Path) -> dict:
    """Use the standalone MarkItDown repo/tool to create a Markdown artifact."""
    source_path = Path(source).expanduser().resolve()
    output_path = Path(output).expanduser().resolve()
    if not source_path.is_file():
        raise FileNotFoundError(source_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = _command() + [str(source_path), "-o", str(output_path)]
    env = os.environ.copy()
    root = os.getenv("MARKITDOWN_ROOT")
    if root:
        package_src = Path(root) / "packages" / "markitdown" / "src"
        if package_src.exists():
            env["PYTHONPATH"] = str(package_src) + os.pathsep + env.get("PYTHONPATH", "")

    try:
        completed = subprocess.run(
            command,
            cwd=root if root and Path(root).is_dir() else None,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        raise MarkItDownError(
            "Could not start MarkItDown. Install the MarkItDown repo/package or set MARKITDOWN_COMMAND."
        ) from exc

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout).strip()
        raise MarkItDownError(f"MarkItDown conversion failed (exit {completed.returncode}): {detail}")
    if not output_path.is_file():
        raise MarkItDownError("MarkItDown reported success but did not create the Markdown output")

    return {
        "source_file": str(source_path),
        "markdown_file": str(output_path),
        "markdown_characters": len(output_path.read_text(encoding="utf-8")),
        "converter": "external-markitdown",
    }


def read_markdown(path: str | Path) -> str:
    markdown_path = Path(path).expanduser().resolve()
    if not markdown_path.is_file():
        raise FileNotFoundError(markdown_path)
    text = markdown_path.read_text(encoding="utf-8", errors="replace")
    if len(text.strip()) < 50:
        raise MarkItDownError("Markdown input is empty or too short")
    return text
