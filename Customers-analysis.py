#Import library

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Import csv file
df =pd.read_csv('Customers.csv',low_memory=False)

#Check the first 5 rows of the dataframe
#print(df.head())

###--Data Cleaning--###
##--Change dtype--## 
#Change data type of 'Gender' to boolean
df['Gender'] = df['Gender'].map({'Male': True, 'Female': False})

#Change the data type of 'Zip Code' column to int
df['Zip Code'] = pd.to_numeric(df['Zip Code'], errors='coerce').fillna(0).astype(int)

#Change data type of 'Birthday' to datetime
df['Birthday'] = pd.to_datetime(df['Birthday'], errors='coerce')

#Check the data types of each column
#print(df.dtypes)

##--Handle missing values--##
#Check for missing values in each column
#missing_values = df.isnull().sum()
#print("Missing values in each column:\n", missing_values)

#show rows with missing values
#missing_rows = df[df.isnull().any(axis=1)]
#print("Rows with missing values:\n", missing_rows)

#Replace missing values in 'State Code' with 'NA'
df['State Code'] = df['State Code'].fillna('NA')

#--Data Analysis--##
#Calculate age from 'Birthday' column
current_date = pd.to_datetime('today')
df['Age'] = (current_date - df['Birthday']).dt.days // 365

#Group ages into bins
age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
age_labels = ['<18', '18-24', '25-34', '35-44', '45-54', '55-64', '65+']
df['Age Group'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels, right=False)

#Plot: Create a histogram to visualize age distribution
plt.figure(figsize=(10, 6))
plt.hist(df['Age'].dropna(), bins=age_bins, edgecolor='black', alpha=0.7)
plt.xlabel('Age')
plt.ylabel('Number of Customers')
plt.title('Age Distribution of Customers')
plt.xticks(age_bins)
plt.grid(axis='y')
plt.show()


#Calculate average age
average_age = df['Age'].mean()
#print(f"Average Age: {average_age:.2f} years")


#Count number of customers by each continent
continent_counts = df['Continent'].value_counts()
#print("Number of customers by continent:\n", continent_counts)

#Plot: Create a bar chart to visualize customer distribution by continent
plt.figure(figsize=(10, 6))
plt.bar(continent_counts.index, continent_counts.values, color='skyblue')
plt.xlabel('Continent')
plt.ylabel('Number of Customers')
plt.title('Customer Distribution by Continent')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Count number of customers by gender
gender_counts = df['Gender'].value_counts()
gender_counts.index = ['Male' if x else 'Female' for x in gender_counts.index]
print("\nNumber of customers by gender:")
print(gender_counts)

#Plot: Create a pie chart to visualize gender distribution
plt.figure(figsize=(8, 6))
plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%')
plt.title('Customer Gender Distribution')
plt.axis('equal')
plt.show()