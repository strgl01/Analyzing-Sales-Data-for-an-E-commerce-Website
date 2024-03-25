import pandas as pd
import func


# reading the csv file using encoding parameter to read without error
data=pd.read_csv('data.csv',encoding='ISO-8859-1')

# convert invoicedate to datetime
data=func.conv_to_datetime(data,'InvoiceDate')

# this fn sorts a df on certain column and returns whole df
data=func.sort_on_column(data,['InvoiceDate'],'True')

# this fn take two series and retuen product of both
data['Total_Price']=func.mult_col(data['Quantity'],data['UnitPrice'])

#print(data[data['Description'].isnull()].shape)
#print(data.shape)

# On analysis found if description was NAN it was a garbage row
data=data.dropna(subset=['Description'])

# On analysis found if unitprice was 0 it was a garbage row
data=data[data['UnitPrice']!=0]

#on analysis custID has nan
data=data[data['CustomerID'].notnull()]

# on analysis fount quantity for certain stock was negative to handle that created group on basis of CustomerID and called fn on it
cust=data.groupby('CustomerID')
new_data=cust.apply(func.remove_only_negative_stocks)
new_data=new_data.drop(columns=['CustomerID']).reset_index()
new_data=new_data.drop(columns=['level_1'])
#stored cleaned data in clean_data.csv
new_data.to_csv('clean_data.csv')























#print(data.groupby('CustomerID').sample(1))
# print(data.sample(10))
#print(data.shape)
# print(data[['Order_Date']])
#print(data[(~data['InvoiceNo'].str.startswith('C'))&(data['Quantity']<0)])

#print(data.columns.to_list())
#print(data[data['StockCode']=='20703'])
#print(data[(data['CustomerID']==17375.0)&(data['StockCode']=='20703')])
# print(data[data['Description'].isnull()])
# print(data[['StockCode','Description']])
#print(data.head())
#print(data[data['CustomerID']==12605.0])
#print(data.shape)
#print(data[(data['InvoiceNo']=='C540307') | (data['InvoiceNo']=='540307')])
#print(data[data['InvoiceNo']=='540307'])
#print(data.groupby('StockCode')['Quantity'].count())
#print(data[data['StockCode']=='21035']['Quantity'].sum())
#temp=data.groupby('CustomerID')['Quantity'].sum()
#print(temp[temp<0].index.to_list())
#print(data['CustomerID'].hasnans)
#print(data['StockCode'].hasnans)

#temp=data[data['CustomerID']==17375.0]

#print('***********************new ***************')
#func.no_pur_remove(temp)
#print(func.no_pur_remove(temp))

#print('***********************new ***************')
#print(new_data.shape)
#print(new_data[new_data['CustomerID']==12503.0])
#new_data.drop(columns=['index'],inplace=True)

#print(new_data.sample(50))
#print(new_data.groupby('StockCode')['Quantity'].count())
#print(new_data[new_data['StockCode']=='21035'])
#stock=new_data.groupby('StockCode')
#print(stock[new_data.groupby('StockCode')['Quantity'].sum()<0])

#df=new_data.groupby('StockCode')['Quantity'].sum().reset_index()
#print(df[df['Quantity']<0])
#print(new_data[new_data['StockCode']=='20703'])
#print(new_data[(new_data['CustomerID']==17375.0)&(new_data['StockCode']=='20703')])