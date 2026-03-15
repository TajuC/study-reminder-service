from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Config:
    webhook_url: str
    dry_run: bool
    poll_interval_seconds: int
    log_level: str
    log_dir: Path
    db_path: Path
    schedule_path: Path
    timezone: str
    grace_seconds_pre: int
    grace_seconds_start: int


def load_config(env_path: Path | None = None) -> Config:
    load_dotenv(env_path or BASE_DIR / ".env")

    return Config(
        webhook_url=os.environ.get("DISCORD_WEBHOOK_URL", ""),
        dry_run=os.environ.get("DRY_RUN", "false").lower() in ("true", "1", "yes"),
        poll_interval_seconds=int(os.environ.get("POLL_INTERVAL_SECONDS", "20")),
        log_level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        log_dir=BASE_DIR / "logs",
        db_path=BASE_DIR / "data" / "reminders.db",
        schedule_path=BASE_DIR / "schedule.json",
        timezone="Asia/Jerusalem",
        grace_seconds_pre=90,
        grace_seconds_start=150,
    )
