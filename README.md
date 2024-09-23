# mochi

This is a basic LLM-based chatbot for the chat app Revolt. It supports per channel models and prompts as well as
automatic transient history keeping.

## Requirements
* Only runs on Python 3.10 right now.
* Requires an Ollama backend. 

It's easy to set up and configure:

* Clone the repo.
* In the config directory, copy config.toml.template to config.toml.
* Create a bot in the My Bots section in the Revolt settings.
* Add the bot to a server of your choosing.
* In the toml file: Add your token and adjust the other parameters as desired.

That's it! Just mention the bot in a message and wait for the reply.
There are some minor known issues that I may fix over time if there is demand.
