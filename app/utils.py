from __future__ import annotations

from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

WEEKDAY_NAMES = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


def now_in_tz(tz_name: str) -> datetime:
    return datetime.now(ZoneInfo(tz_name))


def day_name_for_date(d: date) -> str:
    return WEEKDAY_NAMES[d.weekday()]


def class_datetime(d: date, t: time, tz_name: str) -> datetime:
    return datetime.combine(d, t, tzinfo=ZoneInfo(tz_name))


def reminder_key(d: date, start: time, room: str, offset: int) -> str:
    return f"{d.isoformat()}_{start.strftime('%H:%M')}_{room}_{offset}"


def reminder_label(offset: int) -> str:
    if offset == 0:
        return "השיעור מתחיל עכשיו!"
    if offset == 1:
        return "מתחיל בעוד דקה אחת"
    return f"מתחיל בעוד {offset} דקות"


OFFSET_COLORS = {
    10: 0x3498DB,
    5: 0xE67E22,
    1: 0xE74C3C,
    0: 0x2ECC71,
}


def embed_color(offset: int) -> int:
    return OFFSET_COLORS.get(offset, 0x95A5A6)
