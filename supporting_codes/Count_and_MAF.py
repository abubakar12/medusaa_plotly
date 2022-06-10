
from dash import dcc
import numpy as np
import plotly.express as px
import pandas as pd
from dash import Dash,dcc, html, Input, Output, callback
tableau_file=pd.read_csv(r"C:\Users\hp\Desktop\medusaa_plotly\sample_data.csv")
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import json
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='browser'
from datetime import date, timedelta


max_date=pd.to_datetime("2-18-2022",format="%m-%d-%Y")
max_date=pd.to_datetime(max_date).date()
# max_date=date.today()


df = tableau_file.copy()  # iris is a pandas DataFrame
df["product_type"]=df["product_type"].astype(str)
df["CustomerID"]=df["CustomerID"].astype(str)
df=df[["Date",'Year','Month',"Day",'CustomerID','product_type','quantity','amount','price']]

df["Date"]=pd.to_datetime(df["Date"],format="%Y-%m-%d")

less_than_30=d =max_date- timedelta(days=30)
less_than_60=d =max_date- timedelta(days=60)
less_than_90=d =max_date- timedelta(days=90)
df["less_than_30"]=0
df["less_than_60"]=0
df["less_than_90"]=0
df.loc[df["Date"]>=pd.to_datetime(less_than_30),"less_than_30"]=1
df.loc[df["Date"]>=pd.to_datetime(less_than_60),"less_than_60"]=1
df.loc[df["Date"]>=pd.to_datetime(less_than_90),"less_than_90"]=1

df[df["less_than_90"]==1]



# app = Dash(__name__, suppress_callback_exceptions=True)
# server = app.server
    
layout = html.Div([
    html.Br(),
    html.H1("prod_type"),
    dcc.RadioItems(
        id='prod_type',
        options=df["product_type"].unique(),
        value=df["product_type"].unique()[-1]
    ),
    html.Br(),
    html.H1("Days_prev"),
    dcc.RadioItems(
        id='days_prev',
        options=['30','60','90','ALL'],
        value='ALL'
    ),
    html.H1("Moving Avg FIlter Window"),
    dcc.Slider(0, 10, 1,
               value=0,
               id='mov_avg_filt'),
    
    dcc.Graph(id="graph7")

])

@callback(
    Output("graph7", "figure"), 
    Input("prod_type", "value"),
    Input("days_prev","value"),
    Input("mov_avg_filt","value"),
    )
def display_(radio_value,days_prev,roll):

    df_copy=df[df["product_type"]==radio_value].drop("product_type",1)
    
    if days_prev=='30':
        df_copy=df_copy[df_copy["less_than_30"]==1]
        df_copy["count_orders"]=df_copy.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy["MAF"]=df_copy.groupby(['Date'])['count_orders'].\
            transform(lambda x:x.rolling(window=roll).mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
            

    elif days_prev=='60':
        df_copy=df_copy[df_copy["less_than_60"]==1]
        df_copy["count_orders"]=df_copy.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy["MAF"]=df_copy.groupby(['Date'])['count_orders'].\
                transform(lambda x:x.rolling(window=roll).mean())
                
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
         
    elif days_prev=='90':
        df_copy=df_copy[df_copy["less_than_90"]==1]
        df_copy["count_orders"]=df_copy.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy["MAF"]=df_copy.groupby(['Date'])['count_orders'].\
                transform(lambda x:x.rolling(window=roll).mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
        
         
    else:
        df_copy["count_orders"]=df_copy.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy["MAF"]=df_copy.groupby(['Date'])['count_orders'].\
                transform(lambda x:x.rolling(window=roll).mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
    

        
    # data=[]

    # data1 = {
    #     'x': df_copy.index,
    #     'y': df_copy['count_orders'],
    #     'mode': 'lines',
    #     'marker': {'color': '#0074D9'},
    #     'name': 'count_orders',
    #     'plot_bgcolor': 'plotly_dark'
    # }
    # data.append(data1)

    # data2 = {
    #     'x': df_copy.index,
    #     'y': df_copy['MAF'],
    #     'mode': 'lines',
    #     'marker': {'color': '#FF4136'},
    #     'name': 'MAF',
    #     'plot_bgcolor': 'plotly_dark'
    # }
    # data.append(data2)
    
    melted_df=df_copy.melt(id_vars=['Date'],value_vars=["count_orders",'MAF'],var_name='variables',value_name='plot_values').\
        reset_index()

    fig = px.line(melted_df, y=melted_df["plot_values"], x=melted_df["Date"],template="plotly_dark", color='variables')
    return fig
    # return {
    #     'data': data,
    #     'layout': {
    #         # 'uirevision': dataset,
    
    #         'legend': {'x': 0, 'y': 1}
    #     }
    # }


