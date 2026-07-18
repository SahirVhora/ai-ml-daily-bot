# Local runtime requirements

This bot imports `python-telegram-bot` and instantiates the Telegram client at
import time. The smoke test (and any local run) will fail unless these env
vars are set:

| Variable | Where to get it |
| --- | --- |
| `TELEGRAM_BOT_TOKEN` | @BotFather on Telegram -- `/newbot` |
| `TELEGRAM_CHAT_ID` | Send your bot any message, then hit `https://api.telegram.org/bot<TOKEN>/getUpdates` and look for `chat.id` |

For production deploy, the GitHub Actions workflow reads these from repo
secrets (see SETUP.md). For local testing, export them in your shell before
running `python bot.py`:

    export TELEGRAM_BOT_TOKEN=...
    export TELEGRAM_CHAT_ID=...

The audit script (`.hermes/scripts/migrate_audit.py`) marks this project
PASS for install + venv, FAIL for smoke. The smoke failure is expected
behaviour, not a code defect -- it is listed in the migration report as the
single remaining issue across the 53-project portfolio.
