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
- [x] Generate summary of sales channels (online vs offline)
- [x] Visualize sales trends over time (monthly/quarterly)
- [X(KIV)] Brand sales performance VS profit margin (to identify high-performing brands for partnerships or promotions or to invest more in them)
- [x] Which product categories have high profit margins (to focus marketing and sales efforts on high-margin products)
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

#--Analysis--##
'''Generate summary of sales channels (online vs offline)'''
#Group Sales Channel and calculate total sales and profit margin (If StoreKey=0 then online else offline)
sales_channel_summary = df. groupby(df['StoreKey'].apply(lambda x: 'Online' if x == 0 else 'Offline')).agg(
    Total_Sales=('SalesAmount', 'sum'),
    Average_Profit_Margin=('ProfitMargin', 'mean')
).reset_index()
#print(sales_channel_summary)

'''Brand sales performance VS profit margin (to identify high-performing brands for partnerships or promotions or to invest more in them)'''
#Sales trends over time (monthly)
df['Order Month'] = df['Order Date'].dt.to_period('M')
monthly_sales_trends = df.groupby('Order Month').agg(
    Total_Sales=('SalesAmount', 'sum'),
    Average_Profit_Margin=('ProfitMargin', 'mean')
).reset_index()
#Count monthly sales count
monthly_sales_trends['Sales Count'] = df.groupby('Order Month').size().values
#print(monthly_sales_trends)

#Sales trends over time (quarterly)
quarterly_sales_trends = df.groupby(df['Order Date'].dt.to_period('Q')).agg(
    Total_Sales=('SalesAmount', 'sum'),
    Average_Profit_Margin=('ProfitMargin', 'mean')
).reset_index()
#Count quarterly sales count
quarterly_sales_trends ['Sales Count'] = df.groupby(df['Order Date'].dt.to_period('Q')).size().values
#print (quarterly_sales_trends)

'''Brand sales performance VS profit margin (to identify high-performing brands for partnerships or promotions or to invest more in them)'''
#Calculate Brand Sales Performance
brand_sales_performance = df.groupby(['Brand']).agg(Total_Sales=('SalesAmount', 'sum'),Average_Profit_Margin=('ProfitMargin', 'mean')).reset_index()
brand_sales_performance ['Sales Count'] = df.groupby(['Brand']).size().values #Calculate total sales count
#Sort the brand sales performance by Profit Margin in descending order
brand_sales_performance = brand_sales_performance.sort_values(by=['Average_Profit_Margin'], ascending=[False])
#print(brand_sales_performance.head(5)) #Niche Brand

#Top 5 brands by sales count
top_brands_by_sales_count = brand_sales_performance.sort_values(by=['Sales Count'], ascending=[False]).head(5)
#print(top_brands_by_sales_count)

'''Which product categories have high profit margins (to focus marketing and sales efforts on high-margin products)? '''
#Product categories have high profit margin
product_categories_profit_margin = df.groupby(['Category']).agg(Total_Sales=('SalesAmount', 'sum'),Average_Profit_Margin=('ProfitMargin', 'mean')).reset_index()
product_categories_profit_margin ['Sales Count'] = df.groupby(['Category']).size().values #Calculate total sales count
#Sort the product categories by Profit Margin in descending order
product_categories_profit_margin = product_categories_profit_margin.sort_values(by=['Average_Profit_Margin'], ascending=[False])
#print(product_categories_profit_margin.head(5)) #Electronics

#Top 5 product categories by sales count
top_product_categories_by_sales_count = product_categories_profit_margin.sort_values(by=['Sales Count'], ascending=[False]).head(5)
#print(top_product_categories_by_sales_count.head(5))

