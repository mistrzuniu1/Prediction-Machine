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

def main():
    full_training_data=[]
    number_of_season_for_traning=5
    for i in range(number_of_season_for_traning):
        training_data=Helper.getStatistics(i)
        training_data.Date = training_data.Date.apply(Helper.parse_date)
        training_data = Helper.get_important_columns(training_data)
        training_data = GoalCalculation.get_goals(training_data)
        training_data = PointsCalculation.get_agg_points(training_data)
        training_data = FormCalculation.add_form(training_data, 2)
        training_data = FormCalculation.add_form(training_data, 3)
        training_data = FormCalculation.add_form(training_data, 4)
        training_data = GoalCalculation.add_goal_diff(training_data)
        training_data = PointsCalculation.add_points_diff(training_data)
        training_data = Helper.get_mw(training_data)
        full_training_data.append(training_data)
    full_training_data=pd.concat([full_training_data[0],
               full_training_data[1],
               full_training_data[2],
               full_training_data[3],
               full_training_data[4]], ignore_index=True)
    full_training_data.to_csv("data/final.csv")
    pass

if __name__ == "__main__":
    main()