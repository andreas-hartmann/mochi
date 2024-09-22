import configparser
import logging

def load_config(config_file='../config/config.ini'):
    config = configparser.ConfigParser()
    try:
        config.read(config_file)

        # Required sections and keys
        bot_config = config['bot']
        api_config = config['api']
        models_config = dict(config.items('models'))
        prompts_config = dict(config.items('prompts'))
        channels_config = dict(config.items('channels'))
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
    except KeyError as e:
        logging.error(f"Missing required configuration section or key: {e}")
        raise
    except Exception as e:
        logging.error(f"Error loading config: {e}")
        raise