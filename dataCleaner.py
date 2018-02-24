from datetime import datetime as dt
from GoalCalculator import GoalCalculator
from PointsCalculator import PointsCalculator
from FormCalculator import FormCalculator
import Helper

import csv
class dataCleaner:
    def __init__(self,data):
        self.__data=None
        self.__numOfTeams=self.__count_teams()

    def format_data(self,data):
        self.__data=data
        self.__numOfTeams = self.__count_teams()
        self.__data.Date.apply(Helper.parse_date)
        self.__get_important_columns()
        self.__get_mw()
        round_number=max(self.__data['MW'])
        goalCalculator=GoalCalculator(self.__data, round_number,self.__numOfTeams)
        self.__data=goalCalculator.calculateGoals()
        pointsCalculator=PointsCalculator(self.__data,round_number,self.__numOfTeams)
        self.__data=pointsCalculator.calculatePoints()
        formCalculator=FormCalculator(self.__data,round_number,self.__numOfTeams)
        self.__data=formCalculator.addLast3MatchesForm()
        return self.__data


    def __get_important_columns(self):
        columns_req = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
        self.__data = self.__data[columns_req]

    def __get_mw(self):
        j = 1
        MatchWeek = []
        for i in range(len(self.__data)):
            MatchWeek.append(j)
            if ((i + 1)%(self.__numOfTeams/ 2)) == 0:
                j = j + 1
        self.__data['MW'] = MatchWeek

    def __count_teams(self):
        if(self.__data is None):
            return 0
        else:
            return len(self.__data.groupby('HomeTeam').mean().T.columns)
