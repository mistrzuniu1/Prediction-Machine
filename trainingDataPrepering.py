import numpy as np
import pandas as pd
import itertools
from IPython.display import display
import numpy
import Helper
import GoalCalculation
import PointsCalculation
import FormCalculation
from datetime import datetime as dt

def getArchivialData(league, number_of_season):
    full_training_data = []
    for i in range(number_of_season):
        training_data = Helper.getStatistics(league,i)
        training_data=format_data(training_data)
        full_training_data.append(training_data)
    full_training_data = pd.concat([full_training_data[0],
                                    full_training_data[1],
                                    full_training_data[2],
                                    full_training_data[3],
                                    full_training_data[4]], ignore_index=True)
    return full_training_data

def format_data(data):
    data.Date = data.Date.apply(Helper.parse_date)
    data = Helper.get_important_columns(data)
    data = Helper.get_mw(data)
    round_number=max(data['MW'])
    data = GoalCalculation.get_goals(data,round_number)
    data = PointsCalculation.get_agg_points(data,round_number)
    data = FormCalculation.add_form(data, 2,round_number)
    data = FormCalculation.add_form(data, 3,round_number)
    data = FormCalculation.add_form(data, 4,round_number)
    data = GoalCalculation.add_goal_diff(data)
    data = PointsCalculation.add_points_diff(data)
    return data


def prepareActualSeasonData(league):
    actual_season_data=Helper.getStatistics("D1")
    actual_season_data=actual_season_data.fillna(0)
    fixtures=Helper.getFixtures("D1")
    fixtures=fixtures
    actual_season = pd.concat([actual_season_data,fixtures],
                                   ignore_index=True)
    actual_season=format_data(actual_season)
    return actual_season

def main():
    number_of_season_for_traning=5
    actual_season_data = prepareActualSeasonData("D1")
    archivial_data = getArchivialData("D1", number_of_season_for_traning)
    full_training_data = pd.concat([archivial_data,
                                    actual_season_data],
                              ignore_index=True)
    full_training_data.to_csv("data/final"+"D1"+".csv")
    print("Data Prepering done.")
    pass

if __name__ == "__main__":
    main()