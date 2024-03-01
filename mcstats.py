import requests
import json
from mojang import API

_uuid_cache = {}
_pseudo_cache = {}

def pseudo_uuid(username):
    if username in _uuid_cache:
        return _uuid_cache[username]
    else:
        uuid = API().get_uuid(username)
        _uuid_cache[username] = uuid
        return uuid

def uuid_pseudo(uuid):
    if uuid in _pseudo_cache:
        return _pseudo_cache[uuid]
    else:
        pseudo = API().get_username(uuid)
        _pseudo_cache[uuid] = pseudo
        return pseudo
        
def strjsonfile(string):
    if string == None:
        return None
    else:
        return string[:8] + "-" + string[8:12] + "-" + string[12:16] + "-" + string[16:20] + "-" + string[20:] + ".json"

def gettime(json):
    if "stats" in json and "minecraft:custom" in json["stats"] and "minecraft:play_time" in json["stats"]["minecraft:custom"]:
        return round((json["stats"]["minecraft:custom"]["minecraft:play_time"]/1200)/60,2)
    return 0

def getjump(json):
    if "stats" in json and "minecraft:custom" in json["stats"] and "minecraft:jump" in json["stats"]["minecraft:custom"]:
        return json["stats"]["minecraft:custom"]["minecraft:jump"]
    return 0

def getcloche(json):
    if "stats" in json and "minecraft:custom" in json["stats"] and "minecraft:bell_ring" in json["stats"]["minecraft:custom"]:
        return json["stats"]["minecraft:custom"]["minecraft:bell_ring"]
    return 0

def getminer(json):
    if "stats" in json and "minecraft:mined" in json["stats"]:
        json = json["stats"]["minecraft:mined"]
        total_mined = 0
        most_mined_mob = ""
        most_mined_count = 0
        for mob, count in json.items():
            total_mined += count
            if count > most_mined_count:
                most_mined_count = count
                most_mined_mob = mob
        return (total_mined, most_mined_mob, (most_mined_count*100)//total_mined)
    return 0

def getmort(json):
    if "stats" in json and "minecraft:killed_by" in json["stats"]:
        total_killed = json["stats"]["minecraft:custom"]["minecraft:deaths"]
        json = json["stats"]["minecraft:killed_by"]
        total_killed2 = 0
        most_killed_mob = ""
        most_killed_count = 0
        for mob, count in json.items():
            total_killed2 += count
            if count > most_killed_count:
                most_killed_count = count
                most_killed_mob = mob
        return (total_killed, most_killed_mob, (most_killed_count*100)//total_killed)
    return 0

def getdistance(json):
    keys = ["minecraft:swim_one_cm", "minecraft:fly_one_cm", "minecraft:fall_one_cm", "minecraft:horse_one_cm", "minecraft:sprint_one_cm", "minecraft:walk_on_water_one_cm", "minecraft:walk_under_water_one_cm", "minecraft:boat_one_cm", "minecraft:minecart_one_cm"]
    distance = 0
    for key in keys:
        if key in json["stats"]["minecraft:custom"]:
            distance += json["stats"]["minecraft:custom"][key]
    if distance == 0:
        return 0
    return round(float(distance)/100000, 2)

def getbroke(json):
    if "stats" in json and "minecraft:broken" in json["stats"]:
        return sum([json["stats"]["minecraft:broken"][i] for i in json["stats"]["minecraft:broken"]])
    return 0

def getkilled(json):
    if "stats" in json and "minecraft:killed" in json["stats"]:
        json = json["stats"]["minecraft:killed"]
        total_killed = 0
        most_killed_mob = ""
        most_killed_count = 0
        for mob, count in json.items():
            total_killed += count
            if count > most_killed_count:
                most_killed_count = count
                most_killed_mob = mob
        return (total_killed, most_killed_mob, (most_killed_count*100)//total_killed)
    return 0

def getcrafted(json):
    if "stats" in json and "minecraft:crafted" in json["stats"]:
        json = json["stats"]["minecraft:crafted"]
        total_crafted = 0
        most_crafted_item = ""
        most_crafted_count = 0
        for item, count in json.items():
            total_crafted += count
            if count > most_crafted_count:
                most_crafted_count = count
                most_crafted_item = item
        return (total_crafted, most_crafted_item, (most_crafted_count*100)//total_crafted)
    return 0

def getstats(json):
    statistics = {}
    time = gettime(json)
    if time:
        statistics["time_played"] = time

    jump = getjump(json)
    if jump:
        statistics["jumps"] = jump

    cloche = getcloche(json)
    if cloche:
        statistics["cloche_ring"] = cloche

    miner = getminer(json)
    if miner:
        statistics["total_mined"] = miner[0]
        statistics["most_mined"] = miner[1]
        statistics["most_mined_percent"] = miner[2]

    mort = getmort(json)
    if mort:
        statistics["total_deaths"] = mort[0]
        statistics["most_death"] = mort[1]
        statistics["most_death_percent"] = mort[2]

    distance = getdistance(json)
    if distance:
        statistics["distance_travelled"] = distance

    broke = getbroke(json)
    if broke:
        statistics["total_broken"] = broke

    killed = getkilled(json)
    if killed:
        statistics["total_killed"] = killed[0]
        statistics["most_killed"] = killed[1]
        statistics["most_killed_percent"] = killed[2]

    crafted = getcrafted(json)
    if crafted:
        statistics["total_crafted"] = crafted[0]
        statistics["most_crafted"] = crafted[1]
        statistics["most_crafted_percent"] = crafted[2]

    return statistics

def gettimeld(dicstats):
    return [(player, gettime(stats)) for player, stats in sorted(dicstats.items(), key=lambda x: gettime(x[1]), reverse=True)]

def getjumpld(dicstats):
    return [(player, getjump(stats)) for player, stats in sorted(dicstats.items(), key=lambda x: getjump(x[1]), reverse=True)]

def getclocheld(dicstats):
    return [(player, getcloche(stats)) for player, stats in sorted(dicstats.items(), key=lambda x: getcloche(x[1]), reverse=True)]

def getbrokeld(dicstats):
    return [(player, getbroke(stats)) for player, stats in sorted(dicstats.items(), key=lambda x: getbroke(x[1]), reverse=True)]

def getdistanceld(dicstats):
    return [(player, getdistance(stats)) for player, stats in sorted(dicstats.items(), key=lambda x: getdistance(x[1]), reverse=True)]

def getminerld(dicstats):
    return [(player, getminer(stats)[0]) for player, stats in sorted(dicstats.items(), key=lambda x: getminer(x[1])[0], reverse=True)]

def getmortld(dicstats):
    return [(player, getmort(stats)[0]) for player, stats in sorted(dicstats.items(), key=lambda x: getmort(x[1])[0], reverse=True)]

def getkilledld(dicstats):
    return [(player, getkilled(stats)[0]) for player, stats in sorted(dicstats.items(), key=lambda x: getkilled(x[1])[0], reverse=True)]

def getcraftedld(dicstats):
    return [(player, getcrafted(stats)[0]) for player, stats in sorted(dicstats.items(), key=lambda x: getcrafted(x[1])[0], reverse=True)]

