# Made by Severityc on Github | Licensed (MIT)
# This was made for educational purposes only
# Find the latest version at https://github.com/severityc/Fake-Vouch
# Updated 09/01/2024

import requests
import random
import time
import json
import os 

DARK_BLUE = '\033[34m'
NEON_GREEN = '\033[92m'
RESET = '\033[0m'

def title_fuck():
    ascii_art = """
 _____ _    _  _______  __     _____  _   _  ____ _   _ 
|  ___/ \\  | |/ / ____| \\ \\   / / _ \\| | | |/ ___| | | |      Made By Severityc
| |_ / _ \\ | ' /|  _|    \\ \\ / / | | | | | | |   | |_| |     github.com/severityc/Fake-Vouch
|  _/ ___ \\| . \\| |___    \\ V /| |_| | |_| | |___|  _  |
|_|/_/   \\_\\_|\\_\\_____|    \\_/  \\___/ \\___/ \\____|_| |_|
    """
    print(f"{DARK_BLUE}{ascii_art}{RESET}")
    print(f"{NEON_GREEN}Made by Severityc | github.com/severityc{RESET}")

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_config():
    with open("input/config.json", "r", encoding="utf-8") as config_file:
        return json.load(config_file)

def load_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().splitlines()

def send_messages(config, tokens, messages):
    user_id = config['user_id']
    channel_id = config['channel_id']
    wait_time = config['wait_time']
    message_count = config['message_count']
    vouch_format = ['vouch', 'rep', '+vouch', '+rep']

    useragent_headers = {
        "authority": "discord.com",
        "accept": "*/*",
        "accept-language": "en-US",
        "connection": "keep-alive",
        "content-type": "application/json",
        "origin": "https://discord.com",
        "referer": "https://discord.com/channels/@me",
        "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9015 Chrome/108.0.5359.215 Electron/22.3.2 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "en-US",
        "x-discord-timezone": "America/New_York",
    }

    title_fuck()  

    for token in tokens:
        headers = useragent_headers.copy()
        headers["Authorization"] = token

        for _ in range(message_count):
            reason_message = random.choice(messages)
            user_ping = f"<@{user_id}>"
            rep_command = random.choice(vouch_format)
            message_content = f"{rep_command} {user_ping} {reason_message}"

            message_payload = {
                "content": message_content
            }

            response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=message_payload)

            if response.status_code == 200:
                print(f"{DARK_BLUE}Vouch Sent {RESET}: {NEON_GREEN}{message_content}{RESET}")
            else:
                print(f"Failed to send message. Status code: {response.status_code}")

            time.sleep(wait_time)

if __name__ == "__main__":
    title_fuck()  
    input("Press Enter to start the Fake Vouch...")
    clear_console()  
    config = load_config()
    tokens = load_lines("input/tokens.txt")
    messages = load_lines("input/reasons.txt")
    send_messages(config, tokens, messages)
