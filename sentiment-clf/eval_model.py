"""This code is incomplete as of 8/21/2018
"""
from sklearn.model_selection import train_test_split
import pickle
import pandas as pd


def eval_model(path):

    with open(path) as f:
        model = pickle.load(f)

    with open('chalicelib/all/train.tsv') as f:
        data = pd.read_csv(f, sep='\t')

    pos_neg = data[(data['Sentiment'] == 0) | (data['Sentiment'] == 4)]

    pos_neg['Binary'] = pos_neg.apply(
        lambda x: 0 if x['Sentiment'] == 0 else 1, axis=1)

    X = model.vectorizer_transform(pos_neg.loc[:, 'Phrase'])
    print('Vectorizer transform complete')
    y = pos_neg.loc[:, 'Binary']

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model.plot_roc(model, X_test, y_test)


if __name__ == "__main__":

    path = 'chalicelib/models/NLPClassifier.pkl'
    eval_model(path)
