import Helper
import pandas as pd

def get_cuml_points(matchres,round_number=0):
    matchres_points = matchres.applymap(Helper.convert_FTR_to_points)
    matchres_points[1] = matchres_points[0]
    matchres_points[0]=0
    if (round_number == 0):
        round_number = len(matchres_points.columns)

    for i in range(2, round_number):
        matchres_points[i] = matchres_points[i] + matchres_points[i - 1]
    return matchres_points


def get_form(playing_stat, matchweek,round_number=0):
    form = get_team_form(playing_stat)
    form_final = form.copy()

    #if round_number equals 0 then season is complete.
    if (round_number == 0):
        round_number = (Helper.count_teams(playing_stat) * 2) - 2

    for i in range(matchweek, round_number):
        form_final[i] = ''
        j = 0
        while j < matchweek:
            form_final[i] += form[i - j]
            j += 1
    return form_final

def get_team_form(playing_stat,round_number=0):
    teams = {}
    for i in playing_stat.groupby('HomeTeam').mean().T.columns:
        teams[i] = []

    for i in range(len(playing_stat)):
        if playing_stat.iloc[i].FTR == 'H':
            teams[playing_stat.iloc[i].HomeTeam].append('W')
            teams[playing_stat.iloc[i].AwayTeam].append('L')
        elif playing_stat.iloc[i].FTR == 'A':
            teams[playing_stat.iloc[i].AwayTeam].append('W')
            teams[playing_stat.iloc[i].HomeTeam].append('L')
        else:
            teams[playing_stat.iloc[i].AwayTeam].append('D')
            teams[playing_stat.iloc[i].HomeTeam].append('D')

    # if round_number equals 0 then season is complete.
    if (round_number == 0):
        round_number = (Helper.count_teams(playing_stat) * 2) - 2

    return pd.DataFrame(data=teams, index=[i for i in range(0, round_number)]).T

def add_points_diff(playing_statistics_1):
    playing_statistics_1['DiffPts'] = playing_statistics_1['HomeTeamPoints'] - playing_statistics_1['AwayTeamPoints']
    return playing_statistics_1

def get_agg_points(playing_stat):
    matchres = get_team_form(playing_stat)
    cum_pts = get_cuml_points(matchres)

    HomeTeamPoints = []
    AwayTeamPoints = []
    j = 0
    for i in range(len(playing_stat)):
        ht = playing_stat.iloc[i].HomeTeam
        at = playing_stat.iloc[i].AwayTeam
        HomeTeamPoints.append(cum_pts.loc[ht][j])
        AwayTeamPoints.append(cum_pts.loc[at][j])

        if ((i + 1) % (len(matchres)/2)) == 0:
            j = j + 1

    playing_stat['HomeTeamPoints'] = HomeTeamPoints
    playing_stat['AwayTeamPoints'] = AwayTeamPoints
    return playing_stat

