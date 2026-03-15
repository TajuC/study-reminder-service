from __future__ import annotations

import signal
import sys
import time
import logging

from app.config import load_config
from app.logging_setup import setup_logging
from app.reminder_engine import ReminderEngine
from app.schedule_loader import load_schedule
from app.state_store import StateStore
from app.webhook import WebhookClient

logger = logging.getLogger(__name__)

_running = True


def _handle_signal(signum, _frame):
    global _running
    logger.info("Received signal %s, shutting down…", signum)
    _running = False


def main() -> None:
    global _running

    config = load_config()
    setup_logging(config.log_dir, config.log_level)

    logger.info("=" * 60)
    logger.info("Study Reminder Service starting")
    logger.info("Dry-run: %s | Poll: %ds | TZ: %s", config.dry_run, config.poll_interval_seconds, config.timezone)
    logger.info("=" * 60)

    if not config.dry_run and not config.webhook_url:
        logger.error("DISCORD_WEBHOOK_URL is not set and DRY_RUN is false. Exiting.")
        sys.exit(1)

    schedule = load_schedule(config.schedule_path)
    state = StateStore(config.db_path)
    webhook = WebhookClient(config.webhook_url, dry_run=config.dry_run)
    engine = ReminderEngine(config, schedule, state, webhook)

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    logger.info("Service is running. Press Ctrl+C to stop.")

    try:
        while _running:
            try:
                engine.tick()
            except Exception:
                logger.exception("Error during tick")
            time.sleep(config.poll_interval_seconds)
    finally:
        state.close()
        webhook.close()
        logger.info("Service stopped cleanly.")


if __name__ == "__main__":
    main()
