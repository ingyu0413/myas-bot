import discord
from discord.commands import slash_command
from discord.ext import commands, tasks
import logger

import asyncio
import random
import json
from itertools import cycle

with open("config.json", "r") as f:
    config = json.load(f)
    token = config["token"]

ACTIVITIES = ["먀아아아",
              "{}곳의 서버에서 오미쿠지 뽑기",
              "{}곳의 서버에서 그루밍"]

activity = cycle(ACTIVITIES)
intents = discord.Intents.default()

class Myas_Bot(discord.AutoShardedBot):
    def __init__(self):
        logger.log("--# 로딩을 시작할게요!")
        super().__init__(
        help_command=None,
        intents=intents,
        debug_guilds=None,
        )
        self.add_cog(CommandsCog(self))
        self.add_cog(CycleCog(self))
    
    async def on_ready(self):
        logger.log("--# 로딩이 완료되었어요!")
        logger.log(f"봇 이름: {self.user.name}")
        logger.log(f"봇 아이디: {self.user.id}")
        logger.log(f"봇 서버 수: {len(self.guilds)}")
        await self.change_presence(status=discord.Status.online)


class CommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger.log("CommandsCog 로딩 성공!")

    @slash_command(name="오미쿠지", description="오미쿠지를 한번 뽑아보세요!")
    async def gacha(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        logger.command_log(ctx)

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
                logger.command_log(ctx, f"Button {self.button_value} clicked by {interaction.user.name}({interaction.user.id})")
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
            logger.command_log(ctx, "Timed out")
            embed = discord.Embed(title="도대체 언제 버튼을 누를 생각인거야... \\:(")
            return await ctx.edit(embed=embed, view=None)
        if not result:
            view.stop()
            if view.button_value == "그만두기":
                logger.command_log(ctx, "Cancelled")
                embed = discord.Embed(title="오미쿠지를 그만뒀어요. \\:(")
                return await ctx.edit(embed=embed, view=None)
            else:
                embed = discord.Embed(title="오미쿠지를 뽑는 중...", description="*\\*샤카샤카\\*... \\*샤카샤카\\*...*")
                await ctx.edit(embed=embed, view=None)
                await asyncio.sleep(3)

                class Button_TIE(discord.ui.View):
                    def __init__(self, ctx: discord.ApplicationContext):
                        super().__init__(timeout=10 + ctx.bot.latency)
                        self.ctx = ctx
                        self.button_value = None
                    
                    @discord.ui.button(label="묶기", style=discord.ButtonStyle.secondary)
                    async def yes(self, button: discord.ui.Button, interation: discord.Interaction):
                        self.button_value = "묶기"
                        self.stop()
                        await interation.response.defer()
                
                    async def interaction_check(self, interaction):
                        logger.command_log(ctx, f"Button {self.button_value} clicked by {interaction.user.name}({interaction.user.id})")
                        if interaction.user != self.ctx.author:
                            await interaction.response.send_message("남의 뽑기는 건들지 말고 뽑기 명령어를 직접 실행하자!", ephemeral=True)
                            self.button_value = None
                            return False
                        else:
                            return True
                        
                results = ["대길", "길", "중길", "소길", "말길", "흉", "대흉"]
                result = random.choice(results)
                logger.command_log(ctx, f"Result = {result}")
                embed = discord.Embed(title=f"{result}이 나왔어요!", description="`오미쿠지 결과 때문에 오늘 하루를 망치지는 말아요!`")
                view = Button_TIE(ctx)
                await ctx.edit(embed=embed, view=view)
                result = await view.wait()

                if result:
                    return await ctx.edit(embed=embed, view=None)
                if not result:
                    view.stop()
                    if view.button_value == "묶기":
                        logger.command_log(ctx, "Tied")
                        embed = discord.Embed(title="오미쿠지 결과를 묶었어요! \\:D", description="`이번 오미쿠지 결과는 묶어두고 다음을 기대해봐요!`")
                        return await ctx.edit(embed=embed, view=None)
                          
    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        if msg.content.startswith(f"<@{self.bot.user.id}>"):
            logger.mention_log(msg)
            a = ""
            try:
                a = msg.content.split()[1]
            except IndexError:
                pass

            responses = ["먀아?", "먀아!", "먀아..."]
            if a == "🀄":
                responses = ["치냐!", "칸냐!", "퐁냐!", "리치냐!", "론냐!", "쯔모냐!"]
            if a == "🎴":
                responses = ["38광땡!", "고!", "스톱!"]
            if a == "🃏":
                responses = ["원카드!"]
            response = random.choice(responses)
            return await msg.channel.send(response)


class CycleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.change_activity.start()
        logger.log("CycleCog 로딩 성공!")

    @tasks.loop(seconds=30)
    async def change_activity(self):
        playing = next(activity).format(len(self.bot.guilds))
        await self.bot.change_presence(activity=discord.Game(name=playing))
    
myasbot = Myas_Bot()
# Token stored at config.json like {"token":"(token)"}
myasbot.run(token=token)