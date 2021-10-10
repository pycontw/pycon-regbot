import discord

def generate_invalid_token_embed():
    embed=discord.Embed(title="很抱歉 您沒有註冊成功 😭", description="We are sorry but your registration is failed 😭", color=0xff0000)
    embed.set_author(name="PyCon TW RegBot")
    embed.add_field(name="原因", value="錯誤的 Token", inline=True)
    embed.add_field(name="Reason", value="Invalid Token", inline=True)
    embed.set_footer(text="請確認您輸入了正確的 token \nPlease make sure you input a valid token.")
    return embed

def generate_already_used_token_embed():
    embed=discord.Embed(title="很抱歉 您沒有註冊成功 😭", description="We are sorry but your registration is failed 😭", color=0xff0000)
    embed.set_author(name="PyCon TW RegBot")
    embed.add_field(name="原因", value="Token 已經被使用", inline=True)
    embed.add_field(name="Reason", value="Token has been used", inline=True)
    embed.set_footer(text="請您聯絡工作人員 @2021-staff \nPlease contact @2021-staff directly")
    return embed

def generate_register_successfully_embed(given_role: str):
    embed=discord.Embed(title="恭喜您註冊成功 😃", description="Well done! You have successfully registered 😃", color=0x00ff00)
    embed.set_author(name="PyCon TW RegBot")
    embed.add_field(name="您的身分組為", value=given_role, inline=True)
    embed.add_field(name="Your role is", value=given_role, inline=True)
    embed.set_footer(text="現在您可以回到 Python Taiwan server 盡情享受會議! \nNow you can back to Python Taiwan server to enjoy this conference!")
    return embed

def howto_in_dm_channel_embed():
    embed=discord.Embed(title="您已經在 DM channel 中 👍", description="You are already in DM channel 👍", color=0xffff00)
    embed.set_author(name="PyCon TW RegBot")
    embed.add_field(name="請輸入下列指令以進行註冊", value="`!register <TOKEN>`", inline=True)
    embed.add_field(name="Please input below command to register", value="`!register <TOKEN>`", inline=True)
    return embed

def howto_in_registration_desk_embed():
    embed=discord.Embed(title="如何快速註冊 🙌", description="How to register yourself 🙌", color=0xffff00)
    f = discord.File("howto.png", filename="howto.png")
    embed.set_author(name="PyCon TW RegBot")
    embed.set_image(url="attachment://howto.png")
    embed.set_footer(text="Note: \n你需要經過註冊後才能看到 PyCon TW 2021 的全部頻道 \nYou have to register first in order to enjoy all channels for PyCon TW 2021")
    return embed, f