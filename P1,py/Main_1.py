import pandas as pd

df = pd.read_csv('data_test.csv')

df['Efficiency'] = df['Energy_Output'] / df['Operating_Hours']

df['Status'] = 'NORMAL'

df.loc[df['Temperature'] > 85, 'Status'] = 'OVERHEAT'

#Filtering Missing Data

df['Machine_ID'] = df['Machine_ID'].fillna('Turbine_C')


# Agreggration
print(df.groupby('Machine_ID')[['Temperature', 'Efficiency']].mean().reset_index())


