import pandas as pd

class GoalCalculator:

    def __init__(self, data, round_number,numOfTeams):
        self.__data=data
        self.__numOfMatches=len(self.__data)
        self.__numOfTeams=numOfTeams
        if(round_number!=0):
            self.__round_number = round_number
        else:
            self.__round_number = (self.__numOfTeams * 2) - 2

    def calculateGoals(self):
        self.__getGoals()
        self.__addGoalDiff()
        return self.__data

    def __getGoals(self):
        GoalsConceded = self.__getConceded()
        GoalsScored = self.__getScored()

        j = 0
        HomeTeamScored = []
        AwayTeamScored = []
        HomeTeamConceded = []
        AwayTeamConceded = []

        for i in range(self.__numOfMatches):
            ht = self.__data.iloc[i].HomeTeam
            at = self.__data.iloc[i].AwayTeam
            HomeTeamScored.append(GoalsScored.loc[ht][j])
            AwayTeamScored.append(GoalsScored.loc[at][j])
            HomeTeamConceded.append(GoalsConceded.loc[ht][j])
            AwayTeamConceded.append(GoalsConceded.loc[at][j])

            if ((i + 1) % (self.__numOfTeams / 2)) == 0:
                j = j + 1

        self.__data['HomeTeamScored'] = HomeTeamScored
        self.__data['AwayTeamScored'] = AwayTeamScored
        self.__data['HomeTeamConceded'] = HomeTeamConceded
        self.__data['AwayTeamConceded'] = AwayTeamConceded

    def __getScored(self):
        # Create a dictionary with team names as keys
        teams = {}
        for i in self.__data.groupby('HomeTeam').mean().T.columns:
            teams[i] = []

        for i in range(self.__numOfMatches):
            HomeTeamScored = self.__data.iloc[i]['FTHG']
            AwayTeamScored = self.__data.iloc[i]['FTAG']
            teams[self.__data.iloc[i].HomeTeam].append(HomeTeamScored)
            teams[self.__data.iloc[i].AwayTeam].append(AwayTeamScored)

        # Create a dataframe for goals scored where rows are teams and cols are matchweek.
        GoalsScored = pd.DataFrame(data=teams, index=[i for i in range(0, self.__round_number)]).T
        # Aggregate to get uptil that point
        last_match_goals = GoalsScored[1].copy()
        GoalsScored[1] = GoalsScored[0]
        GoalsScored[0] = 0

        for i in range(2, self.__round_number):
            next_match_goals = GoalsScored[i].copy()
            GoalsScored[i] = last_match_goals + GoalsScored[i - 1]
            last_match_goals = next_match_goals.copy()
        return GoalsScored

    def __getConceded(self):
        teams = {}
        for i in self.__data.groupby('HomeTeam').mean().T.columns:
            teams[i] = []

        for i in range(len(self.__data)):
            AwayTeamConceded = self.__data.iloc[i]['FTHG']
            HomeTeamConceded = self.__data.iloc[i]['FTAG']
            teams[self.__data.iloc[i].HomeTeam].append(HomeTeamConceded)
            teams[self.__data.iloc[i].AwayTeam].append(AwayTeamConceded)

        GoalsConceded = pd.DataFrame(data=teams, index=[i for i in range(0, self.__round_number)]).T
        last_match_goals = GoalsConceded[1].copy()
        GoalsConceded[1] = GoalsConceded[0]
        GoalsConceded[0] = 0
        for i in range(2, self.__round_number):
            next_match_goals = GoalsConceded[i].copy()
            GoalsConceded[i] = last_match_goals + GoalsConceded[i - 1]
            last_match_goals = next_match_goals.copy()
        return GoalsConceded
        return GoalsConceded

    def __addGoalDiff(self):
        self.__data['HomeGoalDiff'] = self.__data['HomeTeamScored'] - self.__data[
            'HomeTeamConceded']
        self.__data['AwayGoalDiff'] = self.__data['AwayTeamScored'] - self.__data[
            'AwayTeamConceded']
        self.__data['DiffInGoals'] = self.__data['HomeGoalDiff'] - self.__data[
            'AwayGoalDiff']
