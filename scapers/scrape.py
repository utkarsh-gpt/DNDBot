from sel_scrape import scrape
import json

base_url = "https://5e.tools/data/"

# class_endpoints = {
#  "artificer": "class-artificer.json",
#  "barbarian": "class-barbarian.json",
#  "bard": "class-bard.json",
#  "cleric": "class-cleric.json",
#  "druid": "class-druid.json",
#  "fighter": "class-fighter.json",
#  "monk": "class-monk.json",
#  "paladin": "class-paladin.json",
#  "ranger": "class-ranger.json",
#  "rogue": "class-rogue.json",
#  "sorcerer": "class-sorcerer.json",
#  "warlock": "class-warlock.json",
#  "wizard": "class-wizard.json"
# }

def get_object(object):
    index_json = scrape(base_url + object + "/index.json")

    for item in index_json.values():
        url = base_url + object + '/' + item
        response = scrape(url)
        with open(f"{object}/{item}", "w") as file:
            json.dump(response, file)



get_object("races")

