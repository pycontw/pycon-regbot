import os
import logging
import discord
from discord.ext import commands, tasks
from token_import import import_all_token, read_used_list
from dotenv import load_dotenv
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
HELP_DESCRIPTION = os.getenv("HELP_DESCRIPTION")
USED_FILE = os.getenv("USED_FILE_PATH")
STAFF_ROLE_NAME = os.getenv("STAFF_ROLE_NAME")
SPEAKER_ROLE_NAME = os.getenv("SPEAKER_ROLE_NAME")
ATTENDEE_ROLE_NAME = os.getenv("ATTENDEE_ROLE_NAME")

register_brief = "Enter !register TOKEN to register yourself!"
register_help = "Enter  !register TOKEN to register yourself, you should find your own TOKEN in letter or in OPass"
hello_brief = "Say hello to me!"
hello_help = "Just to say hello, nothing special."

token_dict = import_all_token()
used_list = read_used_list()

help_command = commands.help.DefaultHelpCommand(no_category="The commands I am listening on #registration-desk")
bot = commands.Bot(command_prefix='!', description=HELP_DESCRIPTION, help_command=help_command)

def get_roles_from_ticket_type(roles, ticket_type: str):
    if "Contributor" in ticket_type:
        return discord.utils.get(roles, name=STAFF_ROLE_NAME)
    elif "Speaker" in ticket_type:
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
    name = ctx.message.author.display_name
    if ctx.message.channel.type == discord.ChannelType.private or str(ctx.message.channel) != "registration-desk":
        return

    input_token = TOKEN
    print(f"Token {input_token} received from {name}")
    await ctx.message.delete()
    if input_token not in token_dict.keys():
        await ctx.send(f"Sorry {name}, your token is invalid. Please try again, or ask @{STAFF_ROLE_NAME} for help.")
        logging.info(f"{name} has invalid token: {input_token}")
    elif input_token in used_list:
        await ctx.send(f"Sorry {name}, your token has already been used. Please ask @{STAFF_ROLE_NAME} for help.")
        logging.info(f"{name} has token that already been used: {input_token}")
    else:
        given_role = get_roles_from_ticket_type(ctx.message.guild.roles, token_dict[input_token])
        print(f'Giving {name} the role {given_role}')
        await ctx.message.author.add_roles(given_role)
        await ctx.send(f"{ctx.message.author.name} is successfully registered.")
        used_list.append(input_token)
        with open(USED_FILE, 'w+') as f:
            f.write(f"{input_token}\n")
        logging.info(f"{name} used {input_token} to get {given_role} successfully")

@bot.command(brief=hello_brief, help=hello_help)
async def hello(ctx, *, message=None):
    if ctx.message.channel.type == discord.ChannelType.private:
        return
    name = ctx.message.author.display_name
    print(f"Receive Hello from {name}!")
    print(used_list)
    await ctx.send(f"Hello! {name}, you say {message if message else 'nothing'}")

bot.run(BOT_TOKEN)