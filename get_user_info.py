from exception_handling import get_response
import json
import os

# Reading API Key from text file
# params_filename = 'params.txt'
# key_d = {k:str(v) for k, v in (l.split('=') for l in open(params_filename))}
# API_KEY = key_d['APIKEY']
API_KEY = str(os.environ.get('APIKEY'))
# act_id = '22d10d66-4d2a-a340-6c54-408c7bd53807' # Get from Contents API
# print(API_KEY)
region_list = str(os.environ.get('acc_region')).lower().split(',')

# Requests Header
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": API_KEY
}

# Function to get user's puuid from gameName and tagLine
def get_puuid(gameName, tagLine, region):
    # RIOT url 
    if region.lower() in region_list:
        URL = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}'
    else:
        raise Exception('Region is not present in the existing list')

    # Submitting get request to pull data from RIOT database
    res = get_response('GET', URL, header)
    
    # Converting JSON reponse into Dict object
    dic_res = json.loads(res)
    # print(dic_res)

    # Getting the list of attributes from response
    # print(dic_res.keys())
    return dic_res['puuid']

# Function to get user's gameName and tagLine from puuid
def get_player_tag(puuid, region):
    # RIOT url 
    if region.lower() in region_list:
        URL = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}'
    else:
        raise Exception('Region is not present in the existing list')

    # Submitting get request to pull data from RIOT database
    res = get_response('GET', URL, header)
    
    # Converting JSON reponse into Dict object
    dic_res = json.loads(res)
    # print(dic_res)

    # Getting the list of attributes from response
    # print(dic_res.keys())
    res_payload = {}
    res_payload['gameName'] = dic_res['gameName']
    res_payload['tagLine'] = dic_res['tagLine']
    return res_payload

# Function to get user's active region from puuid and game
def get_player_active_region(puuid, game, region):
    # RIOT url 
    if region.lower() in region_list:
        URL = f'https://{region}.api.riotgames.com/riot/account/v1/active-shards/by-game/{game}/by-puuid/{puuid}'
    else:
        raise Exception('Region is not present in the existing list')

    # Submitting get request to pull data from RIOT database
    res = get_response('GET', URL, header)
    
    # Converting JSON reponse into Dict object
    dic_res = json.loads(res)
    # print(dic_res)

    # Getting the list of attributes from response
    # print(dic_res.keys())
    return dic_res['activeShard']

puuid = get_puuid('n4rX', 'kekw', 'ASIA')

res = get_player_tag(puuid, 'ASIA')

active_region = get_player_active_region(puuid, game='val', region='AMERICAS')
print(f'Player Account Details\nPlayer\'s Tag : {res['gameName']}#{res['tagLine']}\nPUUID : {puuid}\nPlayer account Active region : {active_region}') 