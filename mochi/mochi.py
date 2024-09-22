import aiohttp
import revolt
import asyncio
import ollama
import logging
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

logging.basicConfig(level=logging.INFO)
logging.getLogger('revolt').setLevel(logging.WARN)

BOT_NAME = config['bot']['id']
OWNER_ID = config['bot']['owner_id']
BOT_TOKEN = config['bot']['token']
OLLAMA_API_URL = config['api']['url']
MODELS = {k: v for k, v in config.items('models')}
PROMPTS = {k: v for k, v in config.items('prompts')}
CHANNELS = {k: v for k, v in config.items('channels')}
DEFAULT_MODE = config['default']['mode']

def run_ollama_prompt(model, prompt):
    return ollama.generate(model=model, prompt=prompt)

class Client(revolt.Client):
    async def on_message(self, message: revolt.Message):
        if BOT_NAME in message.raw_mentions:
            mode = CHANNELS.get(message.channel.id, DEFAULT_MODE)
            logging.info("CHANNEL: " + message.channel.id)
            logging.info("MODE: " + mode)
            if mode != DEFAULT_MODE and message.author.id != OWNER_ID:
                reply = "ACCESS DENIED - try in another channel :)"
            else:
                model = MODELS.get(mode)
                history = message.state.messages
                context = ' '.join([msg.content for msg in reversed(history)])
                prompt = PROMPTS.get(mode).format(context, message.content)
                logging.info("PROMPT: " + prompt)
                msg = run_ollama_prompt(model, prompt)
                reply = msg['response']
                logging.info("REPLY: " + reply)
            await message.channel.send(reply)


async def main():
    async with aiohttp.ClientSession() as session:
        client = Client(session, BOT_TOKEN)
        await client.start()

asyncio.run(main())