#Version: 1.4
#GitHub: https://github.com/Simoneeeeeeee/Discord-Select-Menu-Ticket-Bot
#Discord: Simone#0782
#This Bot is using Py-Cord as Discord API Wrapper


import discord
import asyncio
import json
from discord.ui import *
from discord.ext import commands
from discord.ext.commands import has_permissions
from pytz import timezone

with open("config.json", mode="r") as config_file:
    config = json.load(config_file)

BOT_TOKEN = config["token"]
BOT_PREFIX = config["prefix"]

GUILD_ID = config["guild_id"] #Server ID
TICKET_CHANNEL = config["ticket_channel_id"] #Where the bot should send the Embed + SelectMenu

CATEGORY_ID1 = config["category_id_1"] #Support1 Channel
CATEGORY_ID2 = config["category_id_2"] #Support2 Channel

TEAM_ROLE1 = config["team_role_id_1"] #Permissions for Support1
TEAM_ROLE2 = config["team_role_id_1"] #Permissions for Support2

LOG_CHANNEL = config["log_channel_id"] #Log Channel

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    bot.add_view(MyView())
    bot.add_view(delete())

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(
        custom_id="support",
        placeholder="Choose a Ticket option",
        options=[
            discord.SelectOption(
                label="Help",
                emoji="❓",
                value="support1"
            ),
            discord.SelectOption(
                label="Event Help",
                emoji="❓",
                value="support2"
            )
        ]
    )
    async def callback(self, select, interaction):
        if "support1" in interaction.data['values']:
            if interaction.channel.id == TICKET_CHANNEL:
                guild = bot.get_guild(GUILD_ID)
                for ticket in guild.channels:
                    if str(interaction.user.id) in ticket.name:
                        embed = discord.Embed(title=f"You can only open one Ticket!", description=f"Here is your opend Ticket --> {ticket.mention}", color=0xff0000)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        await asyncio.sleep(3)
                        embed = discord.Embed(title="Support-Tickets", color=discord.colour.Color.blue())
                        await interaction.message.edit(embed=embed, view=MyView())
                        return
                category = bot.get_channel(CATEGORY_ID1)
                ticket_channel = await guild.create_text_channel(f"ticket-{interaction.user.id}", category=category,
                                                                topic=f"Ticket from {interaction.user} \nUser-ID: {interaction.user.id}")

                await ticket_channel.set_permissions(guild.get_role(TEAM_ROLE1), send_messages=True, read_messages=True, add_reactions=False,
                                                    embed_links=True, attach_files=True, read_message_history=True,
                                                    external_emojis=True)
                await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False,
                                                    embed_links=True, attach_files=True, read_message_history=True,
                                                    external_emojis=True)
                await ticket_channel.set_permissions(guild.default_role, send_messages=False, read_messages=False, view_channel=False)
                embed = discord.Embed(description=f'**__WELCOME {interaction.user.mention}TO PERSONALIZED TALK!__**\n'
                                                   '**Support Team will be with you shortly.**',
                                                color=discord.colour.Color.blue())
                await ticket_channel.send(embed=embed, view=delete())

                embed = discord.Embed(description=f'📬 Ticket was Created! Look here --> {ticket_channel.mention}',
                                        color=discord.colour.Color.green())
                await interaction.response.send_message(embed=embed, ephemeral=True)
                await asyncio.sleep(3)
                embed = discord.Embed(title="Support-Tickets", color=discord.colour.Color.blue())
                await interaction.message.edit(embed=embed, view=MyView())
                return
        if "support2" in interaction.data['values']:
            if interaction.channel.id == TICKET_CHANNEL:
                guild = bot.get_guild(GUILD_ID)
                for ticket in guild.channels:
                    if str(interaction.user.id) in ticket.name:
                        embed = discord.Embed(title=f"You can only open one Ticket", description=f"Here is your opend Ticket --> {ticket.mention}", color=0xff0000)
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        await asyncio.sleep(3)
                        embed = discord.Embed(title="Support-Tickets", color=discord.colour.Color.blue())
                        await interaction.message.edit(embed=embed, view=MyView())
                        return 
                category = bot.get_channel(CATEGORY_ID2)
                ticket_channel = await guild.create_text_channel(f"ticket-{interaction.user.id}", category=category,
                                                                    topic=f"Ticket from {interaction.user} \nUser-ID: {interaction.user.id}")
                await ticket_channel.set_permissions(guild.get_role(TEAM_ROLE2), send_messages=True, read_messages=True, add_reactions=False,
                                                        embed_links=True, attach_files=True, read_message_history=True,
                                                        external_emojis=True)
                await ticket_channel.set_permissions(interaction.user, send_messages=True, read_messages=True, add_reactions=False,
                                                        embed_links=True, attach_files=True, read_message_history=True,
                                                        external_emojis=True)
                await ticket_channel.set_permissions(guild.default_role, send_messages=False, read_messages=False, view_channel=False)
                embed = discord.Embed(description=f'**__WELCOME {interaction.user.mention}TO PERSONALIZED TALK!__**\n'
                                                   '**Support Team will be with you shortly.**',
                                                    color=discord.colour.Color.blue())
                await ticket_channel.send(embed=embed, view=delete())

                embed = discord.Embed(description=f'📬 Ticket was Created! Look here --> {ticket_channel.mention}',
                                        color=discord.colour.Color.green())
                await interaction.response.send_message(embed=embed, ephemeral=True)

                await asyncio.sleep(3)
                embed = discord.Embed(title="Support-Tickets", color=discord.colour.Color.blue())
                await interaction.message.edit(embed=embed, view=MyView())
        return

class delete(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket 🎫", style = discord.ButtonStyle.red, custom_id="close")
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        channel = bot.get_channel(LOG_CHANNEL)

        fileName = f"{interaction.channel.name}.txt"
        with open(fileName, "w", encoding='utf-8') as file:
            async for msg in interaction.channel.history(limit=None, oldest_first=True):
                time = msg.created_at.replace(tzinfo=timezone('UTC')).astimezone(timezone('Europe/Berlin'))
                file.write(f"{time} - {msg.author.display_name}: {msg.clean_content}\n")

        embed = discord.Embed(
                description=f'Ticket is closing in 5Sec.',
                color=0xff0000)
        embed2 = discord.Embed(title="Ticket Closed!", description=f"Ticket-Name: {interaction.channel.name}\n Closed-From: {interaction.user.name}\n Transcript: ", color=discord.colour.Color.blue())
        file = discord.File(fileName)
        await interaction.response.send_message(embed=embed)
        await channel.send(embed=embed2)
        await asyncio.sleep(1)
        await channel.send(file=file)
        await asyncio.sleep(5)
        await interaction.channel.delete(reason="Ticket closed by user")

@bot.command()
@has_permissions(administrator=True)
async def ticket(ctx):
    channel = bot.get_channel(TICKET_CHANNEL)
    embed = discord.Embed(title="Support-Tickets", color=discord.colour.Color.green())
    await channel.send(embed=embed, view=MyView())

bot.run(BOT_TOKEN)
