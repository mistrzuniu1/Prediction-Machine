from datetime import datetime as dt
import pandas as pd
import Helper
import numpy as np
def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%d/%m/%y').date()

def get_important_columns(dataframe):
    columns_req = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
    playing_stat = dataframe[columns_req]
    return playing_stat

def count_teams(playing_stat):
    return len(playing_stat.groupby('HomeTeam').mean().T.columns)

def convert_FTR_to_points(result):
    if result == 'W':
        return 3
    elif result == 'D':
        return 1
    else:
        return 0

def get_mw(playing_stat):
    j = 1
    MatchWeek = []
    for i in range(len(playing_stat)):
        MatchWeek.append(j)
        if ((i + 1)%(Helper.count_teams(playing_stat)/2)) == 0:
            j = j + 1
    playing_stat['MW'] = MatchWeek
    return playing_stat

def getStatistics(league,number_of_season=-1):
    #if season is -1, it means actual
    if(number_of_season==-1):
        source = "data/"+league+"_current.csv"
    else:
        source="data/"+league+"_"+str(number_of_season)+".csv"
    traning_data=pd.read_csv(source)
    return traning_data

def getFixtures(league):
    source="data/fixtures.csv"
    fixtures=pd.read_csv(source)
    properLeagueFixtures=fixtures.loc[(fixtures["Div"]==league)]
    return properLeagueFixtures
