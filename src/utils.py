import pandas as pd


def load_data(path):
    df = pd.read_csv(path, encoding='ISO-8859-1')
    df.dropna(subset=['CustomerID'], inplace=True)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
    return df


def compute_rfm(df):
    snapshot = df['InvoiceDate'].max()
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot - x.max()).days,
        'InvoiceNo': 'count',
        'TotalAmount': 'sum'
    }).reset_index()

    rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
    rfm['R_score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1], duplicates='drop')
    rfm['F_score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4], duplicates='drop')
    rfm['M_score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4], duplicates='drop')

    def segment(row):
        if row['R_score'] == 4 and row['F_score'] == 4:
            return 'VIP'
        elif row['F_score'] == 4:
            return 'Loyal'
        elif row['R_score'] == 4:
            return 'Recent'
        else:
            return 'Regular'

    rfm['Segment'] = rfm.apply(segment, axis=1)
    return rfm
