# AI/ML Daily Learning Bot -- Setup Guide
# Deployed via Hermes cron (local WSL session)

## Step 1: Create your Telegram Bot

1. Open Telegram -> search for @BotFather
2. Send: /newbot
3. Choose a name: "AI ML Daily Tutor" (or anything)
4. Choose a username: e.g. yourname_aiml_bot
5. BotFather gives you a TOKEN -- save it

## Step 2: Get your Chat ID

1. Start a conversation with your new bot (send it any message)
2. Open this URL in browser (replace YOUR_TOKEN):
   https://api.telegram.org/botYOUR_TOKEN/getUpdates
3. Find "chat":{"id": XXXXXXXX} -- that's your CHAT_ID

## Step 3: Configure environment

Copy the example env file and fill in your values:

```bash
cp .env.example .env
# Edit .env with your actual values:
#   TELEGRAM_BOT_TOKEN=123456:ABC...
#   TELEGRAM_CHAT_ID=123456789
```

Never commit `.env` -- it's listed in `.gitignore`.

## Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Test manually

```bash
# Sets up current_day.txt at day 1 and sends Day 1 via Telegram
python3 bot.py

# Send a specific day (counter unchanged):
python3 bot.py --day 1
```

## Step 6: Schedule with Hermes cron (8 AM daily)

Use Hermes cron instead of system crontab. Create the job from the project directory:

```bash
cd ~/projects/ai-tools/ai-ml-daily-bot
```

Then ask Hermes:

> Create a cron job named "ai-ml-daily-lesson" that runs at 8 AM daily.
> It should cd to ~/projects/ai-tools/ai-ml-daily-bot and run `python3 bot.py`.
> Enable only the terminal toolset. Deliver notifications to Telegram.

Or set it up manually via `cronjob action='create'`:

```
schedule: "0 8 * * *"
workdir: ~/projects/ai-tools/ai-ml-daily-bot
prompt: Run `python3 bot.py`. Report: what day was sent, or if completed, or if error.
deliver: telegram:<CHAT_ID>
enabled_toolsets: ["terminal"]
```

The bot tracks progress in `current_day.txt` in the workdir.
It sends the next lesson each day until day 30, then stops.

## Manual controls

```bash
# Re-send a specific day (counter unchanged):
python3 bot.py --day 5

# Check current progress:
cat current_day.txt

# Reset to start over:
echo "1" > current_day.txt
```

## Notes

- 30 days total, one lesson per cron run
- After Day 30, sends a completion message and stops
- Logs go to bot.log in the project directory
- If a send fails, the counter is NOT incremented -- it retries next run
- State file (current_day.txt) is gitignored -- each machine tracks independently
