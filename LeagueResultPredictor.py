from sklearn.metrics import f1_score

from dataCollecter import dataCollecter
from FeatureTargetManager import FeatureTargetManager

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
import Helper



class LeagueResultPredictor:

    def __init__(self, league, number_of_season):
        self.__league=league
        self.__number_of_season=number_of_season
        self.__dataCollecter = dataCollecter(league, number_of_season)
        self.__clf_A = None
        self.__clf_B = None
        self.__clf_C = None

    def prepareData(self):
        self.__dataCollecter.getData()

    def trainClassifiers(self):
        featureTargetManager=FeatureTargetManager(self.__league)

        X_all,Y_all=featureTargetManager.getFeatureAndTarget()

        X_train, X_test, y_train, y_test = train_test_split(X_all, Y_all,
                                                            test_size=100,
                                                            random_state=2,
                                                            stratify=Y_all)

        self.__clf_A = LogisticRegression(random_state=42)
        self.__clf_B = SVC(random_state=912, kernel='rbf')
        self.__clf_C = xgb.XGBClassifier(seed=82)

        self.__clf_A.fit(X_train, y_train)
        self.__clf_B.fit(X_train, y_train)
        self.__clf_C.fit(X_train, y_train)
        self.checkAccuracy(X_test,y_test)


    def checkAccuracy(self,X_test,y_test):

        y_pred = self.__clf_A.predict(X_test)
        self.__getAccuracyScore(y_test,y_pred,"Logictic Regression")
        y_pred = self.__clf_B.predict(X_test)
        self.__getAccuracyScore(y_test, y_pred,"Support Vector Classification")
        y_pred = self.__clf_C.predict(X_test)
        self.__getAccuracyScore(y_test, y_pred, "XGboost")


    def __getAccuracyScore(self,y_test,y_pred,name):
        f1 = f1_score(y_test, y_pred, pos_label='H', average='micro')
        acc = sum(y_test == y_pred) / float(len(y_pred))
        print(name)
        print("F1 score and accuracy score for test set: {:.4f} , {:.4f}.".format(f1, acc))


    def __predictProbabilitiesForUpcoming(self,clf):
        featureTargetManager = FeatureTargetManager(self.__league)
        features=featureTargetManager.getFeatureToPredictUpcoming()
        y_pred = clf.predict_proba(features)
        return y_pred

    def getProbabilitiesForUpcomingMatches(self,clf):
        teams=Helper.getTeamsForUpcoming(self.__league)
        matchweek=Helper.getMatchweekForUpcoming(self.__league)
        p=self.__predictProbabilitiesForUpcoming(clf)
        teamsAndProbability = np.append(teams, p, axis=1)
        teamsAndProbability = pd.DataFrame(data=teamsAndProbability)
        teamsAndProbability = teamsAndProbability.drop([0], 1)
        teamsAndProbability.columns = ['HomeTeam', 'AwayTeam', '2', 'X', '1']
        teamsAndProbability=teamsAndProbability[['HomeTeam', 'AwayTeam', '1', 'X', '2']]
        teamsAndProbability.to_csv("data/"+self.__league+"/Predictions/week:"+str(matchweek)+".csv")

    def getLogisticRegressionClassifier(self):
        return self.__clf_A





