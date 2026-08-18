from sklearn.ensemble import RandomForestClassifier


def train_model(rfm):
    rfm['HighValue'] = rfm['Segment'].apply(lambda x: 1 if x == 'VIP' else 0)
    X = rfm[['Recency', 'Frequency', 'Monetary']]
    y = rfm['HighValue']

    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model
