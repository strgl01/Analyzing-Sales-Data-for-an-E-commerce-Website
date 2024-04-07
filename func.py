import pandas as pd
import numpy as np


# take a df and column and convert that column to datetime
def conv_to_datetime(df,column):
    df[column]=pd.to_datetime(df[column])
    return df

# take a df and column and bool vale and sort df on basis of that column
def sort_on_column(df,column,asc):
    df=df.sort_values(column,ascending=bool(asc))
    return df

# take two series and multiply it
def mult_col(sr_A,sr_B):
    return sr_A*sr_B


#this fn remove custid or stock which had only negative value, works on group object. Here while applying join i have not handeled NAN value because i have arleardy removed any NAN value from CustID column
def remove_only_negative_stocks(group):
    # divide each group in to part purchase and returned
    pur=group[~group['InvoiceNo'].str.startswith('C')][['StockCode','Quantity']]
    _ret=group[group['InvoiceNo'].str.startswith('C')][['StockCode','Quantity']]
    #print(pur)
    #print(_ret)
    # return a empty df if purchase df is empty
    if pur.empty:
        #print(1)
        return pd.DataFrame()
    # return same group if return df is empty
    elif _ret.empty:
        return group
    
    else:
        # gets stock names in purchase df
        pur_grp_name=list(pur.groupby('StockCode').groups.keys())
        #print(pur_grp_name)
        # df of purchase stock and there total quantity
        pur_grp=pur.groupby('StockCode').sum().reset_index()
        # gets stock names in return df
        _ret_grp_name=list(_ret.groupby('StockCode').groups.keys())
        # df of return stock and there total quantity
        _ret_grp=_ret.groupby('StockCode').sum().reset_index()
        #print(_ret_grp_name)
        # stock list which are only returned not purchased
        reject_stock=np.setdiff1d(_ret_grp_name,pur_grp_name)
        #check if no reject stock in list
        if reject_stock.size==0:
            # join two df pur_grp and _ret_grp
            temp=pur_grp.merge(_ret_grp,on='StockCode',how='inner')
            # check if any stock is returned more times than no. of time purchased
            temp['Quantity']=temp['Quantity_x']+temp['Quantity_y']
            # collect those stock which has negative quantity
            garbage_stock=temp[temp['Quantity']<0]['StockCode'].to_list()
            # remove above collected stock from each group
            group=group[~(group['StockCode'].isin(garbage_stock))]
            return group
        else:
            # creat a new return df because some stock were only in return df not in purchase df hence removed those
            _ret=_ret[~(_ret['StockCode'].isin(reject_stock))]
            # remove rejected stock from group also
            group=group[~(group['StockCode'].isin(reject_stock))]
             # df of return stock and there total quantity
            _ret_grp=_ret.groupby('StockCode').sum().reset_index()
                #print(pur)
                #print(_ret)
            # join two df pur_grp and _ret_grp
            temp=pur_grp.merge(_ret_grp,on='StockCode',how='inner')
            # check if any stock is returned more times than no. of time purchased
            temp['Quantity']=temp['Quantity_x']+temp['Quantity_y']
            # collect those stock which has negative quantity
            garbage_stock=temp[temp['Quantity']<0]['StockCode'].to_list()
            # remove above collected stock from each group
            group=group[~(group['StockCode'].isin(garbage_stock))]
            return(group)



# fn to sort inside each group for stockcode
def Sort_each_group_Stock(group,arg1):
    return(group.sort_values(by='Quantity',ascending=arg1)[['Year','Quarter','Country','StockCode','Quantity']].head(5))

# fn to sort inside each group for Customer
def Sort_each_group_Cust(group,arg1):
    return(group.sort_values(by='Total_Price',ascending=arg1)[['Year','Quarter','Country','CustomerID','Total_Price']].head(5))


# fn to find stock pairs
def coupled_stocks(Stock, df):
    d={}
    done=[]
   
    for j in Stock:
        if j in done:
            print(done)
            continue

        else:
           
           print(j)
           Invoice = df[df['StockCode']==j]['InvoiceNo'].unique().tolist()
           row_newdf=[]
           unq_stock_in_df=np.array([])
           d[j]=[]
           for i in Invoice:
            
            temp=df[df['InvoiceNo']==i]
            row_newdf.append(temp['StockCode'].tolist())
            unq_stock_in_df=np.union1d(unq_stock_in_df,np.array(temp['StockCode'].tolist()))
        
           new_df=pd.DataFrame(row_newdf)
           total_space=new_df.shape[0]
           for stck in unq_stock_in_df:
                if stck==j:
                    continue
                else:
                    count=new_df.eq(stck).sum().sum()
                    prob=(count/total_space)*100
                
                    if prob>50:
                        d[j].append(stck)
                        done.append(stck)
       

    print(d)
    return(d)
        
                

    

        



