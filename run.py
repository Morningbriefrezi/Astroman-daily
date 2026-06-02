#!/usr/bin/env python3
"""Astroman Business Hub — marketing, daily routine, CEO briefs, product scout."""

from __future__ import annotations

import os
import runpy
import subprocess
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_python(relative: str) -> None:
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    os.chdir(ROOT)
    script = ROOT / relative
    print(f"Running {script}")
    runpy.run_path(str(script), run_name="__main__")


def run_product_scout() -> None:
    scout_dir = ROOT / "jobs" / "product_scout"
    os.chdir(scout_dir)
    if str(scout_dir) not in sys.path:
        sys.path.insert(0, str(scout_dir))
    runpy.run_path(str(scout_dir / "main.py"), run_name="__main__")


def run_marketing() -> None:
    marketing_dir = ROOT / "jobs" / "marketing"
    subprocess.run(["npm", "install", "--silent"], cwd=marketing_dir, check=True)
    env = os.environ.copy()
    env.setdefault("DAY", __import__("datetime").datetime.utcnow().strftime("%A"))
    env.setdefault("TELEGRAM_TOKEN", env.get("TELEGRAM_BOT_TOKEN", ""))
    env.setdefault("CHAT_ID", env.get("TELEGRAM_CHAT_ID", ""))
    env.setdefault("OPENAI_KEY", env.get("OPENAI_API_KEY", ""))
    subprocess.run(["node", "generate.js"], cwd=marketing_dir, env=env, check=True)


def main() -> None:
    job = os.getenv("JOB", "").strip()
    try:
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
    except SystemExit:
        raise
    except subprocess.CalledProcessError as exc:
        print(f"Marketing job failed: {exc}", file=sys.stderr)
        raise SystemExit(exc.returncode)
    except Exception:
        traceback.print_exc()
        raise SystemExit(1)


if __name__ == "__main__":
    main()
