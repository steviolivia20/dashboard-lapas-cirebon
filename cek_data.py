import pandas as pd

df = pd.read_excel("data.xlsx")

print("5 data teratas:")
print(df.head())

print("\nNama kolom:")
print(df.columns)

print("\nInfo dataset:")
print(df.info())
