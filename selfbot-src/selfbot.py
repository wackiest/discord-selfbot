import discord, json, os, time, httpx
import asyncio
from discord.ext import commands
from colorama import Fore
from pypresence import Presence
from datetime import datetime


#Client & Configuration
config = json.load(open('config.json'))


client = commands.Bot(
    command_prefix = config["prefix"],
    case_insensitive=True,
    help_command=None,
    self_bot=True
)

def updateConfig():
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

#----------------------------------------------------------------------------------------------------------------------
# Register events

@client.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'''{Fore.LIGHTBLUE_EX}

                                                    virtue da best

                                            Connected as: {client.user}

________________________________________________________________________________________________________________________

''')

@client.event
async def on_command_error(ctx, error):
    print(f"[{Fore.YELLOW}!{Fore.RESET}] {Fore.RED}[ERROR]{Fore.RED}: {Fore.YELLOW}{error}{Fore.RESET}")

@client.event
async def on_command(ctx):
    print(f"{Fore.LIGHTBLUE_EX}[COMMAND]{Fore.LIGHTBLUE_EX}:{Fore.BLUE} {ctx.command.name}{Fore.RESET}")

#----------------------------------------------------------------------------------------------------------------------

#Commands

@client.command()
async def prefix(ctx, arg):
    await ctx.message.delete()
    old = client.command_prefix
    client.command_prefix = arg
    await ctx.send(f"```ini\n[ i am cat i go meow ]\n\nPrefix changed to: {client.command_prefix}```", delete_after=4)

@client.command(aliases=["deleteall"])
async def d(ctx, limit: int=None):
    await ctx.message.delete()
    passed = 0
    failed = 0
    ratelimited = 0
    async for msg in ctx.message.channel.history(limit=limit):
        if msg.author.id == client.user.id:
            try:
                await msg.delete()
                passed += 1
            except discord.errors.HTTPException:
                ratelimited += 1
                failed += 1

    await ctx.send(f"```ini\n[ i am cat i go meow ]\n\nDeleted {passed} messages\nRateLimited {ratelimited} times.```", delete_after=4)

@client.command()
async def purge(ctx, amount: int):
    await ctx.message.delete()
    deleted = 0
    ratelimited = 0
    async for message in ctx.channel.history(limit=amount):
        if message.author.id == client.user.id:
            try:
                await message.delete()
                deleted += 1
            except discord.errors.Forbidden:
                ratelimited += 1

    await ctx.send(f"```ini\n[ i am cat i go meow ]\n\nDeleted {deleted} messages\nRateLimited {ratelimited} times.```", delete_after=4)

@client.command()
async def av(ctx, *, user: discord.User = None):
    await ctx.message.delete()
    if user is None:
        user = ctx.author
    avatarurl = user.avatar_url
    await ctx.send(avatarurl)
    
    
@client.command()
async def banner(ctx, user:discord.Member):
    await ctx.message.delete()
    if user == None:
        user = ctx.author
    req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req["banner"]
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
    await ctx.send(f"{banner_url}")

    
    
@client.command()
async def stream(ctx, *, message):
    await ctx.message.delete()
    stream = discord.Streaming(
        name=message,
        url="https://twitch.tv/virtueontop", 
    )
    await client.change_presence(activity=stream)
    await ctx.send(f"```ini\n[ i am cat i go meow ]\n\nStream set to: {message}```", delete_after=4)


@client.command()
async def help(ctx):
    await ctx.send(f"```ini\n[ epic help menu ]\n\n>prefix ? [changes prefix to whatever u want]\n>purge 99 [purges specified amount of messages]\n>d [attempts to delete all messages in the channel command is sent in, fair warning you WILL get ratelimited]\n>av @user [gets users profile pic]\n>banner @user [gets users banner if they have one]\n>stream text [streams the text provided as your status]\n\n\n[made by virtue#0002]```", delete_after=8)



client.run(config["token"], bot=False, reconnect=True)





