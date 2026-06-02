#!/usr/bin/env python3
"""Astroman Business Hub — marketing, daily routine, CEO briefs, product scout."""

from __future__ import annotations

import os
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_python(relative: str) -> None:
    script = ROOT / relative
    print(f"Running {script}")
    runpy.run_path(str(script), run_name="__main__")


def run_product_scout() -> None:
    scout_dir = ROOT / "jobs" / "product_scout"
    os.chdir(scout_dir)
    runpy.run_path(str(scout_dir / "main.py"), run_name="__main__")


def run_marketing() -> None:
    marketing_dir = ROOT / "jobs" / "marketing"
    subprocess.run(["npm", "install", "--silent"], cwd=marketing_dir, check=True)
    env = os.environ.copy()
    env.setdefault("DAY", __import__("datetime").datetime.utcnow().strftime("%A"))
    subprocess.run(["node", "generate.js"], cwd=marketing_dir, env=env, check=True)


def main() -> None:
    job = os.getenv("JOB", "").strip()
    if job == "astroman_daily":
        run_python("jobs/astroman_daily.py")
    elif job == "lisa_morning":
        os.environ["MODE"] = "morning"
        run_python("jobs/lisa.py")
    elif job == "lisa_evening":
        os.environ["MODE"] = "evening"
        run_python("jobs/lisa.py")
    elif job == "marketing":
        run_marketing()
    elif job == "product_scout":
        run_product_scout()
    else:
        raise SystemExit(
            "Set JOB to: astroman_daily, lisa_morning, lisa_evening, marketing, product_scout"
        )


if __name__ == "__main__":
    main()
