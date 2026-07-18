# AI/ML Daily Learning Bot

A Telegram bot that delivers a 30-day AI/ML curriculum, one lesson per day.

Designed to run as a scheduled job (GitHub Actions or cron) so lessons arrive automatically without keeping your laptop on.

## What it teaches

The 30-day curriculum covers:

- **Week 1**: AI fundamentals, supervised/unsupervised/reinforcement learning, data quality, linear regression, classification, overfitting/underfitting
- **Week 2**: Decision trees, random forests, SVMs, k-NN, k-means, neural networks, backpropagation, deep learning
- **Week 3**: CNNs, RNNs/LSTMs, Transformers, LLMs, embeddings, vector databases, RAG
- **Week 4**: Prompt engineering, AI agents, MLOps, AI ethics, generative AI, enterprise AI, RLHF, frontier models

## How it works

- Lessons are stored in `bot.py` as a 30-day curriculum.
- `current_day.txt` tracks which lesson to send next.
- Each run sends the current lesson and increments the counter.
- The GitHub Actions workflow commits the updated `current_day.txt` back to the repo after each run.
- When the curriculum finishes, the bot sends a completion message and stops silently on subsequent runs.

## Quick start

### Local manual run

1. Install dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

2. Set environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export TELEGRAM_CHAT_ID="your-chat-id"
```

3. Send a specific day:

```bash
.venv/bin/python bot.py --day 1
```

### Daily automated delivery

The `.github/workflows/` directory contains the GitHub Actions workflow that runs `bot.py` daily at 8 AM. See [SETUP.md](SETUP.md) for setup instructions.

> Note: Local smoke tests will fail without `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` set. This is expected — see [RUNTIME.md](RUNTIME.md) for details.

## Files

| File | Purpose |
|---|---|
| `bot.py` | Main bot logic and 30-day curriculum |
| `requirements.txt` | Python dependencies |
| `current_day.txt` | Day counter state |
| `bot.log` | Runtime log |
| `SETUP.md` | GitHub Actions deployment guide |
| `RUNTIME.md` | Local runtime requirements |

## Environment variables

| Variable | Purpose |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Token from @BotFather |
| `TELEGRAM_CHAT_ID` | Target Telegram chat ID |

## Commands

```bash
# Send today's lesson
python bot.py

# Send a specific day without changing the counter
python bot.py --day 5
```

## License

Private — for internal use.
