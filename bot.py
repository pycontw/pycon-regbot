import os
import logging
import discord
from discord.ext import commands
from token_import import import_all_token, read_used_list
from dotenv import load_dotenv
from embed_builder import *
load_dotenv()

# logging config
logging.basicConfig(
    filename=".log/reg.log",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%b-%d %H:%M:%S",
)

# Defined in .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
USED_FILE = os.getenv("USED_FILE_PATH")
STAFF_ROLE_NAME = os.getenv("STAFF_ROLE_NAME")
SPEAKER_ROLE_NAME = os.getenv("SPEAKER_ROLE_NAME")
ATTENDEE_ROLE_NAME = os.getenv("ATTENDEE_ROLE_NAME")

register_brief = "輸入 `!register <TOKEN>` 以註冊 Enter `!register <TOKEN>` to register!"
register_help = "在與我的 DM channel 中直接輸入  `!register <TOKEN>` 以進行註冊 \n Enter `!register <TOKEN>` in the DM channel with me"
hello_brief = "跟我說聲嗨! Say hello to me!"
hello_help = "只是跟我打聲招呼 沒有什麼特別的 \n Just to say hello, nothing special."
howto_brief = "提示您如何註冊 How to register yourself?"
howto_help = "提供指南讓您能夠了解如何註冊 \n Give you an instruction about registration."
help_description = "您需要幫助嗎? Do you need help?"

token_dict = import_all_token()
used_list = read_used_list()

help_command = commands.help.DefaultHelpCommand(no_category="我的指令列表 The commands I am listening")
bot = commands.Bot(command_prefix='!', description=help_description, help_command=help_command)

def get_roles_from_ticket_type(roles, ticket_type: str):
    if "contributor" in ticket_type:
        return discord.utils.get(roles, name=STAFF_ROLE_NAME)
    elif "speaker" in ticket_type:
        return discord.utils.get(roles, name=SPEAKER_ROLE_NAME)
    else:
        return discord.utils.get(roles, name=ATTENDEE_ROLE_NAME)

# ---------------------------------------
# Bot Initialization
# ---------------------------------------
@bot.event
async def on_ready():
    listening_activity = discord.Activity(type=discord.ActivityType.listening, name="!register")
    await bot.change_presence(activity=listening_activity)
    print(f'Registration bot is ready. Token count: {len(token_dict)}')
    logging.info(f"Token count: {len(token_dict)}")
    logging.info('Registration bot is ready.')


# ---------------------------------------
# Command
# ---------------------------------------
@bot.command(brief=register_brief, help=register_help)
async def register(ctx, *, TOKEN=None):
    server = bot.get_guild(int(GUILD_ID))

    name = ctx.message.author.display_name
    if ctx.message.channel.type != discord.ChannelType.private:
        return

    input_token = TOKEN
    print(f"Token {input_token} received from {name}")
    if input_token not in token_dict.keys():
        await ctx.send(embed=generate_invalid_token_embed())
        logging.info(f"{name} has invalid token: {input_token}")
    elif input_token in used_list:
        await ctx.send(embed=generate_already_used_token_embed())
        logging.info(f"{name} has inputted token that already been used: {input_token}")
    else:
        given_role = get_roles_from_ticket_type(server.roles, token_dict[input_token])
        member = await server.fetch_member(ctx.message.author.id)
        print(f'Giving {name} the role {given_role}')
        await member.add_roles(given_role)
        used_list.append(input_token)
        with open(USED_FILE, 'a') as f:
            f.write(f"{input_token}\n")
        logging.info(f"{name} used {input_token} to get {given_role} successfully")
        await ctx.send(embed=generate_register_successfully_embed(given_role))

@bot.command(brief=hello_brief, help=hello_help)
async def hello(ctx, *, message=None):
    if ctx.message.channel.type != discord.ChannelType.private:
        return
    name = ctx.message.author.display_name
    await ctx.send(f"Hello! {name}, you say {message if message else 'nothing'}")

@bot.command(brief=howto_brief, help=howto_help)
async def howto(ctx, *, message=None):
    if ctx.message.channel.type == discord.ChannelType.private:
        await ctx.send(embed=howto_in_dm_channel_embed())
    elif ctx.channel.name == "⚠｜registration-desk":
        embed, f = howto_in_registration_desk_embed()
        await ctx.send(embed=embed, file=f)

bot.run(BOT_TOKEN)