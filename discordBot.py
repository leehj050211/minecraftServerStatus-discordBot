import discord
from discord.ext.commands import Bot
import requests
import json

url = "https://bssm.kro.kr/minecraft_status"

TOKEN=("토큰")

intents=discord.Intents.default()
bot = Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 에 로그인하였습니다!')

@bot.command()
async def mine(ctx):
    response = requests.get(url)
    if response.status_code == 200:
        data=json.loads(response.text)
        if data['status']!=1:
            if data['status']==2:
                embed = discord.Embed(title="mine.bssm.kro.kr",description="마크 서버가 현재 닫혀있습니다.", color=0x202124)
                await ctx.send("마크 서버", embed=embed)
            elif data['status']==3:
                embed = discord.Embed(title="mine.bssm.kro.kr",description="연결은 되었지만 서버 정보를 불러올 수 없습니다.", color=0x202124)
                await ctx.send("마크 서버", embed=embed)
            else:
                embed = discord.Embed(title="mine.bssm.kro.kr",description="알 수 없는 오류입니다.", color=0x202124)
                await ctx.send("마크 서버", embed=embed)
        else:
            if int(data['players']['online'])>0:
                playersName = ""
                embed = discord.Embed(title="mine.bssm.kro.kr", color=0x202124)
                embed.set_thumbnail(url="https://bssm.kro.kr/icons/server-icon.png")
                for i in range(0, len(data['players']['sample'])):
                    playersName += data['players']['sample'][i]['name']+" "
                embed.add_field(name="접속중인 플레이어 "+str(data['players']['online'])+"/"+str(data['players']['max']),value=playersName, inline=True)
                await ctx.send("마크 서버", embed=embed)
            else:
                embed = discord.Embed(title="mine.bssm.kro.kr", color=0x202124)
                embed.set_thumbnail(url="https://bssm.kro.kr/icons/server-icon.png")
                embed.add_field(name="접속중인 플레이어 "+str(data['players']['online'])+"/"+str(data['players']['max']),value="현재 접속중인 플레이어가 없습니다.", inline=True)
                await ctx.send("마크 서버", embed=embed)
    else : 
        await ctx.send(response.status_code)

bot.run(TOKEN)



# import pymysql

# conn = pymysql.connect(host='127.0.0.1', user='user', password='password', db='db', charset='utf8')
# cur = conn.cursor()

# intents = discord.Intents.default()
# client = discord.Client(intents=intents)
# TOKEN=("토큰")
# @client.event
# async def on_ready():
#     print(f'{client.user} 에 로그인 성공')


# @client.event
# async def on_message(message):
#         query = "SELECT * FROM `discord_bot` WHERE MATCH(`Q`, `title`) AGAINST('"+message.content+"' IN BOOLEAN MODE);"
#         cur.execute(query)
#         row=cur.fetchone()
#         if row==None :
#             await message.reply('해당질문에 대한 답이 없습니다.')
#         else :
#             titleText=row['title']
#             answerText=row['A']
#             await message.reply(""+titleText)
#             await message.reply("답변:"+answerText)
# client.run(TOKEN)