import requests
import json
import discord
from discord.ext import commands, tasks
import attacks_remain
import sched
import time
from datetime import timedelta, datetime
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

clash_api_key = None

clan_tag = None

@bot.event
async def on_ready():
    print("[on_ready] ready as", bot.user.name)

@bot.command(name='warreminder')
async def warreminder(ctx, *args):
    global clan_tag
    if len(args) != 1:
        await ctx.send("Error: usage should be !warreminder <clan tag>")
        return
    clan_tag = args[0]
    await ctx.send("Clan tag set as " + clan_tag)
    war_reminder = attacks_remain.WarReminder(clan_tag=clan_tag, api_key=clash_api_key)
    notification_time = war_reminder.get_notify_time()

    # # DEBUG: manually change notification time to 10 seconds from now
    # notification_time = datetime.now() + timedelta(seconds=10)

    await ctx.send("Will remind at " + str(notification_time))

    # wait to notify members until that time comes around
    await schedule_reminder(ctx, notification_time)

async def notify_members(ctx):
    war_reminder = attacks_remain.WarReminder(clan_tag=clan_tag, api_key=clash_api_key)
    remind_list = war_reminder.get_attacks_remaining()
    remind_string = ""
    for member in remind_list:
        remind_string += member["tag"] + " " + member["name"] + " has attacks left!\n"
    await ctx.send("8 hours left to go in war!\n" + remind_string)

def set_clash_api_key(key):
    global clash_api_key
    clash_api_key = key

async def schedule_reminder(ctx, notification_time):
    s = sched.scheduler(time.time, time.sleep)
    
    # Calculate the delay until the target time
    now = datetime.now()
    delay = (notification_time - now).total_seconds()
    
    await asyncio.sleep(delay)

    # Run the task
    await notify_members(ctx)