import pandas as pd
import func
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

# clas implements Linear Regression using OLS Meathod
class MeraLR:
    
    def __init__(self):
        self.m = None
        self.b = None
        
    def fit(self,X_train,y_train):
        
        num = 0
        den = 0
        
        for i in range(X_train.shape[0]):
            
            num = num + ((X_train[i] - X_train.mean())*(y_train[i] - y_train.mean()))
            den = den + ((X_train[i] - X_train.mean())*(X_train[i] - X_train.mean()))
        
        self.m = num/den
        self.b = y_train.mean() - (self.m * X_train.mean())
        # print(self.m)
        # print(self.b)       
    
    def predict(self,X_test):
        
        
        return self.m * X_test + self.b
    




# Data Analysis Code


df=pd.read_csv('clean_data.csv')
# convert invoicedate to datetime
df=func.conv_to_datetime(df,'InvoiceDate')
#print(df.shape)
# creating few columns to do some timly analysis
df['Quarter']=df['InvoiceDate'].dt.quarter
df['Month']=df['InvoiceDate'].dt.month_name()
df['Day']=df['InvoiceDate'].dt.day_name()
df['Year']=df['InvoiceDate'].dt.year
df['Date']=df['InvoiceDate'].dt.date

#Top 5 stock from each country per quarter

# creating a desired group and perform agg and convert the series into df
stock_quaterly=df.groupby(['Year','Quarter','Country','StockCode'])['Quantity'].sum().reset_index()
# creating a group from above df to get top 5 stocks from each country
temp=stock_quaterly.groupby(['Year','Quarter','Country'])
# calling fn to perform sorting on stock and giving top 5 stock from each country
top_5_stock_from_each_country_per_year_per_quarter=temp.apply(func.Sort_each_group_Stock,arg1=False)
# droping the index got from groups through fn return
top_5_stock_from_each_country_per_year_per_quarter=top_5_stock_from_each_country_per_year_per_quarter.reset_index(drop=True).sort_values(['Year','Quarter','Country'])


#Last 5 Coustmer from each country per quarter

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

# Stock=df['StockCode'].unique()
# print(Stock)
# print(df[df['StockCode']=='23166'])
#couple_stock=func.coupled_stocks(Stock,df[~df['InvoiceNo'].str.startswith('C')][['InvoiceNo','StockCode']])


# DF to observe relation b/w Quantity and Price
lr_a=df.groupby('Date')[['Quantity','Total_Price']].sum().reset_index()

# print(a.head(5))
# a.plot.scatter(x='Quantity',y='Total_Price')
# plt.show()
# sns.kdeplot(df['Total_Price'][:500])
# plt.show()

# Implementing Linear Regression
x = lr_a.iloc[:,1].values

y = lr_a.iloc[:,2].values

X_train,X_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=2)

lr = MeraLR()
lr.fit(X_train,y_train)










import streamlit as st
#from analysis import * 

st.set_page_config(layout='wide',page_title='E-commerce Data Analysis')

st.sidebar.title('Analyzing Sales Data for an E-commerce Website')
st.title('Analyzing Sales Data for an E-commerce Website')
selection = st.sidebar.selectbox('Select one',['Summary Of Data','Top stock/Customer','Stock Sold Together','ML Model'])

if selection=='Summary Of Data':

    st.header('Key Insights from Analysis')
    st.markdown('''
    1. Data had 8 features and 541909 records
    2. On analysing data we found for some records Unit Price column had 0 value and for same record Quantity column also had -ve value
    3. On further analysis found the Description and Stock column were NAN, So we removed these records
    4. Observed on sumation of Quantity column for each stock some stocks had -ve output which established some records were wrong as if something is not purchased how it can be returned. 
    5. For now i didn't considered these stocks as it was giving an ambiguous information
    6. After doing all the cleaning now we had 9 features and 405595 records.
    7. We created some features to help our analysis from existing columns like Quarter, Date, Total Price, etc
    8. On the cleaned data we have performed both descripive and inferential statistics.
    9. Please try other selection from sidebar to get more insights from data 
    ''')
    st.balloons()

    
elif selection=='Top stock/Customer':


    option1=st.selectbox('Select Country',df['Year'].sort_values().unique().tolist())
    option2=st.selectbox('Select Country',df['Quarter'].sort_values().unique().tolist())
    option3=st.selectbox('Select Country',df['Country'].sort_values().unique().tolist())

    st.subheader('Top Stock')
    st.dataframe(top_5_stock_from_each_country_per_year_per_quarter[(top_5_stock_from_each_country_per_year_per_quarter['Year']==option1) & (top_5_stock_from_each_country_per_year_per_quarter['Quarter']==option2) & (top_5_stock_from_each_country_per_year_per_quarter['Country']==option3)])

    st.subheader('Top Customer')
    st.dataframe(Top_5_Cust_from_each_country_per_year_per_quarter[(Top_5_Cust_from_each_country_per_year_per_quarter['Year']==option1) & (Top_5_Cust_from_each_country_per_year_per_quarter['Quarter']==option2) & (Top_5_Cust_from_each_country_per_year_per_quarter['Country']==option3)])

    st.subheader('Last Customer')
    st.dataframe(Last_5_Cust_from_each_country_per_year_per_quarter[(Last_5_Cust_from_each_country_per_year_per_quarter['Year']==option1) & (Last_5_Cust_from_each_country_per_year_per_quarter['Quarter']==option2) & (Last_5_Cust_from_each_country_per_year_per_quarter['Country']==option3)])
    st.balloons()

elif selection=='Stock Sold Together':

    option4=st.selectbox('Select a stock code to get other stock code which has high probability of selling with it',df['StockCode'].sort_values().unique().tolist())


    js=func.coupled_stocks([option4],df[~df['InvoiceNo'].str.startswith('C')][['InvoiceNo','StockCode']])


    k=list(js.keys())
    st.header('Stock Description')

    st.subheader(str(df[df['StockCode']==k[0]]['Description'].unique()[0]))


    if js.values():
        a=list(js.values())
        if len(a[0])==0:
            st.write('No stock which was sold with it')
        else:
            t=[]
            for i in a[0]:
                t.append(df[df['StockCode']==i]['Description'].unique())
            st.table(t)

else:

    st.header('Graph of Quantity VS Price')
    st.scatter_chart(lr_a,x='Quantity',y='Total_Price')
    st.write('We see that this graph is somewhat Linear we are applying Linear Regression to predict price if certain value of quantity is given as input')


    st.header('Select Quantity to get estimation of Total Price')
    option5=st.selectbox('Select Quantity sold on any single day',X_test)

    st.write('Estimated price of the quantity sold on a single day')
    st.write(lr.predict(option5))
    st.balloons()

    
