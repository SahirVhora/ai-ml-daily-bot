# AI/ML Daily Learning Bot -- Setup Guide

Deployed via GitHub Actions (runs daily at 8 AM in the cloud).
No need to keep your laptop on.

## Step 1: Create your Telegram Bot

1. Open Telegram -> search for @BotFather
2. Send: /newbot
3. Choose a name: `AIDailyTutor_bot` (or anything)
4. BotFather gives you a TOKEN -- save it

## Step 2: Get your Chat ID

1. Start a conversation with your new bot (send it any message)
2. Open this URL in browser (replace YOUR_TOKEN):
   https://api.telegram.org/botYOUR_TOKEN/getUpdates
3. Find `"chat":{"id": XXXXXXXX}` -- that's your CHAT_ID

## Step 3: Add secrets to GitHub

In your repo's Settings -> Secrets and variables -> Actions, add:

| Secret | Value |
|--------|-------|
| `TELEGRAM_BOT_TOKEN` | The token from BotFather |
| `TELEGRAM_CHAT_ID` | Your chat ID (numeric) |

Never commit these to the repo -- the workflow reads them from GitHub secrets.

## Step 4: Trigger the workflow

The workflow runs automatically at 8 AM daily.
You can also trigger it manually from the GitHub UI:

1. Go to your repo -> Actions -> "Daily AI/ML Lesson" -> Run workflow

## How state works

The bot tracks progress in `current_day.txt`. After each successful send, the
workflow commits the updated counter back to the repo. If a send fails, the
counter is NOT incremented and it retries the next day.

## Manual controls

Trigger a replay of any day from your terminal:

```bash
python3 bot.py --day 5
```

Env vars required for manual runs:
```bash
export TELEGRAM_BOT_TOKEN=***
export TELEGRAM_CHAT_ID=***
python3 bot.py --day 5
```

## Course structure

- 30 days, one lesson per day
- Covers: AI fundamentals -> ML -> Neural Networks -> Transformers ->
  RAG -> Agents -> MLOps -> Ethics -> Enterprise AI
- After Day 30 sends a completion message and stops silently
