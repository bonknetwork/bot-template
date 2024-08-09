import json
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Optional, List
import datetime


@dataclass_json
@dataclass
class Player:
    userid: int
    roles: Optional[int] = None
    ign: Optional[str] = None
    guilds: Optional[str] = None
    blacklisted: Optional[bool] = None
    blacklist_until: Optional[datetime.datetime] = None
    #notes: Optional[dict] = None
    #previous_apps: Optional[dict] = None


class PlayersDB:
    def save_player(self, player: Player):
        try:
            with open("players.json", "r") as players_file:
                allplayers_dict = json.load(players_file)
        except json.decoder.JSONDecodeError:
            allplayers_dict = {}
        playerdata = player.to_dict()
        del playerdata["userid"]
        playerdata["blacklist_until"] = playerdata["blacklist_until"].strftime("%Y-%m-%d %H:%M:%S.%f")
        allplayers_dict[player.userid] = playerdata
        with open("players.json", "w") as outfile:
            json.dump(allplayers_dict, outfile)

    def get_player(self, id):
        try:
            with open("players.json", "r") as players_file:
                allplayers_dict = json.load(players_file)
        except json.decoder.JSONDecodeError:
            allplayers_dict = {}
        id = str(id)
        data = allplayers_dict[id]
        data["userid"] = id
        data["blacklist_until"] = datetime.strptime(data["blacklist_until"], "%Y-%m-%d %H:%M:%S.%f")
        new_player = Player.from_dict(data)
        return new_player


id = 3123213123
player = Player(userid=id, ign="helothere", blacklist_until=datetime.datetime.now())
print(player.blacklist_until)
playersdb = PlayersDB()
playersdb.save_player(player)
new_player = playersdb.get_player(id)
if new_player == player:
    print("hi")