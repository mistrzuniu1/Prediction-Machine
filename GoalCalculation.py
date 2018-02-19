import pandas as pd
import Helper

def get_goals(playing_stat,round_number=0):
    GoalsConceded = get_goals_conceded(playing_stat,round_number)
    GoalsScored = get_goals_scored(playing_stat,round_number)

    j = 0
    HomeTeamScored = []
    AwayTeamScored = []
    HomeTeamConceded = []
    AwayTeamConceded = []

    for i in range(len(playing_stat)):
        ht = playing_stat.iloc[i].HomeTeam
        at = playing_stat.iloc[i].AwayTeam
        HomeTeamScored.append(GoalsScored.loc[ht][j])
        AwayTeamScored.append(GoalsScored.loc[at][j])
        HomeTeamConceded.append(GoalsConceded.loc[ht][j])
        AwayTeamConceded.append(GoalsConceded.loc[at][j])

        if ((i + 1) % (len(GoalsConceded)/2)) == 0:
            j = j + 1

    playing_stat['HomeTeamScored'] = HomeTeamScored
    playing_stat['AwayTeamScored'] = AwayTeamScored
    playing_stat['HomeTeamConceded'] = HomeTeamConceded
    playing_stat['AwayTeamConceded'] = AwayTeamConceded
    return playing_stat

def get_goals_scored(traning_data,round_number=0):
    # Create a dictionary with team names as keys
    teams = {}
    for i in traning_data.groupby('HomeTeam').mean().T.columns:
        teams[i] = []

    for i in range(len(traning_data)):
        HomeTeamScored = traning_data.iloc[i]['FTHG']
        AwayTeamScored = traning_data.iloc[i]['FTAG']
        teams[traning_data.iloc[i].HomeTeam].append(HomeTeamScored)
        teams[traning_data.iloc[i].AwayTeam].append(AwayTeamScored)

    if(round_number==0):
        round_number=(Helper.count_teams(traning_data)*2)-2
    # Create a dataframe for goals scored where rows are teams and cols are matchweek.
    GoalsScored = pd.DataFrame(data=teams, index=[i for i in range(0, round_number)]).T
    # Aggregate to get uptil that point
    last_match_goals=GoalsScored[1].copy()
    GoalsScored[1]=GoalsScored[0]
    GoalsScored[0]=0

    for i in range(2, round_number):
        next_match_goals=GoalsScored[i].copy()
        GoalsScored[i] =last_match_goals + GoalsScored[i - 1]
        last_match_goals = next_match_goals.copy()
    return GoalsScored


def get_goals_conceded(traning_data,round_number=0):
    teams = {}
    for i in traning_data.groupby('HomeTeam').mean().T.columns:
        teams[i] = []

    for i in range(len(traning_data)):
        AwayTeamConceded = traning_data.iloc[i]['FTHG']
        HomeTeamConceded = traning_data.iloc[i]['FTAG']
        teams[traning_data.iloc[i].HomeTeam].append(HomeTeamConceded)
        teams[traning_data.iloc[i].AwayTeam].append(AwayTeamConceded)

    if (round_number == 0):
        round_number = (Helper.count_teams(traning_data) * 2) - 2

    GoalsConceded = pd.DataFrame(data=teams, index=[i for i in range(0, round_number)]).T
    last_match_goals = GoalsConceded[1].copy()
    GoalsConceded[1] = GoalsConceded[0]
    GoalsConceded[0] = 0
    for i in range(2, round_number):
        next_match_goals = GoalsConceded[i].copy()
        GoalsConceded[i] = last_match_goals + GoalsConceded[i - 1]
        last_match_goals = next_match_goals.copy()
    return GoalsConceded

def add_goal_diff(playing_statistics_1):
    playing_statistics_1['HomeGoalDiff'] = playing_statistics_1['HomeTeamScored'] - playing_statistics_1['HomeTeamConceded']
    playing_statistics_1['AwayGoalDiff'] = playing_statistics_1['AwayTeamScored'] - playing_statistics_1['AwayTeamConceded']
    playing_statistics_1['DiffInGoals'] = playing_statistics_1['HomeGoalDiff'] - playing_statistics_1['AwayGoalDiff']
    return playing_statistics_1
