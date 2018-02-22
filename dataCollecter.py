import pandas as pd
from dataCleaner import dataCleaner
class dataCollecter:

    def __init__(self, league, number_of_season):
        self.__data=None
        self.__league=league
        self.__number_of_season=number_of_season

    def getData(self):
        actual_season_data = self.__prepareActualSeasonData()
        archivial_data = self.__getArchivialData()
        full_training_data = pd.concat([archivial_data,
                                        actual_season_data],
                                       ignore_index=True)
        full_training_data.to_csv("data/final" + "D1" + ".csv")
        print("Data Prepering done.")

    def __getArchivialData(self):
        full_training_data = []
        for i in range(self.__number_of_season):
            training_data = self.__getStatistics(i)
            training_data = self.__dataCleaner.format_data(training_data)
            full_training_data.append(training_data)
        #TODO:lp
        full_training_data = pd.concat([full_training_data[0],
                                        full_training_data[1],
                                        full_training_data[2],
                                        full_training_data[3],
                                        full_training_data[4]], ignore_index=True)
        return full_training_data

    def __prepareActualSeasonData(self):
        self.__data = self.__getStatistics()
        self.__data = self.__data.fillna(0)
        fixtures = self.__getFixtures()
        self.__data = pd.concat([self.__data, fixtures],
                                  ignore_index=True)
        self.__dataCleaner=dataCleaner(self.__data)
        actual_season = self.__dataCleaner.format_data(self.__data)
        return actual_season

    def __getStatistics(self, seasonNumber=-1):
        # if season is -1, it means actual
        if (seasonNumber == -1):
            source = "data/" + self.__league + "_current.csv"
        else:
            source = "data/" + self.__league + "_" + str(seasonNumber) + ".csv"
        traning_data = pd.read_csv(source)
        return traning_data

    def __getFixtures(self):
        source = "data/fixtures.csv"
        fixtures = pd.read_csv(source)
        properLeagueFixtures = fixtures.loc[(fixtures["Div"] == self.__league)]
        return properLeagueFixtures