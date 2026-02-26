# 🌸 Rosé Bot — Full-Featured Nextcord Discord Bot

A cozy, all-in-one Discord bot with tickets, free AI, pets, RL resources, economy, and more.

## 📦 Quick Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment variables
cp .env.example .env
# Edit .env with your keys

# 3. Run
python bot.py
```

## 🔑 Environment Variables

Create a `.env` file (or set these in your host's dashboard):

```env
# Required
DISCORD_TOKEN=your_bot_token_here

# AI — at least one required for /ai commands (both are FREE, no credit card)
OPENROUTER_API_KEY=your_key   # free at https://openrouter.ai
HF_API_KEY=your_key           # free at https://huggingface.co/settings/tokens

# Optional AI settings
OPENROUTER_MODEL=mistralai/mistral-7b-instruct:free
HF_MODEL=mistralai/Mistral-7B-Instruct-v0.3
```

### Getting free AI keys

**OpenRouter (recommended primary):**
1. Go to https://openrouter.ai → Sign Up (free)
2. Settings → API Keys → Create Key
3. Free models have the `:free` suffix — no billing needed

**HuggingFace (fallback):**
1. Go to https://huggingface.co → Sign Up (free)
2. Settings → Access Tokens → New Token (read access)
3. Paste as `HF_API_KEY`

---

## ✨ Features

### 🎫 Tickets (`/ticket`)
`open` · `panel` · `setup` · `list` · `add_user` · `remove_user`
- Free: 1 open ticket | Premium: 10 open tickets
- Button-based creation panels
- Auto permission handling, transcripts

### 🎮 Fun (`/fun`)
`8ball` · `coinflip` · `roll` · `trivia` · `rps` · `joke` · `fact`

### 💰 Economy (`/economy`)
`balance` · `daily` · `work` · `slots` · `give` · `leaderboard`
- Free daily: 🪙500 | Premium daily: 🪙1000

### 🤖 AI (`/ai`) — 100% FREE models
`chat` · `summarize` · `roast` · `imagine` · `models` · `usage` · `clear_memory`
- Primary: **OpenRouter** (Mistral 7B, Llama 3.2, Gemma 2, Phi-3, Qwen 2)
- Fallback: **HuggingFace** Inference API
- Free: 5 msgs/day | Premium: 50 msgs/day + persistent memory

### 📚 RL Resources (`/rl`)
`browse` · `random` · `search` · `top` · `upvote` · `roadmap` · `submit`
- 14 curated seed resources
- Beginner / intermediate / advanced roadmaps
- Submit resources (Premium)

### 🐾 Pets (`/pet`)
`adopt` · `status` · `feed` · `play` · `sleep` · `list` · `rename` · `leaderboard`
- Stats decay over time (hunger, happiness, energy)
- Leveling & XP system
- Rarities: Common → Uncommon → Rare ⭐ → Legendary ⭐⭐
- Free: 1 pet (common only) | Premium: 5 pets + rare/legendary

### 🍵 Cozy (`/cozy`)
`affirmation` · `vibe` · `mood` · `mood_history` · `board` · `tea` · `playlist` · `breathe` · `hug` · `quote`

### 🔧 Utility
`/remind` · `/poll` · `/serverinfo` · `/userinfo` · `/avatar` · `/ping` · `/invites` · `/help`

### ⭐ Premium (`/premium`)
`info` · `status`
- Subscribe: https://patreon.com/katsioon
- Join server: https://discord.gg/rKajpSCGKF

---

## 🔧 Dev Commands (`/dev`) — Bot owner only

Edit `DEV_IDS` in `cogs/dev.py` to add your Discord user ID.

| Command | Description |
|---------|-------------|
| `/dev config [guild_id]` | View a guild's full config |
| `/dev set_join_channel` | Set member join announcement channel |
| `/dev set_leave_channel` | Set member leave announcement channel |
| `/dev set_join_message` | Custom join message (`{user}`, `{server}`) |
| `/dev set_leave_message` | Custom leave message |
| `/dev toggle_invite_tracking` | Enable/disable invite tracking per guild |
| `/dev grant_premium` | Grant premium to user or guild (with expiry) |
| `/dev revoke_premium` | Revoke premium |
| `/dev broadcast` | Send announcement to all guild system channels |
| `/dev guilds` | List all guilds the bot is in |
| `/dev stats` | Memory, latency, guild/user counts |
| `/dev reload [cog]` | Hot-reload a cog without restart |
| `/dev sql [query]` | Read-only SQL query on the database |

---

## 📁 File Structure

```
rose-bot/
├── bot.py              # Main bot, join/leave events, invite tracking
├── requirements.txt
├── .env.example
├── data/               # Auto-created — holds rose.db (SQLite)
├── cogs/
│   ├── tickets.py      # Ticket system
│   ├── entertainment.py # Fun + economy
│   ├── ai.py           # AI chat (OpenRouter + HuggingFace)
│   ├── rl.py           # RL resource library
│   ├── pets.py         # Virtual pets
│   ├── cozy.py         # Cozy features
│   ├── utility.py      # Server tools, reminders, polls
│   ├── premium.py      # Premium info/status
│   └── dev.py          # Dev/owner-only commands
└── utils/
    ├── db.py           # Database schema & init
    └── helpers.py      # Shared embed helpers
```
