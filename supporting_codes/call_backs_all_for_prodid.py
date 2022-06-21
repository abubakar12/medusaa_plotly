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
# import sqlalchemy
import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, \
    ServersideOutputTransform,callback

def decrypt(enc):
        key = '!!!!kfk9072p!!!!' #16 char for AES128
        iv =  'aaiissyysstteemm'.encode('utf-8') #16 char for AES128
        enc = base64.b64decode(enc)
        cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc),16)

def encrypt(data):
        key = '!!!!kfk9072p!!!!' #16 char for AES128
        iv =  'aaiissyysstteemm'.encode('utf-8') #16 char for AES128
        data= pad(data.encode(),16)
        cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
        return base64.b64encode(cipher.encrypt(data))
    
# link=f"/prod_id_page/?client_id={encrypt(data)}"

# params =urllib.parse.quote_plus('Driver={ODBC Driver 13 for SQL Server};'
#                                 'Server=tcp:shopifyai.database.windows.net,1433;'
#                                 'Database=ShopifyAI;'
#                                 'Uid=aiadmin;Pwd=kfk9072p!;'
#                                 'Encrypt=yes;'
#                                 'TrustServerCertificate=no;'
#                                 'Connection Timeout=30;')
# engine = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))

# client_id=50
# tableau_file=pd.read_sql(f"select Date,CustomerID,product_type,quantity,amount,price,product_id,sku from salesanalytics where cid = {client_id}",engine)
# max_date=tableau_file[tableau_file["quantity"].notnull()]["Date"].max()
# max_date=pd.to_datetime(max_date).date()



# df = tableau_file.copy()  # iris is a pandas DataFrame
# df["product_type"]=df["product_type"].astype(str)
# df["CustomerID"]=df["CustomerID"].astype(str)
# df["product_id"]=df["product_id"].astype(str)


###########################################################################################
#Gather all call backs
option_selected = dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("Total Revenue : "),
                            html.H6(id="tot_rev2"),
                        ],
                        color="light",
                    ),
                  
                ),
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("TOtal products sold: "),
                            html.H6(id="tot_prod_id"),
                        ],
                        color="success",
                    ),
                 
                ),
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("Unique Skus Sold: "),
                            html.H6(id="unq_sku_id"),
                        ],
                        color="success",
                    ),
                    
                ),
        
                dbc.Col(
                    html.Div([
                    html.H6("prod_type2"),
                    dcc.Dropdown(
                    id='prod_type2',
                    options=["prod1","prod2","prod3"],
                    value="prod1",)
                    # md=2,
                    ],id="container_prod_type",),
                ),
                dbc.Col(
                    html.Div([
                    html.H6("prod_id"),
                    dcc.Dropdown(
                    id='prod_id',)
                    # options=df["product_id"].unique(),
                    # value=df["product_id"].unique()[-1]),
                    # md=2,
                    ],id="container_prod_id",),
                ),
                dbc.Col(
                    html.Div([
                        html.H6("Days_prev"),
                        dcc.Dropdown(
                            id='days_prev2',
                            options=['30','60','90','ALL'],
                            value='ALL'
                        ),
                    # md=2,
                    ]),
                ),
                dbc.Col(
                    html.Div([
                    html.H6(id="selected_id"),
                    # md=2,
                    ]),width=True,
                ),
                
                dbc.Col(
                    html.Div([
                    html.H6(id="data_refresh_id"),
                    dbc.Button("Refresh Data",id="refresh_button",n_clicks=0,color="primary"),
                   
                    # dcc.Location(id='url_user2', refresh=False),
                    # md=2,
                    ]),width=True,
                ),
            ]
        ),
        # dbc.Row([html.Div(dcc.Link('Product_type page', href="/prod_type_page/")),
        #           html.Br(),
        #           html.Div(dcc.Link('Variant page', href="/variant_id_page/"))],id="basic_div_2")
        # dbc.Row(html.Div(dcc.Link('Category', href='/Category_page'))),
        ],fluid=True,
)

###############################################################################
#change dropdown values
def drop_down_updater(df):
    product_select=df["product_type"].unique()[-1]
    product_id_select=df[df["product_type"]==product_select]["product_id"].unique()[0]
    option_selected = html.Div([
                        html.H6("prod_type2"),
                        dcc.Dropdown(
                        id='prod_type2',
                        options=df["product_type"].unique(),
                        value=product_select),
                        # md=2,
                        ],id="container_prod_type",)
                  
    
    option_selected1 = html.Div([
                        html.H6("prod_id"),
                        dcc.Dropdown(
                        id='prod_id',
                        options=df["variant_id"].unique(),
                        value=product_id_select,
                        ),
                        # md=2,
                        ],id="container_prod_id",)

    return option_selected,option_selected1





#######################################################################################
@callback(
    Output("selected_id", "children"), 
    Output("prod_id", "options"),
    Input("prod_type2", "value"),
    Input("days_prev2","value"),
    Input('store-data2', 'data'),
    )
def revenue_tots(radio_value,days_prev2,data):
    df=data
    # df = pd.DataFrame(df)
    df=df[df["product_type"]==radio_value]
    val=[{'label': str(i), 'value': str(i)} for i in df["product_id"].unique()]
    output="Product Type : {}-Days Previous : {}".format(radio_value,days_prev2)
    return output,val

@callback(
    Output("prod_id", "value"),
    Input("prod_id", "options"), prevent_initial_call=True)
def set_cities_value(available_options):
    return available_options[0]['value']

######################################################################################################################



@callback(
    ServersideOutput("store-data2", "data"), 
    Output("data_refresh_id", "children"),
    Output("container_prod_type","children"),
    Output("container_prod_id","children"),
    Input("refresh_button","n_clicks"),
    Input("url","search"),
    State('container_prod_type', 'children'),
    State('container_prod_id', 'children'),
    State('store-data', 'data'),
    )
def data_refresh_code(refresh_button,params,container_prod_type,container_prod_id,data2):

        
        df=data2
        
        layout_update,layout_update1=drop_down_updater(df)
            



        
    
        return df,"Refreshed Date : {}".format(datetime.datetime.now().strftime('%y-%m-%d %a %H:%M:%S')),layout_update,layout_update1


       
###############################################################################################################
#Revenue dialog box
            



@callback(
    Output("tot_rev2", "children"), 
    Input("prod_type2", "value"),
    Input("prod_id","value"),
    Input("days_prev2","value"),
    Input('store-data2', 'data'), prevent_initial_call=True
    )
def revenue_tot(radio_value,prod_id,days_prev2,data):
    print("{}....".format(data),flush=True)
    df=data
    # df = pd.DataFrame(df)

    total_revenue=df.copy()
    # total_revenue=pd.DataFrame(df)
    df_copys=total_revenue[(total_revenue["product_type"]==radio_value)\
                           &(total_revenue["product_id"]==prod_id)]
    df_copys=df_copys[df_copys["quantity"]>0]
    
    if days_prev2=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        revenue=df_copy['amount'].sum()

        
    elif days_prev2=='60':
            df_copy=df_copys[df_copys["less_than_60"]==1]
            revenue=df_copy['amount'].sum()                 
            
    elif days_prev2=='90':
            df_copy=df_copys[df_copys["less_than_90"]==1]
            revenue=df_copy['amount'].sum()                       

            
    else:
            df_copy=df_copys.copy()
            revenue=df_copy['amount'].sum()                

            

    
    # arr=[revenue,tot_products,unique_skus]
    return revenue

    
@callback(
    Output("tot_prod_id", "children"),
    Input("prod_type2", "value"),
    Input("prod_id","value"),
    Input("days_prev2","value"),
    Input('store-data2', 'data'), prevent_initial_call=True
    )
def tot_prod_id(radio_value,prod_id,days_prev2,data):
    df=data
    # df = pd.DataFrame(df)

    total_revenue=df.copy()
    df_copys=total_revenue[(total_revenue["product_type"]==radio_value)\
                           &(total_revenue["product_id"]==prod_id)]
    df_copys=df_copys[df_copys["quantity"]>0]
    
    if days_prev2=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        tot_products=df_copy['quantity'].sum()
        
    elif days_prev2=='60':
            df_copy=df_copys[df_copys["less_than_60"]==1]
            tot_products=df_copy['quantity'].sum()
            
    elif days_prev2=='90':
            df_copy=df_copys[df_copys["less_than_90"]==1] 
            tot_products=df_copy['quantity'].sum()
            
    else:
            df_copy=df_copys.copy()
            tot_products=df_copy['quantity'].sum()

    
    return tot_products
        
@callback(
    Output("unq_sku_id", "children"),
    Input("prod_type2", "value"),
    Input("prod_id","value"),
    Input("days_prev2","value"),
    Input('store-data2', 'data'), prevent_initial_call=True
    )
def tot_unq_sku(radio_value,prod_id,days_prev2,data):
    df=data
    total_revenue=df.copy()
    # total_revenue=pd.DataFrame(df)
    df_copys=total_revenue[(total_revenue["product_type"]==radio_value)\
                           &(total_revenue["product_id"]==prod_id)]
    df_copys=df_copys[df_copys["quantity"]>0]
    
    if days_prev2=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        unique_skus=df_copy['sku'].nunique()

        
    elif days_prev2=='60':
            df_copy=df_copys[df_copys["less_than_60"]==1]
            unique_skus=df_copy['sku'].nunique()

            
    elif days_prev2=='90':
            df_copy=df_copys[df_copys["less_than_90"]==1]
            unique_skus=df_copy['sku'].nunique()                   

            
    else:
            df_copy=df_copys.copy()
            unique_skus=df_copy['sku'].nunique()                 

            
    
    # arr=[revenue,tot_products,unique_skus]
    return unique_skus

##############################################################################################
#product_sales.py

layout7 = html.Div([

    html.Br(),
    html.H6("Product Sales in Category"),
    html.Button("Toggle sort",id="toggle_sort",n_clicks=0),
    html.Br(),
    dcc.Graph(id="graph7_id")

])

@callback(
    Output("graph7_id", "figure"), 
    Input("prod_type2", "value"),
    Input("prod_id","value"),
    Input("days_prev2","value"),
    Input("toggle_sort","n_clicks"),  
    Input('store-data2', 'data'), prevent_initial_call=True
    )
def display_(radio_value,prod_id,day_prev,toggle,data):
    dfp=data
    # dfp = pd.DataFrame(dfp)

    df_copy=dfp[(dfp["product_type"]==radio_value)\
                               &(dfp["product_id"]==prod_id)].drop("product_type",1)
    df_copy=df_copy.groupby(['sku'])['quantity'].sum().reset_index()
    try:
        fig = px.bar(df_copy, y="sku", x="quantity",orientation='h',title='product_sales')
    except:
        fig = px.bar(df_copy, y="sku", x="quantity",orientation='h',title='product_sales')
    if toggle%2==0:
        fig=fig.update_layout(yaxis={'categoryorder':'total descending'},template="plotly_dark")   
    else:
        fig=fig.update_layout(yaxis={'categoryorder':'total ascending'},template="plotly_dark")
    
    return fig

#product_sales.py

prod_id_percent_sales = html.Div([

    dcc.Graph(id="graph_prod_id_%")

])

@callback(
    Output("graph_prod_id_%", "figure"), 
    Input("prod_type2", "value"),
    Input("days_prev2","value"),  
    Input('store-data2', 'data'), prevent_initial_call=True
    )
def variant_percent(radio_value,days_prev2,data):
    dfp=data
    # dfp = pd.DataFrame(dfp)

    df_copys=dfp[(dfp["product_type"]==radio_value)]
    if days_prev2=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy=df_copy.groupby(['product_id'])['quantity'].sum().reset_index()
        total=df_copy['quantity'].sum()
        df_copy["total"]=total
        df_copy["%_sales"]=(df_copy["quantity"]/df_copy["total"])*100

        
    elif days_prev2=='60':
            df_copy=df_copys[df_copys["less_than_60"]==1]
            df_copy=df_copy.groupby(['product_id'])['quantity'].sum().reset_index()
            total=df_copy['quantity'].sum()
            df_copy["total"]=total
            df_copy["%_sales"]=(df_copy["quantity"]/df_copy["total"])*100

            
    elif days_prev2=='90':
            df_copy=df_copys[df_copys["less_than_90"]==1]
            df_copy=df_copy.groupby(['product_id'])['quantity'].sum().reset_index()
            total=df_copy['quantity'].sum()
            df_copy["total"]=total
            df_copy["%_sales"]=(df_copy["quantity"]/df_copy["total"])*100                   

            
    else:
            df_copy=df_copys.copy()
            df_copy=df_copy.groupby(['product_id'])['quantity'].sum().reset_index()
            total=df_copy['quantity'].sum()
            df_copy["total"]=total
            df_copy["%_sales"]=(df_copy["quantity"]/df_copy["total"])*100  
            

    
    try:
        fig = px.pie(df_copy, values='%_sales', names='product_id', title='% product id  sales')
    except:
        fig = px.pie(df_copy, values='%_sales', names='product_id', title='% product id  sales')
    fig=fig.update_traces(textposition='inside')
    fig=fig.update_layout(template="plotly_dark",uniformtext_mode='hide')
    return fig

##########################################################################################
#new_customers.py



layout6 = html.Div([
    html.Br(),    
    dcc.Graph(id="graph6_id")

])

@callback(
    Output("graph6_id", "figure"), 
    Input("prod_type2", "value"),
    Input("prod_id","value"),
    Input("days_prev2","value"),
    Input('store-data2', 'data'), prevent_initial_call=True
    )
def new_customers(radio_value,prod_id,days_prev2,data):
    df=data
    # df = pd.DataFrame(df)
    
    df_copys=df[(df["product_type"]==radio_value)\
                               &(df["product_id"]==prod_id)].drop("product_type",1)
    
    if days_prev2=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
    elif days_prev2=='60':
            df_copy=df_copys[df_copys["less_than_60"]==1]
                
    elif days_prev2=='90':
            df_copy=df_copys[df_copys["less_than_90"]==1]
                
    else:
            df_copy=df_copys.copy()

      
   
    try:
        fig = px.bar(df_copy, y="total_customers", x="Date",title='new_customers')
    except:
        fig = px.bar(df_copy, y="total_customers", x="Date",title='new_customers')
    fig=fig.update_layout(template="plotly_dark")
    return fig


########################################################################################
#unique_customers.py


layout5 = html.Div([
    html.Br(),
    dcc.Graph(id="graph5_id")

])

@callback(
    Output("graph5_id", "figure"), 
    Input("prod_type2", "value"),
    Input("prod_id","value"),
    Input("days_prev2","value"),
    Input('store-data2', 'data'), prevent_initial_call=True
    )
def unique_customers(radio_value,prod_id,days_prev2,data):
    df=data
    # dfu = pd.DataFrame(dfu)
    
    dfu=df.copy()
    df_copys=dfu[(dfu["product_type"]==radio_value)\
                               &(dfu["product_id"]==prod_id)].drop("product_type",1)

    if days_prev2=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy=df_copy.groupby(["Date"])['CustomerID'].nunique().reset_index()
        df_copy=df_copy.rename(columns={"CustomerID":"unique_customer"})
    elif days_prev2=='60':
            df_copy=df_copys[df_copys["less_than_60"]==1]
            df_copy=df_copy.groupby(["Date"])['CustomerID'].nunique().reset_index()
            df_copy=df_copy.rename(columns={"CustomerID":"unique_customer"})
                
    elif days_prev2=='90':
            df_copy=df_copys[df_copys["less_than_90"]==1]
            df_copy=df_copy.groupby(["Date"])['CustomerID'].nunique().reset_index()
            df_copy=df_copy.rename(columns={"CustomerID":"unique_customer"})
                
    else:
            df_copy=df_copys.copy()       
            df_copy=df_copy.groupby(["Date"])['CustomerID'].nunique().reset_index()
            df_copy=df_copy.rename(columns={"CustomerID":"unique_customer"})
    try:
        fig = px.bar(df_copy, y="unique_customer", x="Date",title="UNIQUE_CUSTOMERS")
    except:
        fig = px.bar(df_copy, y="unique_customer", x="Date",title="UNIQUE_CUSTOMERS")
    fig=fig.update_layout(template="plotly_dark")
    
    return fig

###########################################################################################
#unique_dollar_graph.py
layout4 = html.Div([
    html.Br(),

    
    dcc.Graph(id="graph4_id")

])

@callback(
    Output("graph4_id", "figure"), 
    Input("prod_type2", "value"),
    Input("prod_id","value"),
    Input("days_prev2","value"),
    Input('store-data2', 'data'), prevent_initial_call=True
    )
def unique_dollar_graph(radio_value,prod_id,days_prev2,data):
    
    df=data
    # df = pd.DataFrame(df)

    
    df_copys=df[(df["product_type"]==radio_value)\
                               &(df["product_id"]==prod_id)].drop("product_type",1)
    
    if days_prev2=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy["sum_qty"]=df_copy.groupby(['Date'])['quantity'].transform(lambda x:x.sum())
        
        df_copy["sum_dollar_value"]=df_copy.groupby(['Date'])['amount'].transform(lambda x:x.sum())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
            

    elif days_prev2=='60':
        df_copy=df_copys[df_copys["less_than_60"]==1]
        df_copy["sum_qty"]=df_copy.groupby(['Date'])['quantity'].transform(lambda x:x.sum())
        
        df_copy["sum_dollar_value"]=df_copy.groupby(['Date'])['amount'].transform(lambda x:x.sum())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
         
    elif days_prev2=='90':
        df_copy=df_copys[df_copys["less_than_90"]==1]
        df_copy["sum_qty"]=df_copy.groupby(['Date'])['quantity'].transform(lambda x:x.sum())
        
        df_copy["sum_dollar_value"]=df_copy.groupby(['Date'])['amount'].transform(lambda x:x.sum())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
         
    else:
        df_copy=df_copys.copy()
        df_copy["sum_qty"]=df_copy.groupby(['Date'])['quantity'].transform(lambda x:x.sum())
      
        df_copy["sum_dollar_value"]=df_copy.groupby(['Date'])['amount'].transform(lambda x:x.sum())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
    
    df_copy["sum_qty"]=df_copy["sum_qty"].fillna(0)

    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add traces
    fig.add_trace(
        go.Scatter(name="sum_qty",x=df_copy["Date"], y=df_copy["sum_qty"]), secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(name="sum_dollar_value",x=df_copy["Date"], y=df_copy["sum_dollar_value"]),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(title_text="sales Vs Dollar graph")

    # Set x-axis title
    fig.update_xaxes(title_text="xaxis title")
    fig.layout.template="plotly_dark"
    # Set y-axes titles
    fig.update_yaxes(
        title_text="<b>primary</b>sum_qty", 
        secondary_y=False)
    fig.update_yaxes(
        title_text="<b>secondary</b>sum_dollar_value", 
        secondary_y=True)

    return fig


#######################################################################################################
#products_per_unq_customers.py
layout3 = html.Div([
    html.Br(),    
    dcc.Graph(id="graph3_id")

])

@callback(
    Output("graph3_id", "figure"), 
    Input("prod_type2", "value"),
    Input("prod_id","value"),
    Input("days_prev2","value"),
    Input('store-data2', 'data'), prevent_initial_call=True
    )
def products_per_unq_customers(radio_value,prod_id,days_prev2,data):
    df=data
    # df = pd.DataFrame(df)

    
    df_copys=df[(df["product_type"]==radio_value)\
                               &(df["product_id"]==prod_id)].drop("product_type",1)
    
    if days_prev2=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy["sum_qty"]=df_copy.groupby(['CustomerID'])['quantity'].transform(lambda x:x.sum())
        df_copy["avg_product_per_customer"]=df_copy.groupby(['CustomerID'])['sum_qty'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["CustomerID"])
            

    elif days_prev2=='60':
        df_copy=df_copys[df_copys["less_than_60"]==1]
        df_copy["sum_qty"]=df_copy.groupby(['CustomerID'])['quantity'].transform(lambda x:x.sum())
        df_copy["avg_product_per_customer"]=df_copy.groupby(['CustomerID'])['sum_qty'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["CustomerID"])
         
    elif days_prev2=='90':
        df_copy=df_copys[df_copys["less_than_90"]==1]
        df_copy["sum_qty"]=df_copy.groupby(['CustomerID'])['quantity'].transform(lambda x:x.sum())
        df_copy["avg_product_per_customer"]=df_copy.groupby(['CustomerID'])['sum_qty'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["CustomerID"])
         
    else:
        df_copy=df_copys.copy()
        df_copy["sum_qty"]=df_copy.groupby(['CustomerID'])['quantity'].transform(lambda x:x.sum())
        df_copy["avg_product_per_customer"]=df_copy.groupby(['CustomerID'])['sum_qty'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["CustomerID"])    
    try:
        fig = px.bar(df_copy, y="avg_product_per_customer", x="CustomerID",title="products_per_unq_customers")
    except:
        fig = px.bar(df_copy, y="avg_product_per_customer", x="CustomerID",title="products_per_unq_customers")
    fig=fig.update_layout(template="plotly_dark")
    return fig
###################################################################################################
#Count_and_MAF.py
layout2 = html.Div([
    html.Br(),
    html.H6("Moving Avg FIlter Window"),
    dcc.Slider(0, 10, 1,
               value=0,
               id='mov_avg_filt'),
    
    dcc.Graph(id="graph2_id")

])

@callback(
    Output("graph2_id", "figure"), 
    Input("prod_type2", "value"),
    Input("prod_id","value"),
    Input("days_prev2","value"),
    Input("mov_avg_filt","value"),
    Input('store-data2', 'data'), prevent_initial_call=True
    )
def Loess(radio_value,prod_id,days_prev2,roll,data):
    df=data
    # df = pd.DataFrame(df)

    
    df_copys=df[(df["product_type"]==radio_value)\
                               &(df["product_id"]==prod_id)].drop("product_type",1)
    
    if days_prev2=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy["count_orders"]=df_copy.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy=df_copy.drop_duplicates(subset=["Date","count_orders"])
        df_copy["MAF"]=df_copy['count_orders'].rolling(window=roll).mean()
            

    elif days_prev2=='60':
        df_copy=df_copys[df_copys["less_than_60"]==1]
        df_copy["count_orders"]=df_copy.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy=df_copy.drop_duplicates(subset=["Date","count_orders"])
        df_copy["MAF"]=df_copy['count_orders'].rolling(window=roll).mean()
        
        
         
    elif days_prev2=='90':
        df_copy=df_copys[df_copys["less_than_90"]==1]
        df_copy["count_orders"]=df_copy.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy=df_copy.drop_duplicates(subset=["Date","count_orders"])
        df_copy["MAF"]=df_copy['count_orders'].rolling(window=roll).mean()
        
        
         
    else:
        df_copy=df_copys.copy()
        df_copy["count_orders"]=df_copys.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy=df_copy.drop_duplicates(subset=["Date","count_orders"])
        df_copy["MAF"]=df_copy['count_orders'].rolling(window=roll).mean()

    
    melted_df=df_copy.melt(id_vars=['Date'],value_vars=["count_orders",'MAF'],var_name='variables',value_name='plot_values').\
        reset_index()
    # melted_df["Date"]=melted_df["Date"].dt.strftime('%d/%b/%y') 
    try:
        fig = px.line(melted_df, y="plot_values", x="Date", color='variables',title="Count_and_MAF",markers=True)
    except:
        fig = px.line(melted_df, y="plot_values", x="Date", color='variables',title="Count_and_MAF",markers=True)
    fig=fig.update_layout(template="plotly_dark")
    return fig



#################################################################################################################
#Average_selling_price.py
layout1 = html.Div([
    html.Br(),
    dcc.Graph(id="graph1_id")

])

@callback(
    Output("graph1_id", "figure"), 
    Input("prod_type2", "value"),
    Input("prod_id","value"),
    Input("days_prev2","value"),
    Input('store-data2', 'data'), prevent_initial_call=True
    )
def avg_selling_price(radio_value,prod_id,days_prev2,data):
    df=data
    # df = pd.DataFrame(df)

    df_copys=df[(df["product_type"]==radio_value)\
                               &(df["product_id"]==prod_id)]
    
    
    if days_prev2=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy["avg_selling_price"]=df_copy.groupby(['Date'])['price'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
            

    elif days_prev2=='60':
        df_copy=df_copys[df_copys["less_than_60"]==1]
        df_copy["avg_selling_price"]=df_copy.groupby(['Date'])['price'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
         
    elif days_prev2=='90':
        df_copy=df_copys[df_copys["less_than_90"]==1]
        df_copy["avg_selling_price"]=df_copy.groupby(['Date'])['price'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
        
         
    else:
        df_copy=df_copys.copy()
        df_copy["avg_selling_price"]=df_copy.groupby(['Date'])['price'].\
            transform(lambda x:x.mean())
      
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
    
    # df_copy["Date"]=df_copy["Date"].dt.strftime('%d/%b/%y') 
    try:    
        fig = px.line(df_copy, y="avg_selling_price", x="Date",title="Average_selling_price",markers=True)
    except:
        fig = px.line(df_copy, y="avg_selling_price", x="Date",title="Average_selling_price",markers=True)
    fig=fig.update_layout(template="plotly_dark")
    
    return fig