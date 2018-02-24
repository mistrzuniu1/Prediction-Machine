import pandas as pd

class PointsCalculator:

    def __init__(self, data, round_number,numOfTeams):
        self.__data=data
        self.__numOfMatches = len(self.__data)
        self.__numOfTeams = numOfTeams
        if (round_number != 0):
            self.__round_number = round_number
        else:
            self.__round_number = (self.__numOfTeams * 2) - 2

    def calculatePoints(self):
        self.__getPoints()
        self.__add_points_diff()
        return self.__data

    def __getCumulatedPoints(self, matches):
        matches_points = matches.applymap(self.FTRtoPoints)

        last_match_goals = matches_points[1].copy()
        matches_points[1] = matches_points[0]
        matches_points[0] = 0

        for i in range(2, self.__round_number):
            next_match_goals = matches_points[i].copy()
            matches_points[i] = last_match_goals + matches_points[i - 1]
            last_match_goals = next_match_goals.copy()
        return matches_points

    def __getTeamForm(self):
        teams = {}
        for i in self.__data.groupby('HomeTeam').mean().T.columns:
            teams[i] = []

        for i in range(self.__numOfMatches):
            if self.__data.iloc[i].FTR == 'H':
                teams[self.__data.iloc[i].HomeTeam].append('W')
                teams[self.__data.iloc[i].AwayTeam].append('L')
            elif self.__data.iloc[i].FTR == 'A':
                teams[self.__data.iloc[i].AwayTeam].append('W')
                teams[self.__data.iloc[i].HomeTeam].append('L')
            else:
                teams[self.__data.iloc[i].AwayTeam].append('D')
                teams[self.__data.iloc[i].HomeTeam].append('D')

        # if round_number equals 0 then season is complete.
        for i in teams:
            while(len(teams[i])<self.__round_number):
                teams[i].append('D')

        return pd.DataFrame(data=teams, index=[i for i in range(0, self.__round_number)]).T

    def __add_points_diff(self):
        self.__data['DiffPts'] = self.__data['HomeTeamPoints'] - \
                                 self.__data['AwayTeamPoints']

    def __getPoints(self):
        matches = self.__getTeamForm()
        cum_pts = self.__getCumulatedPoints(matches)


        HomeTeamPoints = []
        AwayTeamPoints = []
        j = 0
        for i in range(self.__numOfMatches):
            ht = self.__data.iloc[i].HomeTeam
            at = self.__data.iloc[i].AwayTeam
            HomeTeamPoints.append(cum_pts.loc[ht][j])
            AwayTeamPoints.append(cum_pts.loc[at][j])

            if ((i + 1) % (self.__numOfTeams / 2)) == 0:
                j = j + 1

        self.__data['HomeTeamPoints'] = HomeTeamPoints
        self.__data['AwayTeamPoints'] = AwayTeamPoints

    def FTRtoPoints(self, result):
        if result == 'W':
            return 3
        elif result == 'D':
            return 1
        else:
            return 0



