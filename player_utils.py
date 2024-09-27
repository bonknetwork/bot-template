import json
from dataclasses import dataclass, field, asdict
from dataclasses_json import dataclass_json
from typing import Optional, List
from datetime import datetime, timedelta
import time
import os
import requests
import re
import json


@dataclass_json
@dataclass
class Player:
    userid: int
    roles: Optional[list] = None
    ign: Optional[str] = None
    guilds: Optional[str] = None
    blacklisted: Optional[bool] = None
    blacklist_until: Optional[int] = None
    # notes: Optional[dict] = None
    # previous_apps: Optional[dict] = None


class PlayersDB:
    def __init__(self, file_name="players.json"):
        self.file_name = file_name

    def save_player(self, player: Player):
        try:
            with open(self.file_name, "r") as players_file:
                allplayers_dict = json.load(players_file)
        except json.decoder.JSONDecodeError:
            allplayers_dict = {}
        playerdata = player.to_dict()
        del playerdata["userid"]
        allplayers_dict[str(player.userid)] = playerdata
        with open(self.file_name, "w") as outfile:
            json.dump(allplayers_dict, outfile)

    def get_player(self, userid):
        try:
            with open(self.file_name, "r") as players_file:
                allplayers_dict = json.load(players_file)
        except json.decoder.JSONDecodeError:
            allplayers_dict = {}
        userid = str(userid)
        data = allplayers_dict[userid]
        data["userid"] = int(userid)
        try:
            data["blacklist_until"] = int(data["blacklist_until"])
        except:
            pass
        retrieved_player = Player.from_dict(data)
        return retrieved_player

def simple_time_transalte(text):
    time_units = {
        'd': 'days',
        'h': 'hours',
        'm': 'minutes',
        's': 'seconds',
        'w': 'weeks',
        'mo': 'months',  # For months, custom handling will be required.
        'M': 'months',  # Additional alias for months
        'y': 'years'  # For years, custom handling will be required.
    }

    # Handle special cases like "inf", "infinite", "indefinite", "forever"
    if text.lower() in ['inf', 'infinite', 'indefinite', 'forever']:
        return float('inf')  # Infinite future timestamp

    # Regular expression to match patterns like "2d", "3h", "5mo", "1y", etc.
    match = re.match(r'(\d+)([dhmswy]|mo)$', text)
    if match:
        value, unit = match.groups()
        value = int(value)

        # Handle weeks, days, hours, minutes, and seconds with timedelta
        if unit in ['d', 'h', 'm', 's', 'w']:
            unit_name = time_units[unit]
            delta = timedelta(**{unit_name: value})
            future_time = datetime.now() + delta

        # Handle months and years
        elif unit == 'mo':
            future_time = datetime.now().replace(month=datetime.now().month + value)
        elif unit == 'y':
            future_time = datetime.now().replace(year=datetime.now().year + value)

        # Convert future time to Unix timestamp
        unix_timestamp = int(future_time.timestamp())
        return unix_timestamp

    return None

PORT = 9000
def translate_time(text):
    unix_timestamp = simple_time_transalte(text)
    if unix_timestamp is not None:
        return unix_timestamp

    # Fallback to Duckling if no match in advanced parser
    if not text.startswith("in "):
        text = "in " + text

    response = requests.post(f'http://10.1.1.53:{PORT}/parse', data={'locale': 'en_US', 'text': text})
    result = json.loads(response.text)

    if result and isinstance(result, list) and 'value' in result[0]['value']:
        # Extract the ISO 8601 timestamp from the first result
        iso_timestamp = result[0]['value']['value']
        dt = datetime.fromisoformat(iso_timestamp)
        unix_timestamp = int(time.mktime(dt.timetuple()))

        return unix_timestamp
    else:
        # Handle cases where Duckling could not parse the time
        raise ValueError("Could not parse time from input")



if __name__ == '__main__':
    result = translate_time("2days")
    print(result)