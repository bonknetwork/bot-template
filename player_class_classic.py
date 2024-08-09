import json
class Player:
    def __init__(self, userid: int):
        self.userid = userid
        self.displayname = ""
        self.roleids = []
        self.ign = ""
        self.guilds = []
        self.blacklisted = False
        self.notes = []
        self.previous_apps = []





class PlayersDB:

    def save_player(self):
        try:
            with open("players.json", "r") as mod_requests_file:
                allplayers_dict = json.load(mod_requests_file)
        except json.decoder.JSONDecodeError:
            allplayers_dict = {}





        with open("players.json", "w") as outfile:
            json.dump(allplayers_dict, outfile)