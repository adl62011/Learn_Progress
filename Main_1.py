import pandas as pd
import numpy as np
import matplotlib as plt

df = pd.read_csv("energy_sensor_data.csv")

df['Timestamp'] = pd.to_datetime(df['Timestamp'])

df['Net_Profit_IDR'] = (df['Energy_Output']*2000) - (df['Maintenance_Cost']) 

#print(df.head(3))
df.sort_values(by='Net_Profit_IDR')

print(df)