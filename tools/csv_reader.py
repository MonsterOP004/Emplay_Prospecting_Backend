import pandas as pd

def load_audience(path: str) -> list[dict]:
    df = pd.read_csv(path)
    return df.to_dict(orient='records')
