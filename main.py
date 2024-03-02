import yaml
import threading
import selenium
import time, random
import sys, datetime
from colorama import Fore, Style
import webbrowser

webbrowser.open("https://guns.lol/severity")

sys.dont_write_bytecode = True
from source.headers import Headers
from source.client import CreateClient

config_yaml = yaml.safe_load(open("config.yaml", "r"))
token_json = open('input/tokens.txt').read().split("\n")
vouch_json = open(f"input/vouch.txt", encoding="utf-8").read().split("\n")

client = CreateClient()
token_index = vouch_index = total_count = 0
random.shuffle(vouch_json)
random.shuffle(token_json)

class Printer:
    def __init__(self) -> None:
        self.lock = threading.Lock()
    
    def curr_time(self):
        data = datetime.datetime.now().strftime("%H:%M:%S")
        return data

    def success(self, title: str, desc: str):
        self.lock.acquire()
        time = Printer.curr_time(self)
        print(
            f"""{Fore.LIGHTBLACK_EX}[{time}] [{total_count}] {Fore.LIGHTBLUE_EX}{title}{Fore.LIGHTWHITE_EX} : {Fore.LIGHTGREEN_EX}{desc}{Style.RESET_ALL}"""
        )
        self.lock.release()

    def denied(self, title: str, desc: str):
        self.lock.acquire()
        time = Printer.curr_time(self)
        print(
            f"""{Fore.LIGHTBLACK_EX}[{time}] [{total_count}] {Fore.LIGHTYELLOW_EX}{title}{Fore.LIGHTWHITE_EX} : {Fore.LIGHTRED_EX}{desc}{Style.RESET_ALL}"""
        )
        self.lock.release()

print_obj = Printer()
while total_count < config_yaml['Number']:
    format_str = random.choice(config_yaml['formats'])
    vouch_json[vouch_index] = vouch_json[vouch_index].rstrip()
    req = None
    try:
        req = client.post(
            url="https://discord.com/api/v9/channels/{}/messages".format(config_yaml['ChannelId']),
            headers=Headers.get_headers(client, token_json[token_index]),
            json={
                "content": "{} <@{}> {}".format(
                    format_str, random.choice(config_yaml['VouchOwner']), vouch_json[vouch_index])
            }
        )
    except:
        pass

    if req and req.status_code == 200:
        total_count += 1
        print_obj.success(title='Vouch Sent', desc=vouch_json[vouch_index])
    else:
        if req and req.text:
            print_obj.denied(title='Vouch Error', desc=req.json().get("message"))
        else:
            print_obj.denied(title='Vouch Error', desc="Request Not Sent") 
    
    vouch_index += 1
    token_index += 1

    if vouch_index >= len(vouch_json):
        random.shuffle(vouch_json)
        vouch_index = 0

    if token_index >= len(token_json):
        random.shuffle(token_json)
        token_index = 0
    
    rand_time = random.randint(
        int(config_yaml['TimeLimit']['low']), 
        int(config_yaml['TimeLimit']['high'])
    )
    time.sleep(rand_time)
