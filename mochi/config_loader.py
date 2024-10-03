import toml
import logging
import os

def load_config(config_file='../config/config.toml'):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, config_file)
    try:
        logging.info(f"Loading config file {config_file_path}")
        config = toml.load(config_file_path)

        bot_config = config['bot']
        api_config = config['api']
        models_config = config['models']
        prompts_config = config['prompts']
        channels_config = config['channels']
        default_config = config['default']

        return {
            'BOT_NAME': bot_config['id'],
            'OWNER_ID': bot_config['owner_id'],
            'BOT_TOKEN': bot_config['token'],
            'OLLAMA_API_URL': api_config['url'],
            'MODELS': models_config,
            'PROMPTS': prompts_config,
            'CHANNELS': channels_config,
            'DEFAULT_MODE': default_config['mode']
        }
    except FileNotFoundError as e:
        print(f"Error loading config: {e}")
        raise
    except KeyError as e:
        logging.error(f"Missing required configuration section or key: {e}")
        raise
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        raise