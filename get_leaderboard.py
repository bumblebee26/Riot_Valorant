# Importing required libraries
import pandas as pd 
from exception_handling import get_response
import json

# Reading API Key from text file
params_filename = 'params.txt'
key_d = {k:str(v) for k, v in (l.split('=') for l in open(params_filename))}
API_KEY = key_d['APIKEY']
act_id = '22d10d66-4d2a-a340-6c54-408c7bd53807' # Get from Contents API
# print(API_KEY)

# Requests Header
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": API_KEY
}

def get_region_meta(region, act_id):
    # RIOT url for Val/Contents
    # region = 'eu' # LATAM, AP, NA, KR, BR, EU
    URL = f'https://{region}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{act_id}'  + '?size=200&startIndex=0'   # size -> response size (Default 200) startIndex -> Offset point (Default 0)

    # Submitting get request to pull data from RIOT database
    res = get_response('GET', URL, header)

    # Converting JSON reponse into Dict object
    dic_res = json.loads(res)

    # Getting the list of attributes from response
    # print(dic_res.keys())

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

    print(f'Total players in {region.upper()} leaderboard: {total_players}')
    payload = {}
    payload['act_ID'] = act_ID
    payload['df_players'] = df_players
    payload['total_players'] = total_players
    payload['start_index'] = start_index
    payload['immortal_start_page'] = immortal_start_page
    payload['immortal_start_index'] = immortal_start_index
    payload['radiant_rank_threshold'] = radiant_rank_threshold
    payload['df_tierDetails'] = df_tierDetails
    payload['query'] = query
    payload['lb_region'] = lb_region
    
    return payload

# Function to return full ranked leaderboard
def get_full_leaderboard(region, act_ID, total_players):
    size = 200
    offset = 0
    if total_players%size:
        no_of_pages = (total_players//size)+1
    else:
        no_of_pages = (total_players//size)
    df_full_players_lb = []
    # print(no_of_pages)
    while no_of_pages:
        rep_URL = f'https://{region}.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{act_ID}'  + f'?size={size}&startIndex={offset}'   # size -> response size (Default 200) startIndex -> Offset point (Default 0)
        offset += size
        res = get_response('GET', rep_URL, header)
        dic_res = json.loads(res)
        df_full_players_lb.append(pd.DataFrame(dic_res['players']))
        print(no_of_pages)
        no_of_pages-=1
    return pd.concat(df_full_players_lb)

def load_leaderboard_all_region():
    regions_list = 'LATAM,AP,NA,KR,BR,EU'.lower().split(',')
    for region in regions_list:
        print(f'{str(region).upper()} Leaderboard loading....\n\n')
        region_meta = get_region_meta(region, act_id)
        df = get_full_leaderboard(region=region, act_ID=act_id, total_players=region_meta['total_players'])
        df.to_csv(f'Ranked Leaderboard/{region}_ranked_leaderboard.csv', index = False)

load_leaderboard_all_region()