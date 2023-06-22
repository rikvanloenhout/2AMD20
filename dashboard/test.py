import pandas as pd
from ke_app.data import get_crime_data, get_life_data, get_happiness_data, get_poverty_data, get_merged

df_combined = pd.read_csv("../datasets/all_data.csv")
df_merged = get_merged(df_combined, 0.25, 0.25, 0.25, 0.25)
df_merged['outlier'] = df_combined['outliers']
print(df_merged.head())