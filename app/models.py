from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time


@dataclass(frozen=True)
class ClassSession:
    name: str
    name_en: str
    start: time
    end: time
    room: str
    day: str


@dataclass(frozen=True)
class ScheduleConfig:
    semester_start: date
    semester_end: date
    timezone: str
    skip_dates: list[date] = field(default_factory=list)
    reminder_offsets: list[int] = field(default_factory=lambda: [10, 5, 1, 0])
    classes: dict[str, list[ClassSession]] = field(default_factory=dict)
