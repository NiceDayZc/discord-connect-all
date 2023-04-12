from websocket import WebSocket # pip install websocket-client
from threading import Thread
from yaml import safe_load # pip install pyyaml
from random import choice
from json import dumps
from time import sleep
from httpx import get


"""
@Remove remove if gay
@Author: github.com/NiceDayZc
"""

def want_channel_id_voice(tokens, server):
    get_channel_id = get(f'https://discord.com/api/v9/guilds/{server}/channels', headers={"content-type": "application/json","authorization": tokens}).json()
    return get_channel_id

def want_random_presence():
    return {"status": choice(["online","dnd","idle"]),"since":0,"activites":[],"afk":False}

def want_to_connect(tokens, server, channel, name):
    try:
        while True:
            ws = WebSocket()
            ws.connect("wss://gateway.discord.gg/?v=8&encoding=json")
            ws.send(dumps({"op": 2,"d": {"token": tokens,"capabilities": 125,"properties": {"os": "iOS","browser": "Safari","device": "iPhone","system_locale": "en-US","browser_user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Mobile/15E148 Safari/604.1","browser_version": "15.1","os_version": "15.1","referrer": "","referring_domain": "","referrer_current": "","referring_domain_current": "","release_channel": "stable","client_build_number": 140268,"client_event_source": None,},"presence": {"status": "online","since": 0,"activities": [{"name": "Custom Status","type": 4,"state": "NiceDayZc Spammer","emoji": None,}],"afk": False,},"compress": False,"client_state": {"guild_hashes": {},"highest_last_message_id": "0","read_state_version": 0,"user_guild_settings_version": -1,"user_settings_version": -1,},},}))
            ws.send(dumps({"op": 4, "d": {"guild_id": server, "channel_id": channel, "self_mute": choice([True, False]),"self_deaf": choice([True, False]), "self_stream?": True, "self_video": False,}}))
            ws.send(dumps({"op": 18,"d": {"type": "guild","guild_id": server,"channel_id": channel,"preferred_region": "singapore"}}))
            print(F"connect {tokens} As #{channel} | {name}")
            sleep(0.1)
            #ws.send(dumps({"op": 5,"d":{"speaking": 1 ,"delay": 0,"ssrc": 0}})) #disconnect channel
    except Exception as e:
        print(e)

if (__name__ == "__main__"):
    want_tokens = open("tokens.txt", 'r').read().splitlines()
    config = safe_load(open("config.yml"))
    for channel in want_channel_id_voice(config["setting"]["token"], config["setting"]["server"]):
        if (channel['type'] == 2):
            for tokens_connect in want_tokens:
                Thread(target=want_to_connect,args=(tokens_connect, config["setting"]["server"], channel['id'], channel['name'],)).start()
