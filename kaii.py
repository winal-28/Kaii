import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
from discord.ext.commands import MissingPermissions, CommandNotFound, Bot, guild_only

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

kaii = commands.Bot(command_prefix='CAE', intents=intents)


@kaii.event
async def on_ready():
    print('Kaii deployed! CAEgagaling!')
    await kaii.change_presence(activity=discord.Game(name="CAEcmd"))
    kaii.remove_command('help')


@kaii.event
async def on_member_join(member):
    channel = kaii.get_channel(11031906882136326144)
    await channel.send(f'{member} is in the server!')


@kaii.event
async def on_member_remove(member):
    channel = kaii.get_channel(1031906882136326144)
    await channel.send(f'{member} left the server :(')

@kaii.command()
async def test(ctx, arg):
    await ctx.send(arg)

@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument): 
     await ctx.send("Please provide an argument!")

@kaii.command()
async def cmd(ctx):
    nl = '\n'
    embed = discord.Embed(
        title="Kaii Commands",
        url="https://discord.com/app",
        description=
        f"Command prefix: CAE {nl} Here are the list of commands:{nl} CAEcommands - Shows this {nl} CAEping - check bot ping {nl} CAEtanginamo - Makes me mad >:( {nl} CAEmsg (insert what you want me to say here) - makes me say shit on your demand!, {nl} Moderation Commands {nl}{nl} CAEkick (insert user here) - kicks the member you want to kick {nl} CAEban (insert user here) - bans the member you want to kick {nl}{nl}",
        color=0x00FFFF)
    await ctx.send(embed=embed)

#moderation commands
@kaii.command(name="mute")
@commands.has_permissions(manage_roles=True, manage_channels=True)
async def mute(ctx, user: discord.Member, *, reason=None):
    try: 
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(role, send_messages=False)
        await user.add_roles(role, reason=reason)
        if reason:
            await ctx.send(f"{user} has been muted for {reason}.")
        else:
            await ctx.send(f"{user} has been muted.")
    except discord.Forbidden:
        await ctx.send(f":x: Could not mute {user}.")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(":x: You don't have permission to mute members.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":question: Please mention a user to mute.")

@kaii.command()
@commands.has_permissions(manage_roles=True, manage_channels=True)
async def unmute(ctx, *, user: discord.Member):
    await user.edit(mute=False)
    await ctx.send(f"{user.mention} has been unmuted.")

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(":x: You don't have permission to unmute members.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":question: Please mention a user to unmute.")
        
@kaii.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):  
    if ctx.author.id == user.id:
        await ctx.send(":x: You can't kick yourself.")
        return
    message = f"You have been kicked by {ctx.author.mention} on {ctx.guild.name} for {reason}"
    await ctx.guild.kick(user)
    await ctx.send(f"User {user.mention} has been kicked for `{reason}`.")
    try: 
        await user.send(message)
    except: 
        return

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(":x: You don't have permission to kick members.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":question: Please mention a user to kick.")

@kaii.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
    if ctx.author.id == user.id:
        await ctx.send(":x: You can't ban yourself.")
        return
    message = f"You have been banned by {ctx.author.mention} on {ctx.guild.name} for {reason}"
    await ctx.guild.ban(user)            
    await ctx.send(f"User {user.mention} has been banned. Reason: {reason}.")
    try:
        await user.send(message)
    except: 
        return

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to ban members.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":question: Please mention a user to ban.")

@kaii.command(name="unban")
@guild_only() 
async def _unban(ctx, id: int):
    user = await kaii.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.send(f"{user} has been unbanned sucessfully, we hope you behave. CAEbbehave :ok_hand:")

@_unban.error
async def _unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(":x: You don't have permission to unban members.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(":question: Please mention a user to unban.")

#utility commands
@kaii.command()
async def ping(ctx):
    await ctx.send(f'Pongina! {round(kaii.latency * 1000)}ms')


@kaii.command()
async def kamusta(ctx):
    await ctx.send(
        'Hello, I am CAEbot. You can call me Kaii. I belong to the Ctrl + Alt + Elite Club. Check us out at https://www.facebook.com/profile.php?id=61551823690869.'
    )

@kaii.command()
async def msg(ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

@msg.error
async def msg_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please give some message!")

@kaii.command(aliases=['tanginamo'])
async def tangina_mo(ctx):
    resbak = [
        'Yawa ka',
        'Pta ka',
        'bole ka tim',
        'kakastiguhon ko ikaw',
        'suntukay nala',
        'himuon ko ikaw na sura'
    ]
    await ctx.message.delete()
    await ctx.send(f'{random.choice(resbak)}')

load_dotenv()
token = os.environ['TOKEN']
kaii.run(token)
