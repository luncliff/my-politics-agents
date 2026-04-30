"""Lint YAML frontmatter in agents/, skills/, .github/prompts/.

규칙:
- 모든 *.agent.md / SKILL.md / *.prompt.md는 YAML frontmatter로 시작.
- 필수 키: description.
- *.agent.md / SKILL.md는 추가로 name, applyTo, tools 권장.
"""
from __future__ import annotations
import sys
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]

TARGETS = [
    ("agents/*.agent.md",        ["description", "name"]),
    ("skills/*/SKILL.md",        ["description", "name"]),
    (".github/prompts/*.prompt.md", ["description"]),
]


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    return yaml.safe_load(text[3:end])


def main() -> int:
    errors: list[str] = []
    checked = 0
    for pattern, required in TARGETS:
        for path in ROOT.glob(pattern):
            checked += 1
            text = path.read_text(encoding="utf-8")
            data = parse_frontmatter(text)
            if data is None:
                errors.append(f"{path}: missing or invalid YAML frontmatter")
                continue
            for key in required:
                if key not in data or data[key] in (None, ""):
                    errors.append(f"{path}: missing required key '{key}'")
    if errors:
        print(f"checked {checked} files, {len(errors)} error(s):")
        for e in errors:
            print("  -", e)
        return 1
    print(f"ok: {checked} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
