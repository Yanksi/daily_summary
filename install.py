#!/usr/bin/env python3
"""Install Daily Summary skills globally to ~/.claude/"""

import shutil
import sys
from pathlib import Path

SKILLS = [
    "summarize-to-notion",
    "summarize-to-notion-personal",
    "configure-notion",
    "weekly-summary",
]

def main():
    src = Path(__file__).resolve().parent / ".claude"
    dest = Path.home() / ".claude"

    if not src.exists():
        print(f"Error: source directory not found: {src}", file=sys.stderr)
        sys.exit(1)

    # Install skills
    for skill in SKILLS:
        skill_src = src / "skills" / skill
        skill_dest = dest / "skills" / skill
        if skill_dest.exists():
            shutil.rmtree(skill_dest)
        shutil.copytree(skill_src, skill_dest)
        print(f"  Installed skill: {skill}")

    # Install config (don't overwrite if already configured)
    config_dest = dest / "config"
    config_dest.mkdir(parents=True, exist_ok=True)
    config_file = config_dest / "notion-config.json"
    if config_file.exists():
        print(f"  Config already exists, skipping: {config_file}")
    else:
        shutil.copy2(src / "config" / "notion-config.json", config_file)
        print(f"  Installed config: {config_file}")

    print(f"\nDone! Skills installed to {dest / 'skills'}")
    print("Open Claude Code and type / to verify the commands are available.")

if __name__ == "__main__":
    main()
