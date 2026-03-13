import pathlib
import re
import subprocess
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MARKER_WORDS = ("TO" + "DO", "FIX" + "ME")
MARKER_PATTERN = re.compile(r"\b(?:" + "|".join(MARKER_WORDS) + r")\b")
EXCLUDED_PATH_PARTS = {".git", ".pytest_cache", ".venv", "__pycache__"}


def tracked_files():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    files = []
    for relative_path in result.stdout.splitlines():
        path = ROOT / relative_path
        if any(part in EXCLUDED_PATH_PARTS for part in path.parts):
            continue
        if path.is_file():
            files.append(path)
    return files


class NoTodoFixmeCommentsTest(unittest.TestCase):
    def test_tracked_files_do_not_contain_todo_or_fixme_markers(self):
        matches = []

        for path in tracked_files():
            contents = path.read_text(encoding="utf-8")
            for line_number, line in enumerate(contents.splitlines(), start=1):
                if MARKER_PATTERN.search(line):
                    matches.append(f"{path.relative_to(ROOT)}:{line_number}: {line.strip()}")

        failure_message = "Found " + "/".join(MARKER_WORDS) + " markers:\n" + "\n".join(matches)
        self.assertEqual(matches, [], failure_message)


if __name__ == "__main__":
    unittest.main()
