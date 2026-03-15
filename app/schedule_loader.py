from __future__ import annotations

import json
import logging
from datetime import date, time
from pathlib import Path

from app.models import ClassSession, ScheduleConfig

logger = logging.getLogger(__name__)


def _parse_time(raw: str) -> time:
    parts = raw.strip().split(":")
    return time(int(parts[0]), int(parts[1]))


def load_schedule(path: Path) -> ScheduleConfig:
    logger.info("Loading schedule from %s", path)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    semester = data["semester"]
    classes: dict[str, list[ClassSession]] = {}

    for day_name, sessions in data.get("classes", {}).items():
        day_list: list[ClassSession] = []
        for s in sessions:
            day_list.append(
                ClassSession(
                    name=s["name"],
                    name_en=s["name_en"],
                    start=_parse_time(s["start"]),
                    end=_parse_time(s["end"]),
                    room=s["room"],
                    day=day_name,
                )
            )
        classes[day_name] = day_list

    skip_dates = [date.fromisoformat(d) for d in data.get("skip_dates", [])]
    offsets = data.get("reminder_offsets_minutes", [10, 5, 1, 0])

    cfg = ScheduleConfig(
        semester_start=date.fromisoformat(semester["start_date"]),
        semester_end=date.fromisoformat(semester["end_date"]),
        timezone=data.get("timezone", "Asia/Jerusalem"),
        skip_dates=skip_dates,
        reminder_offsets=sorted(offsets, reverse=True),
        classes=classes,
    )
    logger.info(
        "Schedule loaded: %d day(s), semester %s to %s, %d skip date(s)",
        len(classes),
        cfg.semester_start,
        cfg.semester_end,
        len(skip_dates),
    )
    return cfg
