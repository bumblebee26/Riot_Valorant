# Importing required libraries
import pandas as pd 
import requests
import json
from exception_handling import get_response

# Reading API Key from text file
params_filename = 'params.txt'
key_d = {k:str(v) for k, v in (l.split('=') for l in open(params_filename))}
API_KEY = key_d['APIKEY']
# print(API_KEY)

# RIOT url for Val/Contents
region = 'ap' # LATAM, AP, NA, KR, BR, EU
URL = f'https://{region}.api.riotgames.com/val/content/v1/contents?locale=en-US'

# Requests Header
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": API_KEY
}

# Submitting get request to pull data from RIOT database
res = get_response('GET', URL, header)

# Converting JSON reponse into Dict object
dic_res = json.loads(res)

# Getting the list of attributes from response
print(dic_res.keys())

# Fetching content based on attribute
game_version = dic_res['version']                                   # Game Version
df_characters = pd.DataFrame(dic_res['characters'])                 # Characters
df_maps = pd.DataFrame(dic_res['maps'])                             # Maps
df_chromas = pd.DataFrame(dic_res['chromas'])                       # Weapon Skins with Variants
df_skins = pd.DataFrame(dic_res['skins'])                           # Weapon Skins
df_skinLevels = pd.DataFrame(dic_res['skinLevels'])                 # Weapon Skins with Upgrade Level
df_equips = pd.DataFrame(dic_res['equips'])                         # Weapons and Equipments
df_gameModes = pd.DataFrame(dic_res['gameModes'])                   # Game Modes
df_totems = pd.DataFrame(dic_res['totems'])                         # totems - Null for now
df_sprays = pd.DataFrame(dic_res['sprays'])                         # Sprays
df_sprayLevels = pd.DataFrame(dic_res['sprayLevels'])               # Sprays with levels - Didn't find any difference except id and assetName
df_charms = pd.DataFrame(dic_res['charms'])                         # Gun Buddy
df_charmLevels = pd.DataFrame(dic_res['charmLevels'])               # Gun Buddy with levels - Didn't find any difference except id and assetName
df_playerCards = pd.DataFrame(dic_res['playerCards'])               # Player Cards
df_playerTitles = pd.DataFrame(dic_res['playerTitles'])             # Player Title
df_acts = pd.DataFrame(dic_res['acts'])                             # Acts
df_ceremonies = pd.DataFrame(dic_res['ceremonies'])                 # Ceremonies // Round end Banner

# print(df_ceremonies)

# print(df_chromas[df_chromas['name'].str.lower().str.contains("prime")])
# print(df_skins[df_skins['name'].str.lower().str.contains("prime")])
# print(df_skinLevels[df_skinLevels['name'].str.lower().str.contains("prime")])
# print(df_charmLevels[df_charmLevels['name'].str.lower().str.contains("fist")])

    
