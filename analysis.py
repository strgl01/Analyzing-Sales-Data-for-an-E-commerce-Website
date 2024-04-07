import pandas as pd
import time
import func
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv('clean_data.csv')
# convert invoicedate to datetime
df=func.conv_to_datetime(df,'InvoiceDate')
# creating few columns to do some timly analysis
df['Quarter']=df['InvoiceDate'].dt.quarter
df['Month']=df['InvoiceDate'].dt.month_name()
df['Day']=df['InvoiceDate'].dt.day_name()
df['Year']=df['InvoiceDate'].dt.year
df['Date']=df['InvoiceDate'].dt.date

'''Top 5 stock from each country per quarter'''

# creating a desired group and perform agg and convert the series into df
stock_quaterly=df.groupby(['Year','Quarter','Country','StockCode'])['Quantity'].sum().reset_index()
# creating a group from above df to get top 5 stocks from each country
temp=stock_quaterly.groupby(['Year','Quarter','Country'])
# calling fn to perform sorting on stock and giving top 5 stock from each country
top_5_stock_from_each_country_per_year_per_quarter=temp.apply(func.Sort_each_group_Stock,arg1=False)
# droping the index got from groups through fn return
top_5_stock_from_each_country_per_year_per_quarter=top_5_stock_from_each_country_per_year_per_quarter.reset_index(drop=True).sort_values(['Year','Quarter','Country'])


'''Last 5 Coustmer from each country per quarter'''

# creating a desired group and perform agg and convert the series into df
Last_Coustmer_quaterly=df.groupby(['Year','Quarter','Country','CustomerID'])['Total_Price'].sum().reset_index()
# creating a group from above df to get Last 5 cust from each country
temp=Last_Coustmer_quaterly.groupby(['Year','Quarter','Country'])
# calling fn to perform sorting on stock and giving Last 5 cust from each country
Last_5_Cust_from_each_country_per_year_per_quarter=temp.apply(func.Sort_each_group_Cust,arg1=True)
# calling fn to perform sorting on stock and giving top 5 cust from each country
Top_5_Cust_from_each_country_per_year_per_quarter=temp.apply(func.Sort_each_group_Cust,arg1=False)
# droping the index got from groups through fn return
Last_5_Cust_from_each_country_per_year_per_quarter=Last_5_Cust_from_each_country_per_year_per_quarter.reset_index(drop=True).sort_values(['Year','Quarter','Country'])
# droping the index got from groups through fn return
Top_5_Cust_from_each_country_per_year_per_quarter=Top_5_Cust_from_each_country_per_year_per_quarter.reset_index(drop=True).sort_values(['Year','Quarter','Country'])

# print(top_5_stock_from_each_country_per_year_per_quarter.head(6))
# print(Last_5_Cust_from_each_country_per_year_per_quarter.head(6))
# print(Top_5_Cust_from_each_country_per_year_per_quarter.head(6)) 

Stock=df['StockCode'].unique()
# print(Stock)
# print(df[df['StockCode']=='23166'])


# with open('stock.txt','w') as f:
#     f.write(func.coupled_stocks(Stock,df[~df['InvoiceNo'].str.startswith('C')][['InvoiceNo','StockCode']]))
a=df.groupby('Date')['Total_Price'].sum().reset_index()
print(a.shape)
# a.plot.scatter(x='Date',y='Total_Price')
# plt.show()
# sns.kdeplot(df['Total_Price'][:500])
# plt.show()
