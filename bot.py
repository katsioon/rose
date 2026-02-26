"""
Rosé - A feature-rich Nextcord Discord bot
"""

import nextcord
from nextcord.ext import commands
import aiosqlite
import os
import logging
from utils.db import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
log = logging.getLogger("Rosé")

COGS = [
    "cogs.tickets",
    "cogs.entertainment",
    "cogs.horoscope",
    "cogs.rl",
    "cogs.pets",
    "cogs.cozy",
    "cogs.utility",
    "cogs.premium",
    "cogs.imagine",
    "cogs.social",
    "cogs.lastfm",
    "cogs.levels",
    "cogs.emojis",
    "cogs.rpg",
    "cogs.games",
    "cogs.ai_chat",
    "cogs.custom_commands",
    "cogs.shop",
    "cogs.dev",
]

# Support server config — set these in .env
SUPPORT_GUILD_ID   = int(os.getenv("SUPPORT_GUILD_ID",   "1435"))   # your support server ID
GUILD_LOG_CHANNEL  = int(os.getenv("GUILD_LOG_CHANNEL_ID", "1111")) # channel to log joins/leaves

intents = nextcord.Intents.default()
intents.members = True        # member join/leave events
intents.message_content = True  # needed for prefix commands + transcript history
os.makedirs("data", exist_ok=True)


class Rosé(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents, help_command=None)
        self.db_path        = "data/rose.db"
        self.premium_guilds: set = set()
        self.premium_users:  set = set()

    # ── get language for a guild ───────────────────────────────────────────────
    async def get_lang(self, guild_id: int) -> str:
        try:
            async with aiosqlite.connect(self.db_path) as db:
                async with db.execute(
                    "SELECT lang FROM guild_config WHERE guild_id=?", (guild_id,)
                ) as cur:
                    row = await cur.fetchone()
            return row[0] if row and row[0] else "en"
        except Exception:
            return "en"

    # ── ready ──────────────────────────────────────────────────────────────────
    async def on_ready(self):
        os.makedirs("data", exist_ok=True)
        await init_db(self.db_path)
        await self._load_premium()
        log.info(f"Rosé ready as {self.user} ({self.user.id})")
        await self.change_presence(activity=nextcord.Activity(
            type=nextcord.ActivityType.watching,
            name="paint dry"
        ))

    async def _load_premium(self):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT guild_id FROM premium_guilds") as cur:
                async for row in cur:
                    self.premium_guilds.add(row[0])
            async with db.execute("SELECT user_id FROM premium_users") as cur:
                async for row in cur:
                    self.premium_users.add(row[0])

    # ── guild log helper ───────────────────────────────────────────────────────
    async def _log_guild_event(self, guild: nextcord.Guild, joined: bool):
        if not GUILD_LOG_CHANNEL:
            return
        ch = self.get_channel(GUILD_LOG_CHANNEL)
        if not ch:
            return
        icon = guild.icon.url if guild.icon else None
        if joined:
            embed = nextcord.Embed(
                title="⭐ Rosé was added to a server",
                description=f"**{guild.name}**",
                color=0x57F287,
            )
            embed.add_field(name="Members", value=f"{guild.member_count:,}")
            embed.add_field(name="Server ID", value=str(guild.id))
            embed.add_field(name="Owner", value=f"<@{guild.owner_id}>", inline=False)
            embed.add_field(name="Total Servers", value=str(len(self.guilds)), inline=False)
        else:
            embed = nextcord.Embed(
                title="😭 Rosé was removed from a server",
                description=f"**{guild.name}**",
                color=0xFF4444,
            )
            embed.add_field(name="Server ID", value=str(guild.id))
            embed.add_field(name="Total Servers", value=str(len(self.guilds)), inline=False)
        if icon:
            embed.set_thumbnail(url=icon)
        try:
            await ch.send(embed=embed)
        except Exception as e:
            log.warning(f"Could not send guild log: {e}")

    # ── guild join ─────────────────────────────────────────────────────────────
    async def on_guild_join(self, guild: nextcord.Guild):
        log.info(f"Joined guild: {guild.name} ({guild.id})")
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR IGNORE INTO guild_config (guild_id) VALUES (?)", (guild.id,)
            )
            await db.commit()

        await self._log_guild_event(guild, joined=True)

        ch = guild.system_channel
        if ch and ch.permissions_for(guild.me).send_messages:
            embed = nextcord.Embed(
                title="🌸 Thanks for adding Rosé!",
                description=(
                    "I'm your all-in-one cozy companion!\n\n"
                    "**Get started:**\n"
                    "> `/help` — see all commands\n"
                    "> `/settings language` — switch to Dutch or other languages 🇳🇱\n\n"
                    "**Links:**\n"
                    "> 💬 [Support Server](https://discord.com/app)\n"
                    "> ⭐ [Patreon (Premium)](https://patreon.com/)"
                ),
                color=0xF4A261,
            )
            embed.set_footer(text="Rosé • discord.com")
            await ch.send(embed=embed)

    # ── guild leave ────────────────────────────────────────────────────────────
    async def on_guild_remove(self, guild: nextcord.Guild):
        log.info(f"Left guild: {guild.name} ({guild.id})")
        await self._log_guild_event(guild, joined=False)

    # ── member join ────────────────────────────────────────────────────────────
    async def on_member_join(self, member: nextcord.Member):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT join_channel_id, join_message, invite_tracking FROM guild_config WHERE guild_id=?",
                (member.guild.id,)
            ) as cur:
                row = await cur.fetchone()
        if not row:
            return
        join_ch_id, join_msg, inv_tracking = row
        if join_ch_id:
            ch = member.guild.get_channel(join_ch_id)
            if ch:
                msg = (join_msg or "Welcome {user} to **{server}**! 🍵").format(
                    user=member.mention, server=member.guild.name
                )
                embed = nextcord.Embed(description=msg, color=0xF4A261)
                embed.set_thumbnail(url=member.display_avatar.url)
                await ch.send(embed=embed)
        if inv_tracking:
            await self._track_invite(member)

    # ── member leave ───────────────────────────────────────────────────────────
    async def on_member_remove(self, member: nextcord.Member):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(
                "SELECT leave_channel_id, leave_message FROM guild_config WHERE guild_id=?",
                (member.guild.id,)
            ) as cur:
                row = await cur.fetchone()
        if not row or not row[0]:
            return
        ch = member.guild.get_channel(row[0])
        if ch:
            msg = (row[1] or "**{user}** has left the server. 👋").format(
                user=str(member), server=member.guild.name
            )
            embed = nextcord.Embed(description=msg, color=0x808080)
            embed.set_thumbnail(url=member.display_avatar.url)
            await ch.send(embed=embed)

    # ── invite tracking ────────────────────────────────────────────────────────
    async def _track_invite(self, member: nextcord.Member):
        try:
            invites = await member.guild.invites()
            async with aiosqlite.connect(self.db_path) as db:
                for inv in invites:
                    async with db.execute(
                        "SELECT uses FROM invite_cache WHERE code=?", (inv.code,)
                    ) as cur:
                        row = await cur.fetchone()
                    if row and row[0] < inv.uses:
                        await db.execute(
                            "INSERT OR IGNORE INTO invite_stats (guild_id, inviter_id, code, uses) VALUES (?,?,?,0)",
                            (member.guild.id, inv.inviter.id if inv.inviter else 0, inv.code)
                        )
                        await db.execute(
                            "UPDATE invite_stats SET uses=? WHERE code=?", (inv.uses, inv.code)
                        )
                    await db.execute(
                        "INSERT OR REPLACE INTO invite_cache (code, uses) VALUES (?,?)",
                        (inv.code, inv.uses)
                    )
                await db.commit()
        except Exception as e:
            log.warning(f"Invite tracking error: {e}")


bot = Rosé()

for cog in COGS:
    try:
        bot.load_extension(cog)
        log.info(f"Loaded {cog}")
    except Exception as e:
        log.error(f"Failed to load {cog}: {e}")

TOKEN = os.getenv("DISCORD_TOKEN", ""
