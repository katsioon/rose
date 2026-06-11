"""
Helper utilities - Shared functions for embeds, formatting, and common operations
"""

import nextcord
from datetime import datetime
import math

def create_embed(
    title: str = None,
    description: str = None,
    color: int = 0x2E86AB,
    author_name: str = None,
    author_icon: str = None,
    footer_text: str = None,
    footer_icon: str = None,
    thumbnail: str = None,
    image: str = None,
) -> nextcord.Embed:
    """Create a standardized embed"""
    embed = nextcord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.now()
    )
    
    if author_name:
        embed.set_author(name=author_name, icon_url=author_icon)
    
    if footer_text:
        embed.set_footer(text=footer_text, icon_url=footer_icon)
    
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    
    if image:
        embed.set_image(url=image)
    
    return embed

def create_success_embed(title: str, description: str = None) -> nextcord.Embed:
    """Create a success embed"""
    return create_embed(
        title=f"✅ {title}",
        description=description,
        color=0x4CAF50
    )

def create_error_embed(title: str, description: str = None) -> nextcord.Embed:
    """Create an error embed"""
    return create_embed(
        title=f"❌ {title}",
        description=description,
        color=0xFF6B6B
    )

def create_info_embed(title: str, description: str = None) -> nextcord.Embed:
    """Create an info embed"""
    return create_embed(
        title=f"ℹ️ {title}",
        description=description,
        color=0x2196F3
    )

def format_number(num: int) -> str:
    """Format large numbers with K, M, B suffixes"""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)

def create_progress_bar(current: int, max_val: int, length: int = 10) -> str:
    """Create a progress bar string"""
    filled = int((current / max_val) * length) if max_val > 0 else 0
    bar = "█" * filled + "░" * (length - filled)
    percent = int((current / max_val) * 100) if max_val > 0 else 0
    return f"{bar} {percent}%"

def format_time_until(timestamp: datetime) -> str:
    """Format time until a timestamp"""
    now = datetime.now()
    diff = timestamp - now
    
    if diff.total_seconds() <= 0:
        return "Now"
    
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    
    if days > 0:
        return f"{days}d {hours}h"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def get_xp_for_level(level: int) -> int:
    """Calculate XP needed to reach a level"""
    return 1000 * level

def get_level_from_xp(xp: int) -> tuple:
    """Get level and remaining XP from total XP"""
    level = 0
    remaining_xp = xp
    
    while remaining_xp >= 1000:
        level += 1
        remaining_xp -= 1000
    
    return level, remaining_xp

def rarity_color(rarity: str) -> int:
    """Get color for rarity level"""
    colors = {
        "common": 0x808080,      # Gray
        "uncommon": 0x4CAF50,    # Green
        "rare": 0x2196F3,        # Blue
        "epic": 0x9C27B0,        # Purple
        "legendary": 0xFFD700,   # Gold
        "mythic": 0xFF6B9D,      # Pink
    }
    return colors.get(rarity.lower(), 0x808080)

def rarity_emoji(rarity: str) -> str:
    """Get emoji for rarity level"""
    emojis = {
        "common": "⚪",
        "uncommon": "🟢",
        "rare": "🔵",
        "epic": "🟣",
        "legendary": "⭐",
        "mythic": "✨",
    }
    return emojis.get(rarity.lower(), "⚪")

def get_stat_bar(stat: int, max_stat: int = 100) -> str:
    """Create a stat bar visualization"""
    filled = int((stat / max_stat) * 10)
    bar = "█" * filled + "░" * (10 - filled)
    return f"{bar} {stat}/{max_stat}"

def format_duration(seconds: int) -> str:
    """Format seconds into readable duration"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def create_leaderboard_embed(
    title: str,
    data: list,
    columns: dict,
    color: int = 0x2E86AB
) -> nextcord.Embed:
    """Create a leaderboard embed
    
    Args:
        title: Leaderboard title
        data: List of tuples with leaderboard data
        columns: Dict of {column_name: data_index}
    """
    embed = nextcord.Embed(title=f"🏆 {title}", color=color)
    
    medals = ["🥇", "🥈", "🥉"]
    
    for i, row in enumerate(data[:10]):
        medal = medals[i] if i < 3 else f"{i+1}."
        
        name = f"{medal} {row[0]}"
        
        values = []
        for col_name, col_index in columns.items():
            values.append(f"{col_name}: {row[col_index]}")
        
        embed.add_field(
            name=name,
            value="\n".join(values),
            inline=False
        )
    
    return embed
