import numpy as np
import plotly.express as px
import pandas as pd
import dash
# from dash import dcc, html, Input, Output, callback,State
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default='browser'
from datetime import date, timedelta
import datetime
import numpy as np
import urllib.parse
import urllib
import dash_bootstrap_components as dbc
import sqlalchemy
import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, \
    ServersideOutputTransform,callback
from pandarallel import pandarallel
pandarallel.initialize()
import pandas as pd
import time
from pandarallel import pandarallel


params =urllib.parse.quote_plus('Driver={ODBC Driver 13 for SQL Server};'
                                'Server=tcp:shopifyai.database.windows.net,1433;'
                                'Database=ShopifyAI;'
                                'Uid=aiadmin;Pwd=kfk9072p!;'
                                'Encrypt=yes;'
                                'TrustServerCertificate=no;'
                                'Connection Timeout=30;')
engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
# df_size = int(5e6)
# df = pd.DataFrame(dict(a=np.random.randint(1, 8, df_size),
#                        b=np.random.rand(df_size)))
# # df["c"] = df.groupby("a").parallel_apply(lambda x:x.b.sum())
# df = df.groupby("a").parallel_apply(lambda x:x.sum())



client_id = 100


tableau_file=pd.read_sql(f"select Date,CustomerID,product_type,quantity,amount,price,product_id,variant_id,sku from salesanalytics where cid = {client_id}",engine)

max_date=tableau_file[tableau_file["quantity"].notnull()]["Date"].max()
max_date=pd.to_datetime(max_date).date()
# max_date=date.today()
df = tableau_file.copy()  # iris is a pandas DataFrame
df["product_type"]=df["product_type"].astype(str)
df["CustomerID"]=df["CustomerID"].astype(str)
df["product_id"]=df["product_id"].astype(str)
df["variant_id"]=df["variant_id"].astype(str)

# def mains():
days_prev="ALL"
total_revenue=df.copy()
                       
df_copys=total_revenue[total_revenue["quantity"]>=0]

def summation(x):
    import numpy
    return numpy.sum(x.quantity)
df_copy=df_copys.copy()
import time
start=time.time()
df_copyaa=df_copy.groupby(['Date','product_type','product_id']).\
                    parallel_apply(summation).reset_index()     
print(time.time()-start)
start=time.time()
df_copyas=df_copy.groupby(['Date','product_type','product_id']).\
                    apply(summation).reset_index()     
print(time.time()-start)



# import numpy as np
# df_size = int(5e6)
# df = pd.DataFrame(dict(a=np.random.randint(1, 8, df_size),
#                        b=np.random.rand(df_size)))

# pandarallel.initialize(progress_bar=True)
# def func(x):
#     import math
#     return math.sin(x.a**2) + math.sin(x.b**2)

# res_parallel = df.apply(func, axis=1)
      
revenue=df_copy["revenue"].sum()

# if __name__ == "__main__":

#     mains()



