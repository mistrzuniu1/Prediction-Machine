import pandas as pd
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import scale
from sklearn.cross_validation import train_test_split
from IPython.display import display
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import numpy as np


class FeatureTargetManager:

    def __init__(self, league):
        self.__league=league
        self.__X_all=None
        self.__y_all=None
        self.__data=None
        self.__numberOfUpcoming = None
    def getFeatureToPredictUpcoming(self):
        self.__X_all=pd.read_csv("data/"+self.__league+"/TrainingData/final"+self.__league+".csv", index_col=0)
        self.__numberOfUpcoming= self.__X_all['FTR'].isnull().sum()
        if(self.__X_all is None):
            print("First of all save the data from actual season!")
            return None
        self.__X_all = self.__X_all.drop(
            ['Date', 'FTR', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'HomeTeamScored', 'AwayTeamScored',
             'HomeTeamConceded',
             'AwayTeamConceded', 'HomeGoalDiff', 'AwayGoalDiff', 'HomeTeamPoints', 'AwayTeamPoints'], 1)
        self.__preprocessFeatures()
        self.__X_all =  self.__X_all[-(self.__numberOfUpcoming):]
        return self.__X_all

    def getFeatureAndTarget(self):
        self.__SeperateFeatureTarget()
        self.__preprocessFeatures()
        return self.__X_all[: len(self.__X_all) - self.__numberOfUpcoming], self.__y_all[: len(self.__y_all) - self.__numberOfUpcoming]

    def __SeperateFeatureTarget(self):
        self.__data= pd.read_csv("data/"+self.__league+"/TrainingData/final"+self.__league+".csv", index_col=0)
        self.__numberOfUpcoming = self.__data['FTR'].isnull().sum()
        self.__data = self.__data[: (len(self.__data) - self.__numberOfUpcoming)]
        self.__X_all = self.__data.drop(
            ['Date', 'FTR', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'HomeTeamScored', 'AwayTeamScored',
             'HomeTeamConceded','AwayTeamConceded', 'HomeGoalDiff', 'AwayGoalDiff', 'HomeTeamPoints', 'AwayTeamPoints'], 1)
        self.__y_all = self.__data['FTR']

    def __preprocessFeatures(self,features=None):
        output = pd.DataFrame(index=self.__X_all.index)
        for col, col_data in self.__X_all.iteritems():
            if col_data.dtype == object:
                col_data = pd.get_dummies(col_data, prefix=col)
            output = output.join(col_data)

        self.__X_all = output
        cols = [['DiffInGoals', 'DiffPts']]
        for col in cols:
            self.__X_all[col] = scale(self.__X_all[col])
