import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
IGNORED_DIRS = {
    ".git",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
    "venv",
}
CHECKED_SUFFIXES = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".txt",
    ".yml",
    ".yaml",
}
MARKERS = ("TO" + "DO", "FIX" + "ME")
SELF_PATH = Path(__file__).resolve()


def iter_project_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    files: list[Path] = []
    for relative_path in result.stdout.splitlines():
        path = REPO_ROOT / relative_path
        if not path.is_file() or path == SELF_PATH:
            continue
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if path.suffix not in CHECKED_SUFFIXES:
            continue
        files.append(path)
    return sorted(files)


def test_repository_contains_no_action_markers():
    offenders: list[str] = []

    for path in iter_project_files():
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if any(marker in line for marker in MARKERS):
                offenders.append(f"{path.relative_to(REPO_ROOT)}:{line_number}")

    marker_summary = "/".join(MARKERS)
    assert offenders == [], f"Found {marker_summary} markers in:\n" + "\n".join(offenders)
