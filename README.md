# 🌸 Rosé Bot — Full-Featured Nextcord Discord Bot

A cozy, all-in-one Discord bot with tickets, free AI, pets, RL resources, economy, games, social features, music, levels, and much more.

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

# Support & Logging (Optional)
SUPPORT_GUILD_ID=your_support_server_id
GUILD_LOG_CHANNEL_ID=your_log_channel_id
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

### 🎮 Entertainment (`/fun`)
`8ball` · `coinflip` · `roll` · `trivia` · `rps` · `joke` · `fact`
- Quick & fun mini-games

### 🌟 Horoscope (`/horoscope`)
`daily` · `weekly` · `love` · `career`
- Personalized horoscope readings by zodiac sign
- Daily, weekly, and category-specific predictions

### 💰 Economy (`/economy`)
`balance` · `daily` · `work` · `slots` · `give` · `leaderboard`
- Free daily: 🪙500 | Premium daily: 🪙1000
- Work mini-jobs to earn coins
- Slots & gambling games
- Economy leaderboards

### 🤖 AI Chat (`/ai`)
`chat` · `summarize` · `roast` · `imagine` · `models` · `usage` · `clear_memory`
- Primary: **OpenRouter** (Mistral 7B, Llama 3.2, Gemma 2, Phi-3, Qwen 2)
- Fallback: **HuggingFace** Inference API
- Free: 5 msgs/day | Premium: 50 msgs/day + persistent memory
- 100% FREE models, no credit card needed

### 📚 RL Resources (`/rl`)
`browse` · `random` · `search` · `top` · `upvote` · `roadmap` · `submit`
- 14 curated seed resources
- Beginner / intermediate / advanced roadmaps
- Submit resources (Premium)
- Resource discovery & voting system

### 🐾 Pets (`/pet`)
`adopt` · `status` · `feed` · `play` · `sleep` · `list` · `rename` · `leaderboard`
- Stats decay over time (hunger, happiness, energy)
- Leveling & XP system
- Rarities: Common → Uncommon → Rare ⭐ → Legendary ⭐⭐
- Free: 1 pet (common only) | Premium: 5 pets + rare/legendary
- Pet leaderboards & achievements

### 🍵 Cozy (`/cozy`)
`affirmation` · `vibe` · `mood` · `mood_history` · `board` · `tea` · `playlist` · `breathe` · `hug` · `quote`
- Wellness & mental health features
- Daily affirmations & motivation
- Mood tracking & history
- Meditation guidance

### 🎵 Imagine (`/imagine`)
`generate` · `edit` · `variations` · `history` · `download`
- AI image generation
- Create, edit, and explore image variations
- Save & manage image history
- High-quality visual content generation

### 👥 Social (`/social`)
`profile` · `follow` · `unfollow` · `followers` · `following` · `feed` · `like` · `comment`
- Social networking features
- User profiles & follower systems
- Social feeds & interactions
- Community engagement

### 🎵 Last.fm (`/lastfm`)
`now_playing` · `top_tracks` · `top_albums` · `top_artists` · `stats` · `compare`
- Music stats integration
- Track now playing music
- View listening history & statistics
- Compare music taste with others

### 📊 Levels (`/levels`)
`rank` · `leaderboard` · `profile` · `stats` · `reset` · `multiplier`
- Experience & leveling system
- Per-guild leaderboards
- User level profiles & stats
- XP multiplier for boosters

### 😀 Emojis (`/emojis`)
`random` · `search` · `stats` · `top` · `custom` · `pack`
- Emoji discovery & management
- Search & filter emojis
- Emoji usage statistics
- Create custom emoji packs

### ⚔️ RPG (`/rpg`)
`start` · `status` · `inventory` · `adventure` · `battle` · `shop` · `quest` · `leaderboard`
- Full RPG experience
- Character creation & progression
- Combat system & battles
- Quests & adventures
- RPG shop & inventory management

### 🎮 Games (`/games`)
`hangman` · `minesweeper` · `tictactoe` · `connect4` · `snake` · `blackjack` · `2048` · `wordle`
- Classic & modern games
- Interactive multiplayer games
- Leaderboards & achievements
- Weekly challenges

### 🛍️ Shop (`/shop`)
`browse` · `buy` · `sell` · `inventory` · `listings` · `trade`
- In-game marketplace
- Buy & sell items
- Trading system
- Player-to-player commerce

### 🎨 Custom Commands (`/custom`)
`create` · `list` · `edit` · `delete` · `run` · `import` · `export`
- Create custom commands
- Server customization
- Command management
- Share & import command sets

### 🔧 Utility
`/remind` · `/poll` · `/serverinfo` · `/userinfo` · `/avatar` · `/ping` · `/invites` · `/help` · `/settings`
- Reminders & scheduling
- Polls & voting
- Server & user information
- Advanced configuration

### ⭐ Premium (`/premium`)
`info` · `status` · `subscribe`
- Subscribe: https://patreon.com/
- Join server: https://discord.gg/rKajpSCGKf
- Enhanced features & priority support
- Exclusive content & perks

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
│   ├── entertainment.py # Fun & games
│   ├── horoscope.py    # Horoscope readings
│   ├── ai_chat.py      # AI chat (OpenRouter + HuggingFace)
│   ├── rl.py           # RL resource library
│   ├── pets.py         # Virtual pets
│   ├── cozy.py         # Wellness & cozy features
│   ├── utility.py      # Server tools, reminders, polls
│   ├── premium.py      # Premium info/status
│   ├── imagine.py      # AI image generation
│   ├── social.py       # Social networking
│   ├── lastfm.py       # Last.fm music stats
│   ├── levels.py       # Experience & leveling
│   ├── emojis.py       # Emoji management
│   ├── rpg.py          # RPG system
│   ├── games.py        # Mini-games collection
│   ├── custom_commands.py # Custom command creation
│   ├── shop.py         # In-game marketplace
│   └── dev.py          # Dev/owner-only commands
└── utils/
    ├── db.py           # Database schema & init
    └── helpers.py      # Shared embed helpers
```

---

## 🚀 Features at a Glance

| Feature | Free | Premium | Details |
|---------|------|---------|---------|
| Tickets | 1 open | 10 open | Full support system |
| Pets | 1 common | 5 + rare/legendary | Virtual companion |
| Economy | 500 daily | 1000 daily | Earn & spend coins |
| AI Chat | 5 msgs/day | 50 msgs/day | Free models, no card |
| Games | ✅ All | ✅ Bonus perks | 8+ games included |
| Levels | ✅ Yes | XP multiplier | Guild-based leveling |
| Custom Commands | ✅ Yes | ✅ More | Server customization |

---

## 💝 Support & Contribute

- 💬 **Support Server**: https://discord.gg/rKajpSCGKf
- ⭐ **Patreon (Premium)**: https://patreon.com/
- 🐛 **Report Issues**: Open an issue on GitHub
- 💡 **Feature Requests**: Discuss in support server

---

## 📜 License

Apache License 2.0 — See [LICENSE](./LICENSE) for details.

---

**Official Bot Invite**: https://discord.com/oauth2/authorize?client_id=1473825746379083982

*Rosé • A cozy companion for your Discord server 🌸*
