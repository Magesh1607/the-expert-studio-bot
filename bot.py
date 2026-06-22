import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

Thread(target=run).start()

import discord
from discord.ext import commands
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO 

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is online!")


@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel

    try:
        # Download avatar
        response = requests.get(member.display_avatar.url)
        avatar = Image.open(BytesIO(response.content)).convert("RGBA")
        avatar = avatar.resize((250, 250))

        # Create circular mask
        mask = Image.new("L", (250, 250), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 250, 250), fill=255)

        # Open background
        img = Image.open("welcome_bg.jpeg").convert("RGBA")

        # Paste circular avatar
        img.paste(avatar, (322, 530), mask)

        # Draw username
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf",55)
        except:
            font = ImageFont.load_default()

        username = member.display_name

        bbox = draw.textbbox((0, 0), username, font=font)
        text_width = bbox[2] - bbox[0]

        x = 900 - (text_width // 2)
        y = 580

        draw.text(
            (x, y),
            username,
            fill="white",
            font=font
        )

        # Save image
        img.save("welcome_output.png")

        # Send welcome image
        if channel:
            await channel.send(
                f"🎉 Welcome {member.mention} to The Expert Studio!",
                file=discord.File("welcome_output.png")
            )

    except Exception as e:
        print("ERROR:", e)


bot.run(TOKEN)