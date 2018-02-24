from datetime import datetime as dt
import pandas as pd

def parse_date(date):
    if date == '':
        return None
    if isinstance(date,float):
        return None
    else:
        return dt.strptime(date, '%d/%m/%y').date()


def getTeamsForUpcoming(league):
    dataframe = pd.read_csv("data/"+league+"/TrainingData/final"+league+".csv", index_col=0)
    numberOfUpcoming = dataframe['FTR'].isnull().sum()
    teams = dataframe[['HomeTeam', 'AwayTeam']]
    teams = teams[-numberOfUpcoming:]
    teams = teams.reset_index()
    return teams

def getMatchweekForUpcoming(league):
    dataframe = pd.read_csv("data/" + league + "/TrainingData/"+ league + "_current.csv", index_col=0)
    matchweek=max(dataframe['MW'])
    return matchweek