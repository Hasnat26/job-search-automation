from pathlib import Path

from backend.candidate.markitdown_adapter import _command


def test_command_resolves_markitdown_from_current_python_environment():
    command = _command()

    executable = Path(command[0])

    if executable.name.lower() == "markitdown.exe":
        assert executable.is_file()
    else:
        assert command == ["markitdown"]
