#!/usr/bin/env python3
"""Validate the illustration Agent Skills for structural consistency.

Run:  python tools/validate_skill.py
Exit: 0 = all checks pass (warnings allowed); 1 = at least one error.

This automates the consistency checks that manual review kept catching:
  - frontmatter present + parseable + `name` matches the directory
  - every references/<file>.md mentioned in SKILL.md actually exists (no dangling links)
  - no orphan reference files (warn)
  - bring-your-own-IP invariant intact for any skill that ships
    references/custom-ip-template.md: qa-checklist exists, its must-pass list is
    character-agnostic (not hardcoded to one mascot), and the "perform(s) the core
    action" clause is present
  - no stray Chinese / Japanese sentences in an English ("-en") skill body

Requires Python 3.8+ (annotations are deferred). Stdlib only — no third-party deps.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Windows consoles default to a legacy codec (cp950/cp1252); force UTF-8 so the
# report can print any skill content (including CJK findings) without crashing.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO = Path(__file__).resolve().parent.parent

# 4+ consecutive CJK ideographs (Basic + Ext-A + Compatibility) or Japanese kana =
# a sentence, not a 2-char name like 小黑.
CJK_RUN = re.compile(r"[぀-ヿ㐀-䶿一-鿿豈-﫿]{4,}")

# Reference files created at runtime (by the user / agent); absence is OK and they
# must not trigger orphan warnings either. (Their *-template.md scaffolds are
# committed files, checked normally by the mention-scan — do NOT add those here.)
RUNTIME_REFS = {"custom-ip.md", "manifest.md", "custom-style.md"}

errors: list[str] = []
warnings: list[str] = []


def err(skill: str, msg: str) -> None:
    errors.append(f"[{skill}] {msg}")


def warn(skill: str, msg: str) -> None:
    warnings.append(f"[{skill}] {msg}")


def read(path: Path, skill: str, label: str) -> str | None:
    """Read UTF-8 text; record an error and return None instead of crashing the run."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        err(skill, f"{label} could not be read as UTF-8: {exc}")
        return None


def parse_frontmatter(text: str) -> dict | None:
    """Minimal YAML-frontmatter parser (top-level single-line key: value). None if absent."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    data: dict[str, str] = {}
    for line in text[3:end].splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            data[m.group(1)] = m.group(2).strip()
    return data


def find_skill_dirs() -> list[Path]:
    dirs = sorted(p.parent for p in REPO.glob("*/SKILL.md"))
    # Guard: a nested layout (e.g. skills/<name>/SKILL.md) would be silently ignored.
    nested = [p for p in REPO.glob("*/*/SKILL.md")]
    if nested:
        warn("(repo)", "SKILL.md found below depth 1 are NOT validated: "
                       + ", ".join(str(p.relative_to(REPO)) for p in nested))
    return dirs


def check_skill(d: Path) -> None:
    name = d.name
    refs_dir = d / "references"
    text = read(d / "SKILL.md", name, "SKILL.md")
    if text is None:
        return

    # 1. frontmatter present, name matches dir, description non-trivial
    fm = parse_frontmatter(text)
    if fm is None:
        err(name, "SKILL.md has no parseable YAML frontmatter (--- ... ---)")
        return
    if not fm.get("name"):
        err(name, "frontmatter missing 'name'")
    elif fm["name"] != name:
        err(name, f"frontmatter name '{fm['name']}' != directory name '{name}'")
    if not fm.get("description"):
        err(name, "frontmatter missing 'description'")
    elif len(fm["description"]) < 40:
        warn(name, f"description is short ({len(fm['description'])} chars) — weak trigger surface")

    # 2. every referenced references/<file>.md exists (runtime-created ones exempt)
    mentioned = {r.lower() for r in re.findall(r"references/([A-Za-z0-9_.-]+\.md)", text, re.I)}
    for ref in sorted(mentioned):
        if ref in RUNTIME_REFS:
            continue
        if not (refs_dir / ref).exists():
            err(name, f"SKILL.md references references/{ref} but it does not exist")

    # 3. orphan reference files (exist but never mentioned, and not runtime-created) -> warn
    if refs_dir.is_dir():
        for ref_file in sorted(refs_dir.glob("*.md")):
            if ref_file.name.lower() not in mentioned and ref_file.name not in RUNTIME_REFS:
                warn(name, f"references/{ref_file.name} exists but is not mentioned in SKILL.md (orphan)")

    # 4. bring-your-own-IP invariant (only for skills that ship the custom-ip mechanism)
    if (refs_dir / "custom-ip-template.md").exists():
        if not (re.search(r"performs?\s+the\s+core", text, re.I) or "核心动作" in text):
            err(name, "BYO-IP skill: SKILL.md is missing the 'perform(s) the core action' / '承担核心动作' invariant")
        qa = refs_dir / "qa-checklist.md"
        if not qa.exists():
            err(name, "BYO-IP skill: references/qa-checklist.md is missing (cannot verify the invariant)")
        else:
            qa_text = read(qa, name, "references/qa-checklist.md")
            if qa_text is not None:
                qa_plain = re.sub(r"[*_`]", "", qa_text)  # strip inline markdown formatting
                if re.search(r"^\s*-\s*(xiaohei is present|有小黑)", qa_plain, re.M | re.I):
                    err(name, "BYO-IP skill: qa-checklist must-pass hardcodes the default mascot (use 'active IP character' / '当前 IP 角色')")
                if not ("active IP character" in qa_text or "当前 IP" in qa_text or "当前IP" in qa_text):
                    warn(name, "BYO-IP skill: qa-checklist never says 'active IP character' / '当前 IP 角色' — verify must-pass is character-agnostic")

    # 5. no Chinese / Japanese sentences in an English skill body
    if name.endswith("-en"):
        md_files = [d / "SKILL.md"]
        if refs_dir.is_dir():
            md_files += sorted(refs_dir.glob("*.md"))
        for md in md_files:
            body = read(md, name, str(md.relative_to(d)))
            if body is None:
                continue
            runs = CJK_RUN.findall(body)
            if runs:
                err(name, f"{md.relative_to(d)} has CJK sentence(s) in an English skill: {runs[:3]}")


def main() -> int:
    skills = find_skill_dirs()
    if not skills:
        print("No skills found (no */SKILL.md under repo root).", file=sys.stderr)
        return 1
    for d in skills:
        check_skill(d)

    print(f"Validated {len(skills)} skill(s): {', '.join(s.name for s in skills)}")
    for w in warnings:
        print(f"  WARN  {w}")
    for e in errors:
        print(f"  ERROR {e}")
    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"\nOK: 0 errors, {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
