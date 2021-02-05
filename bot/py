import discord
from discord.ext import commands

import requests,os,json,time,asyncio,typing,mcrcon,dotenv

from time import sleep
from mcrcon import MCRcon
from dotenv import load_dotenv
from collections.abc import Sequence

load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')

Client = discord.Client()
client = commands.Bot(command_prefix = "xp!")

@client.event
async def on_ready():
  print ("------------------------------------")
  print ("Bot Name: " + client.user.name)
  print ("Discord Version: " + discord.__version__)
  print ("------------------------------------")
  await client.change_presence(activity=discord.Game(name='on SaladMC'))


def reward(usrid):
	#this need to be edited according to the reward you want to give users


#Important! do not remove!
headers = {
	"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Salad/0.4.2 Chrome/78.0.3904.130 Electron/7.1.9 Safari/537.36'
    }
def make_sequence(seq):
    if seq is None:
        return ()
    if isinstance(seq, Sequence) and not isinstance(seq, str):
        return seq
    else:
        return (seq,)

def message_check(channel=None, author=None, content=None, ignore_bot=True, lower=True):
    channel = make_sequence(channel)
    author = make_sequence(author)
    content = make_sequence(content)
    if lower:
        content = tuple(c.lower() for c in content)
    def check(message):
        if ignore_bot and message.author.bot:
            return False
        if channel and message.channel not in channel:
            return False
        if author and message.author not in author:
            return False
        actual_content = message.content.lower() if lower else message.content
        if content and actual_content not in content:
            return False
        return True
    return check

@client.command(pass_context=True)
async def xpreward(ctx):
	user=ctx.author
  consent = None
	em = discord.Embed(title = "Dm has been sent! Please follow the instructions...")
	em.set_thumbnail(url="https://mir-s3-cdn-cf.behance.net/project_modules/disp/35771931234507.564a1d2403b3a.gif")
	message1 = await ctx.send(embed=em)	

	#Dm user for auth information
	em1 = discord.Embed(title="We need to ask you for permission to use your auth code",color=ctx.author.color, timestamp=ctx.message.created_at)
	em1.add_field(name="The bot will only use:", value='Your minecraft username and XP earned on salad')
	em1.add_field(name="None of the data will be stored in our bot", value='if you agree please type in chat "y" if you deny it please type in chat "n"')

	await user.send(embed=em1)

	check = message_check(author=user, channel=ctx.channel, content=('y','yes','n','no'))
	try:
		msg = await client.wait_for('message',timeout=30,check=check)
		if msg:
			if check.actual_content == 'y' or 'yes':
				consent is True
			elif check.actual_content == 'n' or 'no':
				consent is False
		elif msg is None:
			consent is False
		else:
			consent is False
	except asyncio.TimeoutError:
		timeoutembed = discord.Embed(title="Timeout user did not respond")
		await ctx.send(embed=timeoutembed)


	if consent is True:
		await message1.delete()
		emb = discord.Embed(title = 'waiting for authentication...')
		emb.set_thumbnail(url="https://mir-s3-cdn-cf.behance.net/project_modules/disp/35771931234507.564a1d2403b3a.gif")
		message2= await ctx.send(embed=emb)
		checkauth = message_check(author=user,channel=ctx.channel)
		try:
			msg1 = await client.wait_for('message',timeout=30,check=checkauth)
		except asyncio.TimeoutError:
			timeoutembed = discord.Embed(title="Timeout")
			await ctx.send(embed=timeoutembed)

		salad_auth=check.actual_content
		cookie = {"Salad.Authentication": salad_auth}

		await message2.delete()
		embe = discord.Embed(title='Obtaining data from Salad API...')
		embe.set_thumbnail(url="https://mir-s3-cdn-cf.behance.net/project_modules/disp/35771931234507.564a1d2403b3a.gif")
		message3 = await ctx.send(embed=embe)
		data = requests.get(url = 'https://app-api.salad.io/api/v1/profile/xp', headers = headers, cookies = cookie)
		data = data.json()
		xp = str(data['lifetimeXp'])

		if int(xp) > 100000:
			#send reward
			print(reward(uuid))
			await message3.delete()
			embed = discord.Embed(title="We were able to obtain your request successfully!")
			await ctx.send(embed=embed)

		elif int(xp) < 100000:
			await message3.delete()
			embed = discord.Embed(title=f"You don't have enough exp! you have {xp}/100000")
			await ctx.send(embed=embed)

	elif consent is False:
		await message1.delete()
		emb = discord.Embed(title = 'User denied giving us information we failed to send the reward')
		message2= await ctx.send(embed=emb)
	else:
		await message1.delete()
		emb = discord.Embed(title='Error! undefined answer')
		message2 = await ctx.send(embed=emb)

client.run(token)
