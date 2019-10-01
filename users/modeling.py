import gzip
import dill
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import RFECV
import os

def focus_only_stats(df):
    def remove_excess_cols(df):
        return df[['APM', 'Drate', 'Da',  'Dc2', 'Dc4', 'Exposure',
       'GBrate', 'GBa', 'GBc2', 'Gut',
       'HIrate', 'HIa', 'HIc2', 'HIc4', 'HOrate', 'HOa', 'HOc2', 'HOc4',
       'LegLace', 'LSrate', 'LSa', 'LSc2', 'LSc4', 'NPF',
       'oAPM', 'oDrate', 'oDa', 'oDc2', 'oDc4', 'oExposure', 'oGBrate', 'oGBa',
       'oGBc2', 'oGut', 'oHIrate', 'oHIa', 'oHIc2', 'oHIc4', 'oHOrate', 'oHOa',
       'oHOc2', 'oHOc4', 'oLegLace', 'oLSrate', 'oLSa', 'oLSc2', 'oLSc4',
       'oNPF', 'oPassive', 'oPushout', 'oRecovery', 'oTrate',
       'oTa', 'oTc2', 'oTc4', 'oTurn', 'oViolation',
       'Passive', 'Pushout', 'Recovery', 'Trate', 'Ta',
       'Tc2', 'Tc4', 'Turn', 'Violation']]
    return remove_excess_cols(df).filter(regex='^[^o|O]')

def train_model():
    """Train a machine learning model to predict survival on the Titanic.

    Returns
    -------
    best_model : scikit-learn trained classifier
        Returns the best model found through tuning the hyperparameters.
    """
    cwd = os.getcwd()
    matchdata = pd.read_csv(cwd + '/collection/stats/matchdata.csv', engine='python')
    matchdata = matchdata[matchdata['Duration'] != 0] # remove forfeits
    nodupes = matchdata[matchdata['MatchID'].apply(lambda x: len(x) == 4)] # remove dupes

    # no weight or pasive diff or mov or duration (no points)
    # i.e. includes all advanced metrics and base stats (includes duration)
    # removes focus/team, opp/team, date, matchid, all result types except binary
    matches = nodupes[['APM', 'Drate', 'Da',  'Dc2', 'Dc4', 'Exposure',
           'GBrate', 'GBa', 'GBc2', 'Gut',
           'HIrate', 'HIa', 'HIc2', 'HIc4', 'HOrate', 'HOa', 'HOc2', 'HOc4',
           'LegLace', 'LSrate', 'LSa', 'LSc2', 'LSc4', 'NPF',
           'oAPM', 'oDrate', 'oDa', 'oDc2', 'oDc4', 'oExposure', 'oGBrate', 'oGBa',
           'oGBc2', 'oGut', 'oHIrate', 'oHIa', 'oHIc2', 'oHIc4', 'oHOrate', 'oHOa',
           'oHOc2', 'oHOc4', 'oLegLace', 'oLSrate', 'oLSa', 'oLSc2', 'oLSc4',
           'oNPF', 'oPassive', 'oPushout', 'oRecovery', 'oTrate',
           'oTa', 'oTc2', 'oTc4', 'oTurn', 'oViolation',
           'Passive', 'Pushout', 'Recovery', 'Trate', 'Ta',
           'Tc2', 'Tc4', 'Turn', 'Violation',
           'BinaryResult']]    #will drop binary result inplace later

    RESULTS = matches['BinaryResult'].values.tolist() # predictor variable y
    matches = matches.drop(columns=['BinaryResult']) # now drop

    # split into two dfs
    focusdf = matches.filter(regex='^[^o|O]')
    oppdf = matches.filter(regex='^o')

    # get averages from matches NOT the current put into two lists
    focus_predata = []
    for i, row in focusdf.iterrows():
        focus_predata.append(focusdf.drop(i).mean().tolist())

    opp_predata = []
    for i, row in oppdf.iterrows():
        opp_predata.append(oppdf.drop(i).mean().tolist())

    # subtract lists to get diff between focus averages and opponent averages before match
    DATA = np.subtract(focus_predata, opp_predata)

    X_train, X_test, y_train, y_test = train_test_split(DATA, RESULTS, test_size=0.20, random_state=42)

    logistic_classifier = LogisticRegressionCV(cv=5, max_iter=1000)
    logistic_classifier.fit(X_train, y_train)

    rfecv = RFECV(estimator=logistic_classifier, step=1, min_features_to_select=5, cv=5,
                  scoring='accuracy', n_jobs=2)
    rfecv.fit(X_test, y_test)
    return rfecv.estimator_, rfecv.support_

def serialize_model(file_name):
    """Serialize the trained machine learning model.

    Parameters
    ----------
    file_name : str (default='titanic_model.dill')
        File name to use when persisting trained model.
    """""

    tm = train_model()
    model = tm[0]
    support_array = tm[1]
    with gzip.open(file_name, 'wb') as f:
        dill.dump(model, f)

    with gzip.open('support_array.dill.gz', 'wb') as f:
        dill.dump(support_array, f)

def deploy_model(file_name='freestyle_model.dill.gz'):
    """Return the loaded trained model.

    Parameters
    ----------
    file_name : str (default='titanic_model.dill.gz')
        File name to use when persisting trained model.

    Returns
    -------
    model : scikit-learn trained classifier
        Returns the serialized trained model.
    """

    # if the model has not been persisted, create it
    try:
        with gzip.open(file_name, 'rb') as f:
            model = dill.load(f)
        with gzip.open('support_array.dill.gz', 'rb') as f:
            support = dill.load(f)
    except FileNotFoundError:
        print("Trained model not found, creating the file.")
        serialize_model(file_name)
        return deploy_model(file_name=file_name)

    return model, support
