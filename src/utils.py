import pandas as pd
import os
from pathlib import Path


def load_data(path=None):
    # If no path provided, try to find retail.csv relative to this file
    if path is None:
        # Get the directory where this file is located
        current_dir = Path(__file__).parent
        # Try multiple possible locations
        possible_paths = [
            current_dir.parent / "data" / "retail.csv",  # ../data/retail.csv
            Path.cwd() / "data" / "retail.csv",  # ./data/retail.csv
            Path.cwd() / "customer_project" / "data" / "retail.csv",  # ./customer_project/data/retail.csv
        ]
        
        path = None
        for p in possible_paths:
            if p.exists():
                path = str(p)
                break
        
        if path is None:
            raise FileNotFoundError(f"retail.csv not found in expected locations: {[str(p) for p in possible_paths]}")
    
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
