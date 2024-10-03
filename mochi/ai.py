import asyncio
import logging
import traceback
import ollama


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