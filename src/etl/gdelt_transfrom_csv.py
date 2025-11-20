import pandas as pd

df = pd.read_parquet("part-00000-f79bd33c-9d44-40e4-9041-d72fedf0793d-c000.snappy.parquet")
print(df)
print(df.shape)