"""
Gaming Cog - Interactive games, leaderboards, and achievements
"""

import disnake
from disnake.ext import commands
import random
import asyncio
from datetime import datetime, timedelta
from typing import Optional
import json

class GamingView(disnake.ui.View):
    """Base view for gaming interactions"""
    
    def __init__(self, timeout=30):
        super().__init__(timeout=timeout)
        self.result = None
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True


class RockPaperScissorsView(GamingView):
    """Rock Paper Scissors game view"""
    
    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id
        self.choices = {}
    
    @disnake.ui.button(label="🪨 Rock", style=disnake.ButtonStyle.primary)
    async def rock(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.author.id != self.user_id:
            await inter.response.defer(ephemeral=True)
            return
        self.result = "rock"
        self.stop()
        await inter.response.defer()
    
    @disnake.ui.button(label="📄 Paper", style=disnake.ButtonStyle.primary)
    async def paper(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.author.id != self.user_id:
            await inter.response.defer(ephemeral=True)
            return
        self.result = "paper"
        self.stop()
        await inter.response.defer()
    
    @disnake.ui.button(label="✂️ Scissors", style=disnake.ButtonStyle.primary)
    async def scissors(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        if inter.author.id != self.user_id:
            await inter.response.defer(ephemeral=True)
            return
        self.result = "scissors"
        self.stop()
        await inter.response.defer()


class Gaming(commands.Cog):
    """Gaming commands and systems"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.leaderboard = {}
        self.achievements = {}
    
    @commands.command(name="rps")
    async def rock_paper_scissors(self, ctx: commands.Context):
        """Play rock paper scissors against the bot"""
        view = RockPaperScissorsView(ctx.author.id)
        
        embed = disnake.Embed(
            title="🎮 Rock Paper Scissors",
            description="Make your choice!",
            color=disnake.Color.blue()
        )
        embed.set_footer(text="You have 30 seconds to choose")
        
        msg = await ctx.send(embed=embed, view=view)
        
        try:
            await asyncio.wait_for(view.wait(), timeout=30)
            
            player_choice = view.result
            bot_choice = random.choice(["rock", "paper", "scissors"])
            
            # Determine winner
            if player_choice == bot_choice:
                result = "Draw!"
                color = disnake.Color.greyple()
            elif (
                (player_choice == "rock" and bot_choice == "scissors") or
                (player_choice == "paper" and bot_choice == "rock") or
                (player_choice == "scissors" and bot_choice == "paper")
            ):
                result = "You won! 🎉"
                color = disnake.Color.green()
                await self.add_points(ctx.author.id, 10)
            else:
                result = "Bot won! 🤖"
                color = disnake.Color.red()
            
            embed = disnake.Embed(
                title="🎮 Rock Paper Scissors",
                description=f"**Your choice:** {player_choice.capitalize()}\n**Bot choice:** {bot_choice.capitalize()}\n\n**Result:** {result}",
                color=color
            )
            
            await msg.edit(embed=embed, view=None)
        
        except asyncio.TimeoutError:
            await ctx.send("❌ Time's up! You didn't choose in time.")
    
    @commands.command(name="dice")
    async def roll_dice(self, ctx: commands.Context, sides: int = 6):
        """Roll a dice"""
        if sides < 2:
            await ctx.send("❌ Dice must have at least 2 sides.")
            return
        
        if sides > 1000:
            await ctx.send("❌ Dice can't have more than 1000 sides.")
            return
        
        result = random.randint(1, sides)
        
        embed = disnake.Embed(
            title=f"🎲 Dice Roll ({sides} sided)",
            description=f"You rolled: **{result}**",
            color=disnake.Color.blue()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="flip")
    async def flip_coin(self, ctx: commands.Context):
        """Flip a coin"""
        result = random.choice(["Heads", "Tails"])
        emoji = "🪙" if result == "Heads" else "🪙"
        
        embed = disnake.Embed(
            title="Coin Flip",
            description=f"{emoji} **{result}**!",
            color=disnake.Color.gold()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="leaderboard")
    async def show_leaderboard(self, ctx: commands.Context):
        """View gaming leaderboard"""
        if not self.leaderboard:
            await ctx.send("📊 Leaderboard is empty! Start playing games.")
            return
        
        sorted_lb = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)[:10]
        
        description = ""
        for i, (user_id, points) in enumerate(sorted_lb, 1):
            user = self.bot.get_user(user_id)
            name = user.mention if user else f"Unknown User ({user_id})"
            description += f"{i}. {name} - **{points}** points\n"
        
        embed = disnake.Embed(
            title="🏆 Gaming Leaderboard",
            description=description,
            color=disnake.Color.gold()
        )
        embed.set_footer(text=f"Total players: {len(self.leaderboard)}")
        
        await ctx.send(embed=embed)
    
    @commands.command(name="stats")
    async def user_stats(self, ctx: commands.Context, user: Optional[disnake.User] = None):
        """View your gaming stats"""
        if user is None:
            user = ctx.author
        
        points = self.leaderboard.get(user.id, 0)
        achievements = self.achievements.get(user.id, [])
        
        embed = disnake.Embed(
            title=f"🎮 {user.name}'s Stats",
            color=disnake.Color.blue()
        )
        embed.add_field(name="Points", value=f"**{points}**", inline=True)
        embed.add_field(name="Achievements", value=f"**{len(achievements)}**", inline=True)
        embed.add_field(name="Level", value=f"**{max(1, points // 100)}**", inline=True)
        
        if achievements:
            embed.add_field(name="Achievements", value="\n".join(achievements), inline=False)
        
        embed.set_thumbnail(url=user.display_avatar.url)
        
        await ctx.send(embed=embed)
    
    @commands.command(name="guess")
    async def guess_number(self, ctx: commands.Context):
        """Guess a number between 1-100"""
        number = random.randint(1, 100)
        attempts = 0
        max_attempts = 7
        
        embed = disnake.Embed(
            title="🔢 Guess the Number",
            description=f"I'm thinking of a number between 1-100. You have {max_attempts} attempts.",
            color=disnake.Color.blue()
        )
        await ctx.send(embed=embed)
        
        while attempts < max_attempts:
            try:
                msg = await self.bot.wait_for(
                    'message',
                    check=lambda m: m.author == ctx.author and m.channel == ctx.channel,
                    timeout=30
                )
                
                try:
                    guess = int(msg.content)
                except ValueError:
                    await ctx.send("❌ Please enter a valid number.")
                    continue
                
                if guess < 1 or guess > 100:
                    await ctx.send("❌ Number must be between 1-100.")
                    continue
                
                attempts += 1
                
                if guess == number:
                    await ctx.send(f"✅ Correct! The number was **{number}**. You guessed it in **{attempts}** attempts!")
                    await self.add_points(ctx.author.id, (max_attempts - attempts + 1) * 10)
                    return
                elif guess < number:
                    await ctx.send(f"📈 Too low! Attempts left: {max_attempts - attempts}")
                else:
                    await ctx.send(f"📉 Too high! Attempts left: {max_attempts - attempts}")
            
            except asyncio.TimeoutError:
                await ctx.send("❌ Time's up!")
                return
        
        await ctx.send(f"❌ Game over! The number was **{number}**.")
    
    async def add_points(self, user_id: int, points: int):
        """Add points to user's score"""
        if user_id not in self.leaderboard:
            self.leaderboard[user_id] = 0
        self.leaderboard[user_id] += points


def setup(bot: commands.Bot):
    """Load the Gaming cog"""
    bot.add_cog(Gaming(bot))
