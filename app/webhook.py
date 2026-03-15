from __future__ import annotations

import json
import logging
import time
from typing import Any

import requests

from app.models import ClassSession
from app.utils import embed_color, reminder_label

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BACKOFF_BASE = 2


class WebhookClient:
    def __init__(self, webhook_url: str, dry_run: bool = False) -> None:
        self._url = webhook_url
        self._dry_run = dry_run
        self._session = requests.Session()
        self._session.headers["Content-Type"] = "application/json; charset=utf-8"

    def send_reminder(self, cls: ClassSession, offset: int) -> bool:
        payload = self._build_payload(cls, offset)

        if self._dry_run:
            logger.info(
                "[DRY-RUN] Would send webhook:\n%s",
                json.dumps(payload, ensure_ascii=False, indent=2),
            )
            return True

        return self._send_with_retry(payload)

    def _build_payload(self, cls: ClassSession, offset: int) -> dict[str, Any]:
        time_range = (
            f"{cls.start.strftime('%H:%M')}-{cls.end.strftime('%H:%M')}"
        )

        title = "📚 תזכורת לשיעור" if offset > 0 else "🎓 השיעור מתחיל!"

        fields = [
            {"name": "שיעור", "value": cls.name, "inline": True},
            {"name": "שעה", "value": time_range, "inline": True},
            {"name": "חדר", "value": cls.room, "inline": True},
            {"name": "⏰ תזכורת", "value": reminder_label(offset), "inline": False},
        ]

        embed: dict[str, Any] = {
            "title": title,
            "color": embed_color(offset),
            "fields": fields,
            "footer": {"text": cls.name_en},
        }

        return {"embeds": [embed]}

    def _send_with_retry(self, payload: dict[str, Any]) -> bool:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = self._session.post(
                    self._url,
                    data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                    timeout=10,
                )
                if resp.status_code == 429:
                    retry_after = resp.json().get("retry_after", BACKOFF_BASE)
                    logger.warning(
                        "Rate-limited by Discord, retrying in %.1fs", retry_after
                    )
                    time.sleep(retry_after)
                    continue

                resp.raise_for_status()
                logger.info("Webhook sent successfully (attempt %d)", attempt)
                return True

            except requests.RequestException as exc:
                wait = BACKOFF_BASE ** attempt
                logger.warning(
                    "Webhook attempt %d/%d failed: %s — retrying in %ds",
                    attempt,
                    MAX_RETRIES,
                    exc,
                    wait,
                )
                time.sleep(wait)

        logger.error("Webhook failed after %d attempts", MAX_RETRIES)
        return False

    def close(self) -> None:
        self._session.close()
