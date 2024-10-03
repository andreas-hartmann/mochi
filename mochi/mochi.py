import aiohttp
import revolt
import asyncio
import ollama
import logging
import traceback
from config_loader import load_config

logging.basicConfig(level=logging.INFO)  # Set up logging configuration here
config = load_config()
REVOLT_MAX_MESSAGE_LENGTH = 1000

async def run_ollama_prompt(model, prompt):
    try:
        logging.info(f"Running Ollama prompt on model '{model}' with prompt: {prompt}")
        response = await asyncio.to_thread(ollama.generate, model=model, prompt=prompt)
        if 'response' in response:
            return response['response']
        else:
            logging.error(f"Unexpected response from Ollama: {response}")
            return "Error: Unexpected response from model."
    except Exception as e:
        logging.error(f"Error calling Ollama API: {e}")
        traceback.print_exc()
        return "Error: Unable to get response from the model."

class Client(revolt.Client):
    async def on_message(self, message: revolt.Message):
        try:
            if config['BOT_NAME'] in message.raw_mentions:
                mode = config['CHANNELS'].get(message.channel.id, config['DEFAULT_MODE'])
                logging.info(f"CHANNEL: {message.channel.id}, MODE: {mode}, USER: {message.author.id}")

                if mode != config['DEFAULT_MODE'] and message.author.id != config['OWNER_ID']:
                    reply = "ACCESS DENIED - try in another channel :)"
                else:
                    model = config['MODELS'].get(mode)
                    history = ' '.join([historic_message.content for historic_message in reversed(message.state.messages)])
                    prompt = config['PROMPTS'].get(mode).format(
                        server_name = message.channel.server.name,
                        channel_name = message.channel.name,
                        history = history,
                        message = message.content)

                    logging.info(f"PROMPT: {prompt}")

                    reply = await run_ollama_prompt(model, prompt)
                    logging.info(f"REPLY: {reply}")

                chunks = [reply[i:i + REVOLT_MAX_MESSAGE_LENGTH] for i in range(0, len(reply), REVOLT_MAX_MESSAGE_LENGTH)]

                for chunk in chunks:
                    await message.channel.send(chunk)
        except Exception as e:
            logging.error(f"Error handling message: {e}")
            traceback.print_exc()
            await message.channel.send("An error occurred while processing your request.")

async def main():
    try:
        async with aiohttp.ClientSession() as session:
            client = Client(session, config['BOT_TOKEN'])
            await client.start()
    except Exception as e:
        logging.error(f"Error in main bot function: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())