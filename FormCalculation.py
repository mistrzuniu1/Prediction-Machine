import PointsCalculation
import Helper

def add_form(playing_stat, matchweek, round_number):
    form = PointsCalculation.get_form(playing_stat, matchweek, round_number)
    h = ['M' for i in range (int(matchweek * Helper.count_teams(playing_stat)/2))]  # since form is not available for n MW (n*10)
    a = ['M' for i in range (int(matchweek * Helper.count_teams(playing_stat)/2))]

    j=matchweek

    number_of_teams=Helper.count_teams(playing_stat)
    number_of_matches=len(playing_stat)

    for i in range(int(matchweek*(number_of_teams/2)), number_of_matches):
        ht = playing_stat.iloc[i].HomeTeam
        at = playing_stat.iloc[i].AwayTeam

        past = form.loc[ht][j]
        h.append(past[matchweek-1])

        past = form.loc[at][j]
        a.append(past[matchweek-1])

        if ((i + 1) % (number_of_teams/2)) == 0:
            j = j + 1

    matchweek-=1
    playing_stat['HM' + str(matchweek)] = h
    playing_stat['AM' + str(matchweek)] = a
    return playing_stat
