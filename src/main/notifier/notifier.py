import json

import discord
from discord.ext import commands

import asyncio
import threading
from flask import Flask, request, jsonify

from log import log_error, log_info

# Flask globals
app = Flask(__name__)

# Bot globals
token = None
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)
channel_id = None

MAX_LEN = 1000

################################
#                              #
#          Flask App           #
#                              #
################################

@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    content = data.get('content')
    
    if not content:
        return http_response(400, 'Error: No content provided')
    
    formatted = True
    if len(content) > MAX_LEN:
        content = content[0:MAX_LEN]
    if not formatted:
        return http_response(400, 'Notifications not formatted correctly')
    
    # Run the coroutine and wait for it to finish
    asyncio.run_coroutine_threadsafe(notify_new_article(content), client.loop)
    res = http_response(200, 'Success')
    return res

def http_response(code, status):
    return jsonify({
        'status': status
    }), code

def run_flask():
    app.run(host='127.0.0.1', port=5000)

################################
#                              #
#     Discord Bot Handler      #
#                              #
################################

# Logs when Bot is ready
@client.event
async def on_ready():
    log_info('Bot Ready')

# Sends a message to (global) channel_id
async def notify_new_article(content):
    channel = await client.get_channel(channel_id)
    if channel:
        await channel.send(content)
        log_info(f'Bot sent message: \"{content}\" to channel_id: {channel_id}')
    else:
        log_error(f"Channel not found: {channel_id}")

################################
#                              #
#         Initialisers         #
#                              #
################################

def load_creds():
    global token
    global channel_id
    
    with open('credentials.json', 'r') as creds:
        data = json.load(creds)
        token = data['bot_token']
        channel_id = data['channel_id']
    

if __name__ == '__main__':
    load_creds()
    threading.Thread(target=run_flask, daemon=True).start()
    client.run(token)