import pandas as pd
class FormCalculator:

    def __init__(self, data, round_number,numOfTeams):
        self.__data=data
        self.__numOfMatches=len(self.__data)
        self.__numOfTeams=numOfTeams
        if(round_number!=0):
            self.__round_number = round_number
        else:
            self.__round_number = (self.__numOfTeams * 2) - 2

    def addLast3MatchesForm(self):
        for i in range (2,5):
            self.__add_form(i)
        return self.__data

    def __get_form(self,matchweek):
        form = self.__getTeamForm()
        form_final = form.copy()

        for i in range(matchweek, self.__round_number):
            form_final[i] = ''
            j = 0
            while j < matchweek:
                form_final[i] += form[i - j]
                j += 1
        return form_final

    def __add_form(self,lastMatch):
        form = self.__get_form(lastMatch)
        h = ['M' for i in range(
            int(lastMatch * self.__numOfTeams/ 2))]  # since form is not available for n MW (n*10)
        a = ['M' for i in range(int(lastMatch * self.__numOfTeams / 2))]

        j = lastMatch

        for i in range(int(lastMatch * (self.__numOfTeams / 2)), self.__numOfMatches):
            ht = self.__data.iloc[i].HomeTeam
            at = self.__data.iloc[i].AwayTeam

            past = form.loc[ht][j]
            h.append(past[lastMatch - 1])

            past = form.loc[at][j]
            a.append(past[lastMatch - 1])

            if ((i + 1) % (self.__numOfTeams / 2)) == 0:
                j = j + 1

        lastMatch -= 1
        self.__data['HM' + str(lastMatch)] = h
        self.__data['AM' + str(lastMatch)] = a

    #TODO: Delete it!
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
        return pd.DataFrame(data=teams, index=[i for i in range(0, self.__round_number)]).T