import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from token_import import import_all_token

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
HELP_DESCRIPTION = os.getenv("HELP_DESCRIPTION")

register_brief = "Enter !register TOKEN to register yourself!"
register_help = "Enter  !register TOKEN to register yourself, you should find your own TOKEN in letter or in OPass"
hello_brief = "Say hello to me!"
hello_help = "Just to say hello, nothing special."

token_dict = import_all_token()

help_command = commands.help.DefaultHelpCommand(no_category="The commands I am listening")
bot = commands.Bot(command_prefix='!', description=HELP_DESCRIPTION, help_command=help_command)

def get_roles_from_ticket_type(roles, ticket_type: str):
    if "Contributor" in ticket_type:
        return discord.utils.get(roles, name="2020-staff")
    elif "Speaker" in ticket_type:
        return discord.utils.get(roles, name="2020-speaker")
    else:
        return discord.utils.get(roles, name="2020-attendee")

# ---------------------------------------
# Bot Initialization
# ---------------------------------------
@bot.event
async def on_ready():
    listening_activity = discord.Activity(type=discord.ActivityType.listening, name="!register")
    await bot.change_presence(activity=listening_activity)
    print('Registration bot is ready.')


# ---------------------------------------
# Command
# ---------------------------------------
@bot.command(brief=register_brief, help=register_help)
async def register(ctx, *, TOKEN=None):
    name = ctx.message.author.display_name
    if ctx.message.channel.type == "dm" or str(ctx.message.channel) != "test-registration-desk":
        return

    input_token = TOKEN
    print(f"Token {input_token} received from {name}")
    await ctx.message.delete()
    if input_token not in token_dict.keys():
        await ctx.send(f"Sorry {name}, your token is incorrect. Please try again, or ask @2020-staff for help.")
    else:
        given_role = get_roles_from_ticket_type(ctx.message.guild.roles, token_dict[input_token])
        print(f'Giving {name} the role {given_role}')
        await ctx.message.author.add_roles(given_role)
        await ctx.send(f"{ctx.message.author.name} is successfully registered.")

@bot.command(brief=hello_brief, help=hello_help)
async def hello(ctx, *, message=None):
    name = ctx.message.author.display_name
    print(f"Receive Hello from {name}!")
    await ctx.send(f"Hello! {name}, you say {message if message else 'nothing'}")

bot.run(BOT_TOKEN)