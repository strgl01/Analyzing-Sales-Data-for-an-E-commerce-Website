
import numpy as np
import pandas as pd
# # Create a DataFrame
# data = {'col1': [1, 2, 3, 4, 5],
#         'col2': [5, 4, 3, 2, 1],
#         'col3': [1, 9, 3, 2, 1]}
# df = pd.DataFrame(data)

# # Count occurrences of a specific integer in the DataFrame
# count = df.eq(3).sum().sum()

# print("Number of occurrences of integer 3 in DataFrame:", count)






def coupled_stocks(Stock, df):
    d={}
    done=[]

    for j in Stock:
        if j in done:
            continue
        else:
           
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
                        print(j)
                        d[j].append(stck)
                        done.append(stck)
       

    print(d)