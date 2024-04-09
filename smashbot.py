import discord
from discord.ext import commands
import asyncio
import findVodVs
import os

def split_message(message, limit=2000):
    """
    Splits a message into chunks each of size `limit`, which defaults to Discord's limit.
    
    Args:
        message (str): The message to split.
        limit (int, optional): Maximum length of each chunk. Defaults to 2000.
    
    Returns:
        list of str: A list of message chunks, each within the specified limit.
    """
    # Ensure message is a string and limit is an integer greater than 0
    if not isinstance(message, str) or not isinstance(limit, int) or limit <= 0:
        raise ValueError("Invalid message or limit")

    # Return the message itself if it's within the limit
    if len(message) <= limit:
        return [message]

    # Split the message into chunks
    chunks = []
    while message:
        # Find the nearest whitespace to split on to avoid breaking words
        split_index = message.rfind(' ', 0, limit)
        if split_index == -1:  # No whitespace found, forced to split at limit
            split_index = limit
        
        chunk = message[:split_index].strip()
        chunks.append(chunk)
        message = message[split_index:].strip()

    return chunks

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents.all()

# Initialize Bot and Denote The Command Prefix
bot = commands.Bot(command_prefix="!", intents=intents)

text_channel_list = []
guild_list = []

# Runs when Bot Succesfully Connects
@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')

    for guild in bot.guilds:
        guild_list.append(guild)
    print(f"Connected to {len(guild_list)} servers")

@bot.event
async def on_message(message):
    # Make sure the Bot doesn't respond to it's own messages
    if message.author == bot.user: 
        return
    
    if message.content == 'hello bot':
        await message.channel.send(f'Hi {message.author}')

    await bot.process_commands(message)

@bot.command()
async def printTextChannels(ctx):
    for channel in text_channel_list:
        await ctx.send(channel.name)

@bot.command()
async def clear(ctx):
    await ctx.send("Clearing all messages in bot-testing")
    botTestChannel = bot.get_channel(1221596751207596032)
    for thread in botTestChannel.threads:
        await thread.delete()
    await botTestChannel.purge()

myVods =  "https://www.youtube.com/playlist?list=PL0idm2uMQWS99jtrqZZGeshQL1NlMMnb7"
topVods = "https://www.youtube.com/playlist?list=PL0idm2uMQWS9UTUs1us-1uo0dDgYFomZf"

@bot.command()
async def updateVods(ctx):
    botTestChannel = bot.get_channel(1221596751207596032)
    statusmsg = await botTestChannel.send(f"Updating your Vods vs all characters from your Youtube Playlist")
    
    #Dictionary in the format (CharName : List of Vods)
    vodDict = findVodVs.get_all_vods(myVods, "Pawp")
    print("Finished Finding Vods")

    existing_threads = []
    for thread in botTestChannel.threads:
        existing_threads.append(thread.name)

    for char in vodDict:
        thread_name = char + " Vods"
        if thread_name not in existing_threads:
            print("Creating new thread:", thread_name)
            await asyncio.sleep(0.4)  # Delay to help avoid rate limiting
            threadStartMsg = await botTestChannel.send(thread_name)
            thread = await threadStartMsg.create_thread(name=thread_name)
        else:
            print("Thread already exists:", thread_name)
            thread = discord.utils.get(botTestChannel.threads, name=thread_name)
            #Delete messages in thread and post new one
            def isDefaultMsg(m):
                return m.type == discord.MessageType.default
            
            await thread.purge(check= isDefaultMsg)

        for vod in vodDict[char]:
            videoURL = vod.watch_url
            await asyncio.sleep(0.2)  # Delay to help avoid rate limiting
            if (videoURL != ""):
                await thread.send(videoURL)
    
    await statusmsg.delete()
    await asyncio.sleep(1)  # Ensure the last message is sent before deletion to avoid potential rate limiting

bot.run(TOKEN)