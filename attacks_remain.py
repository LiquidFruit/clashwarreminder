import requests
import json
from datetime import datetime, timedelta

class WarReminder:
    def __init__(self, api_key, clan_tag):
        self.clan_tag = clan_tag
        self.api_key = api_key

    def get_attacks_remaining(self):
        url = "https://api.clashofclans.com/v1/clans/%23" + self.clan_tag + "/currentwar"
        auth = "Bearer " + self.api_key
        headers = {"Authorization": auth}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return []
        
        war_info = json.loads(response.text)

        attacks_left = []
        for member in war_info["clan"]["members"]:
            if member["opponentAttacks"] != 2:
                attacks_left.append(member)
        
        return attacks_left
    
    def get_notify_time(self):
        url = "https://api.clashofclans.com/v1/clans/%23" + self.clan_tag + "/currentwar"
        auth = "Bearer " + self.api_key
        headers = {"Authorization": auth}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return None
        
        war_info = json.loads(response.text)
        war_end = datetime.strptime(war_info["endTime"], "%Y%m%dT%H%M%S.%fZ")

        notify_time = war_end - timedelta(hours=8)
        
        return notify_time