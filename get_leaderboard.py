# Importing required libraries
import pandas as pd 
import requests
import json

# Reading API Key from text file
params_filename = 'params.txt'
key_d = {k:str(v) for k, v in (l.split('=') for l in open(params_filename))}
API_KEY = key_d['APIKEY']
# print(API_KEY)

# RIOT url for Val/Contents
region = 'ap' # LATAM, AP, NA, KR, BR, EU
act_id = '22d10d66-4d2a-a340-6c54-408c7bd53807' # Get from Contents API
URL = f'https://{region}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{act_id}'  + '?size=200&startIndex=0'   # size -> response size (Default 200) startIndex -> Offset point (Default 0)

# Requests Header
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": API_KEY
}

# Submitting get request to pull data from RIOT database
res = requests.get(URL, headers=header)
# print(res)
response_status = res.status_code

# Converting JSON reponse into Dict object
dic_res = json.loads(res.content)

# Getting the list of attributes from response
print(dic_res.keys())

# Fetching content based on attribute
act_ID = dic_res['actId']                                       # Queried Act ID
df_players = pd.DataFrame(dic_res['players'])                   # Ranked Leaderboard
total_players = dic_res['totalPlayers']                         # The total number of players in the Ranked Leaderboard
start_index = dic_res['startIndex']                             # Start point of Leaderboard (Default: 0)
immortal_start_page = dic_res['immortalStartingPage']           # Start page of Immortal Rank in Ranked Leaderboard
immortal_start_index = dic_res['immortalStartingIndex']         # Start index of Immortal in Ranked Leaderboard
radiant_rank_threshold = dic_res['topTierRRThreshold']          # Top Tier(Radiant) RR Threshold (RR above which players are Radiant) 
df_tierDetails = pd.DataFrame(dic_res['tierDetails'])           # Ranked Tier details (Radiant, Immortal 3,2 & 1)
query = dic_res['query']                                        # Null for now
lb_region = dic_res['shard']                                    # Region of the Ranked Leaderboard

print(total_players)
print(dic_res['shard'])