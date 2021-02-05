import discord
from discord.ext import commands

import requests,os,json,time,asyncio,typing,dotenv

from time import sleep
from dotenv import load_dotenv
from collections.abc import Sequence

load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')

consent = None

Client = discord.Client()
client = commands.Bot(command_prefix = "xp!")

@client.event
async def on_ready():
  print ("------------------------------------")
  print ("Bot Name: " + client.user.name)
  print ("Discord Version: " + discord.__version__)
  print ("------------------------------------")
  await client.change_presence(activity=discord.Game(name='on Salad'))


def reward(usrid):
  #Write your reward code here

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
        if content and message.content not in content:
            return False
        return True
    return check

@client.command(pass_context=True)
async def xpreward(ctx):
	user=ctx.author

	em = discord.Embed(title = "Please follow the instructions sent in dms...")
	em.set_thumbnail(url="https://mir-s3-cdn-cf.behance.net/project_modules/disp/35771931234507.564a1d2403b3a.gif")
	message1 = await ctx.send(embed=em)	

	#Dm user for auth information
	em1 = discord.Embed(title="We need to ask you for permission to use your auth code",color=ctx.author.color, timestamp=ctx.message.created_at)
	em1.add_field(name="The bot will only use:", value='XP earned on salad')
	em1.add_field(name="None of the data will be stored in our bot", value='if you agree please type in chat "y" if you deny it please type in chat "n"')

	await user.send(embed=em1)

	check = message_check(channel=user.dm_channel,author=user,content=('yes','no','y','n'),ignore_bot=True,lower=True)
	try:
		msg = await client.wait_for('message',timeout=15,check=check)
		if msg:
			if msg.content.lower().strip() == "yes" or "y":
				consent = True
			elif msg.content.lower().strip() == 'no' or 'n':
				consent = False
		elif msg is None:
			consent = False
		else:
			consent = False
	except asyncio.TimeoutError:
		timeoutembed = discord.Embed(title="Timeout user did not respond")
		await ctx.send(embed=timeoutembed)


	if consent is True:
		await message1.delete()
		emb = discord.Embed(title = 'waiting for authentication...')
		emb.set_thumbnail(url="https://mir-s3-cdn-cf.behance.net/project_modules/disp/35771931234507.564a1d2403b3a.gif")
		message2= await ctx.send(embed=emb)
		message4 = await user.send(embed=emb)

		embedus = discord.Embed(title='How can I find my salad auth code? dont worry you have 2 minutes to do it!')
		embedus.add_field(name='Go to app.salad.io and login with your Salad account.', value='-=-=-=-=-=-=-=-=-')
		embedus.add_field(name='Click on the Cookies icon which looks like a lock on the left of the address bar.',value='-=-=-=-=-=-=-=-=-')
		embedus.add_field(name='Click on Cookies.',value='-=-=-=-=-=-=-=-=-')
		embedus.add_field(name='Open the app-api.salad.io folder.',value='-=-=-=-=-=-=-=-=-')
		embedus.add_field(name='Open the Cookies folder.',value='-=-=-=-=-=-=-=-=-')
		embedus.add_field(name='Click on Salad.Authentication.',value='-=-=-=-=-=-=-=-=-')
		embedus.add_field(name='Double click on the Content in the Salad.Authentication folder.',value='-=-=-=-=-=-=-=-=-')

		message5 = await user.send(embed=embedus)


		checkauth = message_check(author=user,channel=user.dm_channel,ignore_bot=True,lower=True)
		try:
			msg1 = await client.wait_for('message',timeout=120,check=checkauth)
			salad_auth = str(msg1.content)
			cookie = {"Salad.Authentication": salad_auth}
			dataobtained = True
		except asyncio.TimeoutError:
			timeoutembed = discord.Embed(title="Timeout user did not respond")
			await ctx.send(embed=timeoutembed)
			dataobtained = False
		await message4.delete()
		await message5.delete()
		await message2.delete()
		if dataobtained is True:
			embe = discord.Embed(title='Obtaining data from Salad API...')
			embe.set_thumbnail(url="https://mir-s3-cdn-cf.behance.net/project_modules/disp/35771931234507.564a1d2403b3a.gif")
			message3 = await ctx.send(embed=embe)
			try:
				data = requests.get(url = 'https://app-api.salad.io/api/v1/profile/xp', headers = headers, cookies = cookie).json()
				xp = str(data['lifetimeXp'])
			except asyncio.ConnectionRefusedError:
				print('Connection refused')
				Errorcode = 10061
				consent = None
			except asyncio.JSONDecodeError:
				print('Wrong Auth Code')
				Errorcode = 404
				consent = None
			if int(xp) > 100000:
				#send reward
				reward(uuid)
				await message3.delete()
				embed = discord.Embed(title="We were able to obtain your request successfully!")
				await ctx.send(embed=embed)

			elif int(xp) < 100000:
				await message4.delete()
				await message5.delete()
				await message3.delete()
				embed = discord.Embed(title=f"You don't have enough exp! you have {xp}/100000")
				await ctx.send(embed=embed)
		elif dataobtained is False:
			consent = None
		else:
			consent = None
	elif consent is False:
		await message1.delete()
		emb = discord.Embed(title = 'User denied giving us information we failed to send the reward')
		message2= await ctx.send(embed=emb)
	else:
		await message1.delete()
		emb = discord.Embed(title=f'Error!: {str(Errorcode)}')
		message2 = await ctx.send(embed=emb)

client.run(token)
