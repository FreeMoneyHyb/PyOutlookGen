import itertools
import json
import time
import multiprocessing
import sys
import threading
import colr
import requests
from tasks.outlook import OutlookAccount, OutlookResponse

config: dict = json.load(open("config.json"))
proxy_iter: iter = itertools.cycle(open("proxies.txt", 'r').read().splitlines())
threads: str = config.get('threads')    
processes: str = config.get('processes')    
sys.stdout.write(colr.color(f"""
▓█████▄  ▒█████   ██▀███  ▄▄▄█████▓     ▄████ ▓█████  ███▄    █ 
▒██▀ ██▌▒██▒  ██▒▓██ ▒ ██▒▓  ██▒ ▓▒    ██▒ ▀█▒▓█   ▀  ██ ▀█   █ 
░██   █▌▒██░  ██▒▓██ ░▄█ ▒▒ ▓██░ ▒░   ▒██░▄▄▄░▒███   ▓██  ▀█ ██▒
░▓█▄   ▌▒██   ██░▒██▀▀█▄  ░ ▓██▓ ░    ░▓█  ██▓▒▓█  ▄ ▓██▒  ▐▌██▒
░▒████▓ ░ ████▓▒░░██▓ ▒██▒  ▒██▒ ░    ░▒▓███▀▒░▒████▒▒██░   ▓██░
 ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░  ▒ ░░       ░▒   ▒ ░░ ▒░ ░░ ▒░   ▒ ▒ 
 ░ ▒  ▒   ░ ▒ ▒░   ░▒ ░ ▒░    ░         ░   ░  ░ ░  ░░ ░░   ░ ▒░
 ░ ░  ░ ░ ░ ░ ▒    ░░   ░   ░         ░ ░   ░    ░      ░   ░ ░ 
   ░        ░ ░     ░                       ░    ░  ░         ░ 
 ░ 
Threads : {threads}, Processes {processes}
Credits Qoft, Dort, FreeMoneyHub
""",fore='red', style='bright'))
time.sleep(2)

def thread_fn():
    while True:
        try:
            proxy_type: str = config.get('proxy-type')
            hook: str = config.get('webhook')
            proxy: str = next(proxy_iter)
            response: OutlookResponse = OutlookAccount(f"{proxy_type}://{proxy}").register_account()
            if response.error:
                if response.error =="SMS Needed":
                    pass
                else:
                    sys.stdout.write(colr.color(f"ERROR: {response.email} [{response.error}]\n",
                                            fore='red', style='bright'))
            else:
                with open("created.txt", "a+") as file:
                    file.write(f"{response.email}:{response.password}\n")
                sys.stdout.write(colr.color(f"CREATED: {response.email}:{response.password}\n",
                                            fore='green', style='bright'))
                requests.post(webhook, data={"content": f"```{response.email}:{response.password}```"}
            sys.stdout.flush()
        except Exception:
            pass


def process_fn():
    for _ in range(config.get("threads")):
        threading.Thread(target=thread_fn).start()


if __name__ == '__main__':
    for _ in range(config.get("processes")):
        multiprocessing.Process(target=process_fn).start()
