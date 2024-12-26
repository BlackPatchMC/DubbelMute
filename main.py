from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
    return "I'm alive!"


def run():
    # Make sure the Flask server runs on 0.0.0.0, and port 8080
    app.run(host='0.0.0.0', port=8080)


Thread(target=run).start()

import os
import discord
from discord.ext import commands

# Define your bot's token
TOKEN = os.getenv("TOKEN")

# The ID of the voice channel to monitor
TARGET_VOICE_CHANNEL_ID = 1316403795034640447  # Replace with your voice channel ID

# Bot intents and command prefix
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_voice_state_update(member, before, after):
    # Check if the user joins or leaves the target channel
    joined_target_channel = after.channel and after.channel.id == TARGET_VOICE_CHANNEL_ID
    left_target_channel = before.channel and before.channel.id == TARGET_VOICE_CHANNEL_ID

    # When joining the target voice channel
    if joined_target_channel and not left_target_channel:
        try:
            # Deafen and mute the member
            await member.edit(deafen=True, mute=True)
            print(
                f"Muted and deafened {member.display_name} in channel {after.channel.name}"
            )
        except discord.Forbidden:
            print(
                f"Permission error: Unable to mute/deafen {member.display_name}."
            )
        except Exception as e:
            print(f"An error occurred: {e}")

    # When leaving the target voice channel (to another channel or disconnecting)
    elif left_target_channel and (not joined_target_channel
                                  or after.channel is None):
        try:
            # Unmute and undeafen the member
            await member.edit(deafen=False, mute=False)
            if after.channel:
                print(
                    f"Unmuted and undeafened {member.display_name} who left channel {before.channel.name}"
                )
            else:
                print(
                    f"Unmuted and undeafened {member.display_name} who disconnected from voice"
                )
        except discord.Forbidden:
            print(
                f"Permission error: Unable to unmute/undeafen {member.display_name}."
            )
        except Exception as e:
            print(f"An error occurred: {e}")


@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")


# Run the bot
bot.run(TOKEN)
