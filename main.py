import requests
import json
import sys
import attacks_remain
from discord_bot import bot, set_clash_api_key
import threading

clash_api_key = None

def run_bot(api):
    bot.run(api)

def main():
    global clash_api_key
    # Check if the correct number of arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python main.py <Clash of Clans API key> <Discord Bot API key>")
        sys.exit(1)

    clash_api_key = sys.argv[1]
    discord_bot_api_key = sys.argv[2]

    set_clash_api_key(clash_api_key)

    bot_thread = threading.Thread(target=run_bot, args=(discord_bot_api_key,))
    bot_thread.start()

    bot_thread.join()

if __name__ == "__main__":
    main()