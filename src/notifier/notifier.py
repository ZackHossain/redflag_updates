import discord
from discord.ext import commands

import asyncio
import threading
from flask import Flask, request, jsonify

import logging

# Flask Details
app = Flask(__name__)

# Bot Details
token = 'MTM4NDEwOTc4ODE5MDczNjQwNA.GR_PTh.b1ASKPg34Pp57d_8upv6Uabox3rHG4Nr8tkVLw'
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)

channel_id = 1384111938228719681

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
        #TODO: Log
        return http_response(400, 'Error: No content provided')
    
    formatted = True
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
    logger.info('Bot Ready')

# Sends a message to (global) channel_id
async def notify_new_article(content):
    channel = client.get_channel(channel_id)
    if channel:
        await channel.send(content)
        logger.info(f'Bot sent message: \"{content}\" to channel_id: {channel_id}')
    else:
        logger.error(f"Channel not found: {channel_id}")

################################
#                              #
#            Logger            #
#                              #
################################

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler()  # also print to console
    ]
)

################################
#                              #
#         Initialisers         #
#                              #
################################

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    threading.Thread(target=run_flask, daemon=True).start()
    client.run(token)