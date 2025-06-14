from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import os

def train_classifier(file_path):
    if not os.path.exists(file_path):
        return None, None

    dfs = pd.read_excel(file_path, sheet_name=None)
    data = pd.concat(dfs.values(), ignore_index=True)

    data = data.dropna(subset=["description", "category"])
    if data.empty:
        return None, None

    X = data["description"]
    y = data["category"]

    vectorizer = CountVectorizer()
    X_vect = vectorizer.fit_transform(X)

    model = MultinomialNB()
    model.fit(X_vect, y)

    return model, vectorizer

def predict_category(description, model, vectorizer):
    if model is None or vectorizer is None:
        return "Other"
    X = vectorizer.transform([description])
    return model.predict(X)[0]
