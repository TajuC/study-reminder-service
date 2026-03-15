from __future__ import annotations

import logging
import sqlite3
import time as _time
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class StateStore:
    _CLEANUP_INTERVAL = 3600

    def __init__(self, db_path: Path) -> None:
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(str(db_path), isolation_level=None)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sent_reminders (
                reminder_key  TEXT PRIMARY KEY,
                sent_at       TEXT NOT NULL,
                class_name    TEXT,
                offset_minutes INTEGER
            )
            """
        )
        self._last_cleanup = 0.0
        logger.info("State store initialised at %s", db_path)

    def is_sent(self, key: str) -> bool:
        row = self._conn.execute(
            "SELECT 1 FROM sent_reminders WHERE reminder_key = ?", (key,)
        ).fetchone()
        return row is not None

    def mark_sent(
        self, key: str, class_name: str, offset: int, now: datetime
    ) -> None:
        self._conn.execute(
            """
            INSERT OR IGNORE INTO sent_reminders
                (reminder_key, sent_at, class_name, offset_minutes)
            VALUES (?, ?, ?, ?)
            """,
            (key, now.isoformat(), class_name, offset),
        )
        logger.debug("Marked sent: %s", key)

    def cleanup_old(self, days: int = 7) -> None:
        now_mono = _time.monotonic()
        if now_mono - self._last_cleanup < self._CLEANUP_INTERVAL:
            return
        cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
        cur = self._conn.execute(
            "DELETE FROM sent_reminders WHERE sent_at < ?", (cutoff,)
        )
        if cur.rowcount:
            logger.info("Cleaned up %d old reminder record(s)", cur.rowcount)
        self._last_cleanup = now_mono

    def close(self) -> None:
        self._conn.close()
