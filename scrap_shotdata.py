#Importar as bibliotecas que serão utilizadas ao longo do código
import requests as req
import pandas as pd
import time
import json
from nba_api.stats.endpoints.commonteamroster import CommonTeamRoster
from nba_api.stats.library.parameters import Season
from nba_api.stats.static import teams

#Definir as funções que serão reutilizadas ao longo do script, para evitar erros
def get_team_id():
    teams_nba = teams.get_teams()

    for team in teams_nba:
        id_team = team['id']
        fn_team = team['full_name']
        teams_dict[id_team] = fn_team

def get_season_roster(season, team_id):
    team_roster = CommonTeamRoster(season=season, team_id=team_id).get_data_frames()[0]
    return team_roster

def get_players(season, team_id):
    for index, row in get_season_roster(season, team_id).iterrows():
        fn_player = row['PLAYER']
        id_player = row['PLAYER_ID']
        players[id_player] = fn_player

teams_dict = {}
get_team_id()

#É necessário especificar os cabeçalhos para que a conexão com o site seja bem-sucedida
headers = {
    'Connection' : 'keep-alive',
    'Accept' : 'application/json, text/plain, */*',
    'x-nba-stats-token' : 'true',
    'X-NewRelic-ID' : 'VQECWF5UChAHUlNTBwgBVw==',
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
    'x-nba-stats-origin' : 'stats',
    'Sec-Fetch-Site' : 'same-origin',
    'Sec-Fetch-Mode' : 'cors',
    'Referer': 'https://stats.nba.com/players/leaguedashplayerbiostats/',
    'Accept-Encoding' : 'gzip, deflate, br',
    'Accept-Language' : 'en-US,en;q=0.9'
    }

#E uma lista com todas as temporadas visadas para coleta dos dados
seasons = ['1996-97', '1997-98', '1998-99', '1999-00', '2000-01', '2001-02', '2002-03', '2003-04',
           '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12',
           '2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20',
           '2020-21']

#A partir daqui é feito um laço de repetição para repetir o processo para todos os times em todas as temporadas
#E depois armazenar tudo em um arquivo no formato CSV
for season in seasons:
    for key, value in teams_dict.items():
        players = {}
        get_players(season, key)
        print(season, value)
        time.sleep(3)
        for key_player, value_player in players.items():
            url= f"https://stats.nba.com/stats/shotchartdetail?AheadBehind=&CFID=33&CFPARAMS={season}&ClutchTime=&Conference=&ContextFilter=&ContextMeasure=FGA&DateFrom=" \
                 f"&DateTo=&Division=&EndPeriod=10&EndRange=28800&GROUP_ID=&GameEventID=&GameID=&GameSegment=&GroupID=&GroupMode=&GroupQuantity=5&LastNGames=0&LeagueID=00&" \
                 f"Location=&Month=0&OnOff=&OpponentTeamID=0&Outcome=&PORound=0&Period=0&PlayerID={key_player}&PlayerID1=&PlayerID2=&PlayerID3=&PlayerID4=&PlayerID5=&Player" \
                 f"Position=&PointDiff=&Position=&RangeType=0&RookieYear=&Season={season}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StartPeriod=1&StartRange=" \
                 f"0&StarterBench=&TeamID=0&VsConference=&VsDivision=&VsPlayerID1=&VsPlayerID2=&VsPlayerID3=&VsPlayerID4=&VsPlayerID5=&VsTeamID="
            response = req.get(url, headers=headers)
            response.raise_for_status()  # raises exception when not a 2xx response
            if response.status_code != 204:
                r=response.json()
                df_headers = r['resultSets'][0]['headers']
                df_data = r['resultSets'][0]['rowSet']
                df = pd.DataFrame(df_data, columns=df_headers)
                df.to_csv(f'{season}_{value}_{key_player}.csv')
                print(f'{season} {value} DONE!')
                time.sleep(10)