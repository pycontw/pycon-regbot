import os
import discord

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
HELP_MESSAGE = os.getenv("HELP_MESSAGE")

activity = discord.Activity(name="!register", type=discord.ActivityType.listening)
client = discord.Client(activity=activity)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message.author.display_name)
    if message.author == client.user or str(message.channel) != "registration-desk":
        return

    if message.content.startswith('!hello'):
        print("Get Hello!")
        await message.channel.send('Hello! {}'.format(message.author.name))
    elif message.content.startswith('!help'):
        await message.channel.send(HELP_MESSAGE)
    elif message.content.startswith('!register ') and message.author.display_name == "JordanTest":
        context = message.content.strip('!register ').split(',')
        full_name, code = context[0].strip(), context[1].strip()
        roles_list = message.guild.roles
        this_role = next(role for role in roles_list if role.name == "2020-staff")
        print(f'Giving {full_name} the role {this_role.name}')
        await message.author.add_roles(this_role)
        await message.channel.send('{} is successfully registered'.format(message.author.name))

client.run(BOT_TOKEN)