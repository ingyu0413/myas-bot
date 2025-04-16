import discord
from discord.commands import slash_command
from discord.ext import commands
import logger

import asyncio
import random
import json

with open("config.json", "r") as f:
  config = json.load(f)
  token = config["token"]

intents = discord.Intents.default()

class Myas_Bot(discord.AutoShardedBot):
  def __init__(self):
    super().__init__(
      help_command=None,
      intents=intents,
      debug_guilds=None,
    )
    self.add_cog(CommandsCog(self))
  
  async def on_ready(self):
    logger.log("--- 로딩이 완료되었어요! ---")
    logger.log(f"봇 이름: {self.user.name}")
    logger.log(f"봇 아이디: {self.user.id}")
    logger.log(f"봇 서버 수: {len(self.guilds)}")
    await self.change_presence(status=discord.Status.online)


class CommandsCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @slash_command(name="오미쿠지", description="오미쿠지를 한번 뽑아보세요!")
  async def gacha(self, ctx: discord.ApplicationContext):
    await ctx.defer()
    logger.log(f"Slash command /오미쿠지 used by {ctx.author.name}({ctx.author.id}) at {ctx.channel.name}({ctx.channel.id}) in {ctx.guild.name}({ctx.guild.id})")

    class Button(discord.ui.View):
      def __init__(self, ctx: discord.ApplicationContext):
        super().__init__(timeout=10 + ctx.bot.latency)
        self.ctx = ctx
        self.button_value = None
      
      @discord.ui.button(label="뽑기!", style=discord.ButtonStyle.green)
      async def yes(self, button: discord.ui.Button, interation: discord.Interaction):
        self.button_value = "뽑기"
        self.stop()
        await interation.response.defer()

      @discord.ui.button(label="그만두기", style=discord.ButtonStyle.red)
      async def cancel(self, button: discord.ui.Button, interation: discord.Interaction):
        self.button_value = "그만두기"
        self.stop()
        await interation.response.defer()
      
      async def interaction_check(self, interaction):
        logger.log(f"Slash command /오미쿠지 by {ctx.author.name}({ctx.author.id}) button clicked by {interaction.user.name}({interaction.user.id})")
        if interaction.user != self.ctx.author:
          await interaction.response.send_message("남의 뽑기는 건들지 말고 뽑기 명령어를 직접 실행하자!", ephemeral=True)
          self.button_value = None
          return False
        else:
          return True
    
    embed = discord.Embed(title="오미쿠지를 뽑을거야?")
    view = Button(ctx)
    await ctx.respond(embed=embed, view=view)

    result = await view.wait()
    if result:
      logger.log(f"Slash command /오미쿠지 by {ctx.author.name}({ctx.author.id}) timed out")
      embed = discord.Embed(title="도대체 언제 버튼을 누를 생각인거야... \\:(")
      return await ctx.edit(embed=embed, view=None)
    if not result:
      view.stop()
      if view.button_value == "그만두기":
        logger.log(f"Slash command /오미쿠지 by {ctx.author.name}({ctx.author.id}) cancelled")
        embed = discord.Embed(title="오미쿠지를 그만뒀어요. \\:(")
        return await ctx.edit(embed=embed, view=None)
      else:
        embed = discord.Embed(title="오미쿠지를 뽑는 중...", description="*\\*샤카샤카\\*... \\*샤카샤카\\*...*")
        await ctx.edit(embed=embed, view=None)
        await asyncio.sleep(3)
        results = ["대길", "길", "중길", "소길", "말길", "흉", "대흉"]
        result = random.choice(results)
        logger.log(f"Slash command /오미쿠지 by {ctx.author.name}({ctx.author.id}) result = {result}")
        embed = discord.Embed(title=f"{result}이 나왔어요!", description="`오미쿠지 결과 때문에 오늘 하루를 망치지는 말아요!`")
        return await ctx.edit(embed=embed, view=None)

  @slash_command(name="먀스", description="먀아아ㅏ")
  async def myas(self, ctx: discord.ApplicationContext):
    logger.log(f"Slash command /먀스 used by {ctx.author.name}({ctx.author.id}) at {ctx.channel.name}({ctx.channel.id}) in {ctx.guild.name}({ctx.guild.id})")
    latency = int(self.bot.latency * 1000)
    await ctx.respond(f"오늘도 먀아아ㅏ 인거에요!\n`ping={latency}ms`")

  @commands.Cog.listener()
  async def on_message(self, msg: discord.Message):
    if msg.content.startswith(f"<@{self.bot.user.id}>"):
      logger.log(f"Bot mentioned by {msg.author.name}({msg.author.id}) at {msg.channel.name}({msg.channel.id}) in {msg.guild.name}({msg.guild.id})")
      responses = ["먀아?", "먀아!", "먀아..."]
      response = random.choice(responses)
      return await msg.channel.send(response)

myasbot = Myas_Bot()
# Token stored at config.json like {"token":"(token)"}
myasbot.run(token=token)