import pandas as pd

df = pd.read_csv("data/processed/master_dataset.csv")
print(df.columns.tolist())