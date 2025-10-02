#Import library

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Import csv file
df =pd.read_csv('Customers.csv',low_memory=False)

#Check the first 5 rows of the dataframe
#print(df.head())

##Change dtype 
#Change data type of 'Gender' to boolean
df['Gender'] = df['Gender'].map({'Male': True, 'Female': False})

#Change the data type of 'Zip Code' column to int
df['Zip Code'] = pd.to_numeric(df['Zip Code'], errors='coerce').fillna(0).astype(int)

#Change data type of 'Birthday' to datetime
df['Birthday'] = pd.to_datetime(df['Birthday'], errors='coerce')

#Check the data types of each column
print(df.dtypes)