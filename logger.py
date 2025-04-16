from datetime import datetime
import discord

def command_log(command_name: str, ctx: discord.ApplicationContext, message: str = None):
    if message is not None:
        log(f"Slash command /{command_name} by {ctx.author.name}({ctx.author.id}): {message}")
    else:
        if ctx.guild is None:
            log(f"Slash command /{command_name} used by {ctx.author.name}({ctx.author.id}) at DM")
        else: 
            log(f"Slash command /{command_name} used by {ctx.author.name}({ctx.author.id}) at {ctx.channel.name}({ctx.channel.id}) in {ctx.guild.name}({ctx.guild.id})")

def mention_log(msg: discord.Message):
    if msg.guild is None:
        log(f"Bot mentioned by {msg.author.name}({msg.author.id}) at DM")
    else:
        log(f"Bot mentioned by {msg.author.name}({msg.author.id}) at {msg.channel.name}({msg.channel.id}) in {msg.guild.name}({msg.guild.id})")

def log(message: str):
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a") as f:
        f.write(f"[{current_time}] {message}\n")
    return print(f"[{current_time}] {message}")