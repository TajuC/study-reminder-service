from __future__ import annotations

import logging
from datetime import timedelta

from app.config import Config
from app.models import ClassSession, ScheduleConfig
from app.state_store import StateStore
from app.utils import class_datetime, day_name_for_date, now_in_tz, reminder_key
from app.webhook import WebhookClient

logger = logging.getLogger(__name__)


class ReminderEngine:
    def __init__(
        self,
        config: Config,
        schedule: ScheduleConfig,
        state: StateStore,
        webhook: WebhookClient,
    ) -> None:
        self._config = config
        self._schedule = schedule
        self._state = state
        self._webhook = webhook

    def tick(self) -> None:
        now = now_in_tz(self._schedule.timezone)
        today = now.date()

        if today < self._schedule.semester_start:
            return
        if today > self._schedule.semester_end:
            return
        if today in self._schedule.skip_dates:
            return

        day = day_name_for_date(today)
        classes = self._schedule.classes.get(day, [])
        if not classes:
            return

        for cls in classes:
            for offset in self._schedule.reminder_offsets:
                self._check_and_send(cls, offset, now, today)

        self._state.cleanup_old(days=7)

    def _check_and_send(self, cls, offset, now, today) -> None:
        key = reminder_key(today, cls.start, cls.room, offset)

        if self._state.is_sent(key):
            return

        send_at = class_datetime(today, cls.start, self._schedule.timezone) - timedelta(
            minutes=offset
        )

        grace = timedelta(
            seconds=(
                self._config.grace_seconds_start
                if offset == 0
                else self._config.grace_seconds_pre
            )
        )

        if now < send_at:
            return
        if now >= send_at + grace:
            logger.debug("Window passed for %s, skipping", key)
            self._state.mark_sent(key, cls.name, offset, now)
            return

        logger.info("Sending reminder: %s", key)
        success = self._webhook.send_reminder(cls, offset)

        if success:
            self._state.mark_sent(key, cls.name, offset, now)
        else:
            logger.error("Failed to send %s — will retry next tick", key)
