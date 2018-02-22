from datetime import datetime as dt
import pandas as pd

def parse_date(date):
    if date == '':
        return None
    else:
        return dt.strptime(date, '%d/%m/%y').date()

def getTeamsForUpcoming():
    dataframe = pd.read_csv("data/finalD1.csv", index_col=0)
    teams = dataframe[['HomeTeam', 'AwayTeam']]
    teams = teams[-9:]
    teams = teams.reset_index()
    return teams