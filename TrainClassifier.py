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

from time import time
from sklearn.metrics import f1_score


def train_classifier(clf, X_train, y_train):
    clf.fit(X_train, y_train)

def predict_labels(clf, features, target):
    y_pred = clf.predict(features)
    return f1_score(target, y_pred, pos_label='H',average='micro'), sum(target == y_pred) / float(len(y_pred))

def predict_possibilities(clf,features):
    y_pred = clf.predict(features)
    return y_pred

def train_predict(clf, X_train, y_train, X_test, y_test):
    clf.fit(X_train, y_train)
    f1, acc = predict_labels(clf, X_train, y_train)
    print("F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1, acc))
    f1, acc = predict_labels(clf, X_test, y_test)
    print("F1 score and accuracy score for test set: {:.4f} , {:.4f}.".format(f1, acc))

def preprocessFeatures(X_all):
    output=pd.DataFrame(index=X_all.index)
    for col, col_data in X_all.iteritems():
        if col_data.dtype==object:
            col_data=pd.get_dummies(col_data,prefix=col)
        output=output.join(col_data)

    cols = [['HomeGoalDiff', 'AwayGoalDiff', 'DiffInGoals', 'DiffPts', 'HomeTeamPoints', 'AwayTeamPoints']]
    for col in cols:
        X_all[col] = scale(X_all[col])
    return output

def SeperateFeatureAndTarget():
    dataframe = pd.read_csv("final.csv", index_col=0)
    X_all = dataframe.drop(
        ['FTR', 'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'HomeTeamScored', 'AwayTeamScored', 'HomeTeamConceded',
         'AwayTeamConceded'], 1)
    Y_all = dataframe['FTR']
    return X_all,Y_all

def main():
    X_all,Y_all=SeperateFeatureAndTarget()
    X_all=preprocessFeatures(X_all)
    X_train,X_test,y_train,y_test = train_test_split(X_all,Y_all,
                                                     test_size=45,
                                                     random_state=2,
                                                     stratify=Y_all)

    clf_A = LogisticRegression(random_state = 42)
    clf_B = SVC(random_state = 912, kernel='rbf')
    clf_C = xgb.XGBClassifier(seed = 82)

    train_predict(clf_A, X_train, y_train, X_test, y_test)
    train_predict(clf_B, X_train, y_train, X_test, y_test)
    train_predict(clf_C, X_train, y_train, X_test, y_test)

    print ('')
    