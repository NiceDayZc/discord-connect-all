from websocket import WebSocket
from threading import Thread
from yaml import safe_load
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
            ws.send(dumps({"op": 2, "d": {"token":tokens,"properties": {"os":"Windows","browser":"Chrome","device":"","system_locale":"en-US","os_version":"10"},"presence": want_random_presence(),"compress": False,}}))
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
