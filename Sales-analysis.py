'''
Checklist

#Data Prep
- [x] Import csv related to sales data
- [x] Merge all sales data into single df
- [x] Clean data (change dtypes, drop unwanted columns)
- [x] Calculate sales based on qty and product and add as new column
- [x] Calculate profit and add as new column for each product
- [x] Calculate profit margins and add as new column


#Analysis
## General Sales Analysis
- [] Generate summary of sales channels (online vs offline)
- [] Visualize sales trends over time (monthly/quarterly)
- [] Brand sales performance VS profit margin (to identify high-performing brands for partnerships or promotions or to invest more in them)
- [] Which product categories have high profit margins (to focus marketing and sales efforts on high-margin products)
- [] What is the correlation between sales volume and profit margin across different product categories (to optimize inventory and marketing strategies)
## Customer analysis for Marketing
- [] what type of customer typically would have a higher percentage of profit margin
- [] Top 10% of customer buy product from which channel (offline/online) (to optimize sales channels and marketing strategies)
- [] What seasonal trends exist in sales data (to target marketing campaigns)
- [] For top 10% of customers by sales, what is their average profit margin (to identify and target high-value customers for loyalty programs or special offers)
- [] for high profit margin products, what is the typical customer demographic (to tailor marketing strategies to the right audience)
## Store Analysis
- [] distribution of profit margin (by country and regions)
- [] Offline store that have highest sales per square ft (to determine best locations for new stores or expansion)
- [] Which country have many offiline sales vs online sales (to determine market preferences to expand into new regions)
- [] For top top 5 stores by sales, what is their average profit margin (to identify successful store strategies that can be replicated elsewhere)
- [] For top 5 stores by profit margin, which categories contribute most to their profit and their square ft (to focus on inventory and distribution strategies)

'''

#Import necessary libraries
import pandas as pd # type: ignore
import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

#Import csv
sales_table =pd.read_csv('Sales.csv',low_memory=False)
prod_table = pd.read_csv('Products.csv',low_memory=False)
store_table = pd.read_csv('Stores.csv',low_memory=False)
customer_table = pd.read_csv('Customers_cleaned.csv',low_memory=False)

#Merge all sales data into single df
merged_df = sales_table.merge(prod_table, on='ProductKey', how='left') \
                       .merge(store_table, on='StoreKey', how='left') \
                       .merge(customer_table, on='CustomerKey', how='left')

#Drop unwanted columns
df = merged_df.drop(columns=['Order Number', 'Line Item', 'Delivery Date', 'Currency Code', 'Gender', 'Name','City','State Code',
                            'Zip Code','Continent','Birthday','Product Name','Color','SubcategoryKey','Subcategory', 'Open Date',
                            'CustomerKey', 'ProductKey','State_y','Country_y','State_x','CategoryKey'])

#Check the first 5 rows of the dataframe
#print(df.head(10))

#Check the data types of each column
#print(df.dtypes)

#Change Data Types
df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')

#Convert monetary columns to numeric
cols_to_convert = ["Unit Cost USD", "Unit Price USD"]
for col in cols_to_convert:
    #Remove any non-numeric characters (like $) if present
    df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
        )
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

df['Square Meters'] = pd.to_numeric(df['Square Meters']).fillna(0)

#print(df.dtypes)


#Profit Calculation
df["SalesAmount"] = df["Unit Price USD"] * df["Quantity"]
df["CostAmount"] = df["Unit Cost USD"] * df["Quantity"]
df["RevenueDifference"] = df["SalesAmount"] - df["CostAmount"] 
df["ProfitMargin"] = df["RevenueDifference"] / df["SalesAmount"] * 100 
#Profit margin in percentage to 2 decimal places
df["ProfitMargin"] = df["ProfitMargin"].round(2)



#print(df.head(10))