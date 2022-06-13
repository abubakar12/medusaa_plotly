import numpy as np
import plotly.express as px
import pandas as pd
from dash import dcc, html, Input, Output, callback
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default='browser'
from datetime import date, timedelta
import dash_bootstrap_components as dbc

tableau_file=pd.read_csv(r"C:\Users\hp\Desktop\medusaa_plotly\sample_data.csv",\
                         usecols=["Date",'Year','Month',"Day",'CustomerID','product_type','quantity','amount','price',"product_id",'sku'])
max_date=pd.to_datetime("2-18-2022",format="%m-%d-%Y")
max_date=pd.to_datetime(max_date).date()
# max_date=date.today()


df = tableau_file.copy()  # iris is a pandas DataFrame
df["product_type"]=df["product_type"].astype(str)
df["CustomerID"]=df["CustomerID"].astype(str)

df["Date"]=pd.to_datetime(df["Date"],format="%Y-%m-%d")
############################################for New customer############################
less_than_current_date=[]
for datee in df["Date"].unique():
    datee=pd.to_datetime(datee).strftime('%Y-%m-%d')
    datee=pd.to_datetime(datee,format="%Y-%m-%d").date()
    if (datee<=max_date):
        less_than_current_date.append(datee)
        
num_new_customers={}   
new_customers=[]
for datee in less_than_current_date:
    print("date : {} ".format(str(datee)))
    
    customers=df[df["Date"]==np.datetime64(datee)]["CustomerID"].unique()
    unique_customer_date=np.setdiff1d(customers,new_customers)
    num_new_customers[str(datee)]=len(list(unique_customer_date))
    new_customers=np.concatenate((new_customers, unique_customer_date), axis=None)
    
new_customers_tot=pd.DataFrame(num_new_customers.items(),columns=["Date","total_customers"])    
new_customers_tot["Date"]=pd.to_datetime(new_customers_tot["Date"],format="%Y-%m-%d")


df=pd.merge(df,new_customers_tot,on=["Date"],how="left")
############################################for New customer############################

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

dfu=df.copy()

###########################################################################################
#Gather all call backs
option_selected = dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("Total Revenue : "),
                            html.H6(id="tot_rev"),
                        ],
                        color="light",
                    ),
                    md=2,
                ),
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("TOtal products sold: "),
                            html.H6(id="tot_prod"),
                        ],
                        color="success",
                    ),
                    md=2,
                ),
                dbc.Col(
                    dbc.Alert(
                        [
                            html.H6("Unique Skus Sold: "),
                            html.H6(id="unq_sku"),
                        ],
                        color="success",
                    ),
                    md=2,
                ),
        
                dbc.Col(
                    html.Div([
                    html.H6("prod_type"),
                    dcc.Dropdown(
                    id='prod_type',
                    options=df["product_type"].unique(),
                    value=df["product_type"].unique()[-1]),
                    # md=2,
                    ]),md=2,
                ),
                dbc.Col(
                    html.Div([
                        html.H6("Days_prev"),
                        dcc.Dropdown(
                            id='days_prev',
                            options=['30','60','90','ALL'],
                            value='ALL'
                        ),
                    # md=2,
                    ]),md=2,
                ),
                dbc.Col(
                    html.Div([
                    html.H5(id="selected"),
                    # md=2,
                    ]),md=2,width=True,
                ),
            ]
        )
        ],fluid=True,
)


@callback(
    Output("selected", "children"), 
    Input("prod_type", "value"),
    Input("days_prev","value"),
    )
def revenue_tots(radio_value,days_prev):

    output="Product Type : {} -- Days Previous : {}".format(radio_value,days_prev)
    return output
###############################################################################################################
#Revenue dialog box
            
total_revenue=df.\
    drop_duplicates(["product_type","Date",'sku'])

# info_bars = html.Div(
#         dbc.Row(
#             [
#                 dbc.Col(
#                     dbc.Alert(
#                         [
#                             html.H6("Total Revenue : "),
#                             html.H6(id="tot_rev"),
#                         ],
#                         color="light",
#                     ),
#                     md=2,
#                 ),
#                 dbc.Col(
#                     dbc.Alert(
#                         [
#                             html.H6("TOtal products sold: "),
#                             html.H6(id="tot_prod"),
#                         ],
#                         color="success",
#                     ),
#                     md=2,
#                 ),
#                 dbc.Col(
#                     dbc.Alert(
#                         [
#                             html.H6("Unique Skus Sold: "),
#                             html.H6(id="unq_sku"),
#                         ],
#                         color="success",
#                     ),
#                     md=2,
#                 ),
#             ]
#         )
# )




@callback(
    Output("tot_rev", "children"), 
    Input("prod_type", "value"),
    Input("days_prev","value"),
    )
def revenue_tot(radio_value,days_prev):

    df_copys=total_revenue[total_revenue["product_type"]==radio_value]
    df_copys=df_copys[df_copys["quantity"]>0]
    
    if days_prev=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy["revenue"]=df_copy.groupby(['Date','product_type'])['amount'].\
                    transform(lambda x:x.sum())
        df_copy=df_copy.\
            drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
        
    elif days_prev=='60':
            df_copy=df_copys[df_copys["less_than_60"]==1]
            df_copy["revenue"]=df_copy.groupby(['Date','product_type'])['amount'].\
                                transform(lambda x:x.sum())                  
            df_copy=df_copy.\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
            
    elif days_prev=='90':
            df_copy=df_copys[df_copys["less_than_90"]==1]
            df_copy["revenue"]=df_copy.groupby(['Date','product_type'])['amount'].\
                    transform(lambda x:x.sum())                       
            df_copy=df_copy.\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
            
    else:
            df_copy=df_copys.copy()
            df_copy["revenue"]=df_copy.groupby(['Date','product_type'])['amount'].\
                                transform(lambda x:x.sum())                 
            df_copy=df_copy.\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
            
    revenue=df_copy["revenue"].sum()
    
    # arr=[revenue,tot_products,unique_skus]
    return revenue

    
@callback(
    Output("tot_prod", "children"),
    Input("prod_type", "value"),
    Input("days_prev","value"),
    )
def tot_prod(radio_value,days_prev):

    df_copys=total_revenue[total_revenue["product_type"]==radio_value]
    df_copys=df_copys[df_copys["quantity"]>0]
    
    if days_prev=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy["total_products"]=df_copy.groupby(['Date','product_type'])['quantity'].\
                    transform(lambda x:x.sum())
        df_copy=df_copy.\
            drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
        
    elif days_prev=='60':
            df_copy=df_copys[df_copys["less_than_60"]==1]
            df_copy["total_products"]=df_copy.groupby(['Date','product_type'])['quantity'].\
                        transform(lambda x:x.sum())                    
            df_copy=df_copy.\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
            
    elif days_prev=='90':
            df_copy=df_copys[df_copys["less_than_90"]==1] 
            df_copy["total_products"]=df_copy.groupby(['Date','product_type'])['quantity'].\
                        transform(lambda x:x.sum())                      
            df_copy=df_copy.\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
            
    else:
            df_copy=df_copys.copy()
            df_copy["total_products"]=df_copy.groupby(['Date','product_type'])['quantity'].\
                        transform(lambda x:x.sum())                    
            df_copy=df_copy.\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
            
    tot_products=df_copy["total_products"].sum()

    
    # arr=[revenue,tot_products,unique_skus]
    return tot_products
        
@callback(
    Output("unq_sku", "children"),
    Input("prod_type", "value"),
    Input("days_prev","value"),
    )
def tot_unq_sku(radio_value,days_prev):

    df_copys=total_revenue[total_revenue["product_type"]==radio_value]
    df_copys=df_copys[df_copys["quantity"]>0]
    
    if days_prev=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy["unique_sku"]=df_copy.groupby(['product_type'])['sku'].\
                    transform(lambda x:x.nunique())
        df_copy=df_copy.\
            drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
        
    elif days_prev=='60':
            df_copy=df_copys[df_copys["less_than_60"]==1]
            df_copy["unique_sku"]=df_copy.groupby(['product_type'])['sku'].\
                        transform(lambda x:x.nunique())
            df_copy=df_copy.\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
            
    elif days_prev=='90':
            df_copy=df_copys[df_copys["less_than_90"]==1]
            df_copy["unique_sku"]=df_copy.groupby(['product_type'])['sku'].\
                        transform(lambda x:x.nunique())                   
            df_copy=df_copy.\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
            
    else:
            df_copy=df_copys.copy()
            df_copy["unique_sku"]=df_copy.groupby(['product_type'])['sku'].\
                        transform(lambda x:x.nunique())                  
            df_copy=df_copy.\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
            
    unique_skus=df_copy["unique_sku"].unique()[0]
    
    # arr=[revenue,tot_products,unique_skus]
    return unique_skus

##############################################################################################
#product_sales.py
dfp=df.copy()
dfp=dfp.groupby(["product_type","product_id"])['quantity']\
    .sum().reset_index().drop_duplicates(subset=["product_type","product_id"]).sort_values(by="quantity",ascending=False)
dfp["product_type"]=dfp["product_type"].astype(str)
dfp["product_id"]=dfp["product_id"].astype(str)
dfp["quantity"]=dfp["quantity"].astype(int)
layout7 = html.Div([

    # html.Br(),
    # html.H1("prod_type"),
    # dcc.RadioItems(
    #     id='prod_type',
    #     options=df["product_type"].unique(),
    #     value=df["product_type"].unique()[-1]
    # ),
    # html.Br(),
    # html.H1("Days_prev"),
    # dcc.RadioItems(
    #     id='days_prev',
    #     options=['30','60','90','ALL'],
    #     value='ALL'
    # ),
    html.Br(),
    html.H6("Product Sales in Category"),
    html.Button("Toggle sort",id="toggle_sort",n_clicks=0),
    html.Br(),
    dcc.Graph(id="graph7")

])

@callback(
    Output("graph7", "figure"), 
    Input("prod_type", "value"),
    Input("days_prev","value"),
    Input("toggle_sort","n_clicks"),   
    )
def display_(radio_value,day_prev,toggle):

    df_copy=dfp[dfp["product_type"]==radio_value].drop("product_type",1)
    try:
        fig = px.bar(df_copy, y="product_id", x="quantity",orientation='h',title='product_sales')
    except:
        fig = px.bar(df_copy, y="product_id", x="quantity",orientation='h',title='product_sales')
    if toggle%2==0:
        fig=fig.update_layout(yaxis={'categoryorder':'total descending'},template="plotly_dark")   
    else:
        fig=fig.update_layout(yaxis={'categoryorder':'total ascending'},template="plotly_dark")
    
    return fig


##########################################################################################
#new_customers.py



layout6 = html.Div([
    html.Br(),    
    dcc.Graph(id="graph6")

])

@callback(
    Output("graph6", "figure"), 
    Input("prod_type", "value"),
    Input("days_prev","value"),
    )
def new_customers(radio_value,days_prev):

    df_copys=df[df["product_type"]==radio_value].drop("product_type",1)
    
    if days_prev=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1].\
            drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
    elif days_prev=='60':
            df_copy=df_copys[df_copys["less_than_60"]==1].\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
                
    elif days_prev=='90':
            df_copy=df_copys[df_copys["less_than_90"]==1].\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
                
    else:
            df_copy=df_copys.copy()
            df_copy=df_copy.drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
            
    try:
        fig = px.bar(df_copy, y="total_customers", x="Date",title='new_customers')
    except:
        fig = px.bar(df_copy, y="total_customers", x="Date",title='new_customers')
    fig=fig.update_layout(template="plotly_dark")
    return fig


########################################################################################
#unique_customers.py
dfu["unique_customer"]=dfu.groupby(["Date",'product_type'])['CustomerID'].\
        transform(lambda x:x.nunique())
dfu=dfu.drop_duplicates(subset=["Date",'product_type'])

layout5 = html.Div([
    html.Br(),
    dcc.Graph(id="graph5")

])

@callback(
    Output("graph5", "figure"), 
    Input("prod_type", "value"),
    Input("days_prev","value"),
    )
def unique_customers(radio_value,days_prev):

    df_copys=dfu[dfu["product_type"]==radio_value].drop("product_type",1)

    
    if days_prev=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1].\
            drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
    elif days_prev=='60':
            df_copy=df_copys[df_copys["less_than_60"]==1].\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
                
    elif days_prev=='90':
            df_copy=df_copys[df_copys["less_than_90"]==1].\
                drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
                
    else:
            df_copy=df_copys.copy()       
            df_copy=df_copy.drop(["less_than_30","less_than_60","less_than_90"],1).drop_duplicates(subset=["Date"])
            
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

    
    dcc.Graph(id="graph4")

])

@callback(
    Output("graph4", "figure"), 
    Input("prod_type", "value"),
    Input("days_prev","value"),
    )
def unique_dollar_graph(radio_value,days_prev):

    df_copys=df[df["product_type"]==radio_value].drop("product_type",1)
    
    if days_prev=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy["sum_qty"]=df_copy.groupby(['Date'])['quantity'].transform(lambda x:x.sum())
        df_copy["sum_qty"]=df_copy.groupby(['Date'])['quantity'].transform(lambda x:x.sum())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        df_copy["sum_dollar_value"]=df_copy.groupby(['Date'])['amount'].transform(lambda x:x.sum())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
            

    elif days_prev=='60':
        df_copy=df_copys[df_copys["less_than_60"]==1]
        df_copy["sum_qty"]=df_copy.groupby(['Date'])['quantity'].transform(lambda x:x.sum())
        df_copy["avg_product_per_customer"]=df_copy.groupby(['Date'])['sum_qty'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        df_copy["sum_dollar_value"]=df_copy.groupby(['Date'])['amount'].transform(lambda x:x.sum())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
         
    elif days_prev=='90':
        df_copy=df_copys[df_copys["less_than_90"]==1]
        df_copy["sum_qty"]=df_copy.groupby(['Date'])['quantity'].transform(lambda x:x.sum())
        df_copy["avg_product_per_customer"]=df_copy.groupby(['Date'])['sum_qty'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        df_copy["sum_dollar_value"]=df_copy.groupby(['Date'])['amount'].transform(lambda x:x.sum())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
         
    else:
        df_copy=df_copys.copy()
        df_copy["sum_qty"]=df_copy.groupby(['Date'])['quantity'].transform(lambda x:x.sum())
        df_copy=df_copy.drop_duplicates(subset=["Date"])    
        
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
    dcc.Graph(id="graph3")

])

@callback(
    Output("graph3", "figure"), 
    Input("prod_type", "value"),
    Input("days_prev","value"),
    )
def products_per_unq_customers(radio_value,days_prev):

    df_copys=df[df["product_type"]==radio_value].drop("product_type",1)
    
    if days_prev=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy["sum_qty"]=df_copy.groupby(['CustomerID'])['quantity'].transform(lambda x:x.sum())
        df_copy["avg_product_per_customer"]=df_copy.groupby(['CustomerID'])['sum_qty'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["CustomerID"])
            

    elif days_prev=='60':
        df_copy=df_copys[df_copys["less_than_60"]==1]
        df_copy["sum_qty"]=df_copy.groupby(['CustomerID'])['quantity'].transform(lambda x:x.sum())
        df_copy["avg_product_per_customer"]=df_copy.groupby(['CustomerID'])['sum_qty'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["CustomerID"])
         
    elif days_prev=='90':
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
    
    dcc.Graph(id="graph2")

])

@callback(
    Output("graph2", "figure"), 
    Input("prod_type", "value"),
    Input("days_prev","value"),
    Input("mov_avg_filt","value"),
    )
def Loess(radio_value,days_prev,roll):

    df_copys=df[df["product_type"]==radio_value].drop("product_type",1)
    
    if days_prev=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy["count_orders"]=df_copy.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy["MAF"]=df_copy.groupby(['Date'])['count_orders'].\
            transform(lambda x:x.rolling(window=roll).mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
            

    elif days_prev=='60':
        df_copy=df_copys[df_copys["less_than_60"]==1]
        df_copy["count_orders"]=df_copy.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy["MAF"]=df_copy.groupby(['Date'])['count_orders'].\
                transform(lambda x:x.rolling(window=roll).mean())
                
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
         
    elif days_prev=='90':
        df_copy=df_copys[df_copys["less_than_90"]==1]
        df_copy["count_orders"]=df_copy.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy["MAF"]=df_copy.groupby(['Date'])['count_orders'].\
                transform(lambda x:x.rolling(window=roll).mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
        
         
    else:
        df_copy=df_copys.copy()
        df_copy["count_orders"]=df_copys.groupby(['Date'])['quantity'].\
            transform(lambda x:x.count())
        df_copy["MAF"]=df_copy.groupby(['Date'])['count_orders'].\
                transform(lambda x:x.rolling(window=roll).mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])

    
    melted_df=df_copy.melt(id_vars=['Date'],value_vars=["count_orders",'MAF'],var_name='variables',value_name='plot_values').\
        reset_index()
    try:
        fig = px.line(melted_df, y=melted_df["plot_values"], x=melted_df["Date"], color='variables',title="Count_and_MAF")
    except:
        fig = px.line(melted_df, y=melted_df["plot_values"], x=melted_df["Date"], color='variables',title="Count_and_MAF")
    fig=fig.update_layout(template="plotly_dark")
    return fig



#################################################################################################################
#Average_selling_price.py
layout1 = html.Div([
    html.Br(),
    dcc.Graph(id="graph1")

])

@callback(
    Output("graph1", "figure"), 
    Input("prod_type", "value"),
    Input("days_prev","value"),
    )
def avg_selling_price(radio_value,days_prev):

    df_copys=df[df["product_type"]==radio_value]
    
    if days_prev=='30':
        df_copy=df_copys[df_copys["less_than_30"]==1]
        df_copy["avg_selling_price"]=df_copy.groupby(['Date','price'])['price'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
            

    elif days_prev=='60':
        df_copy=df_copys[df_copys["less_than_60"]==1]
        df_copy["avg_selling_price"]=df_copy.groupby(['Date','price'])['price'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
         
    elif days_prev=='90':
        df_copy=df_copys[df_copys["less_than_90"]==1]
        df_copy["avg_selling_price"]=df_copy.groupby(['Date','price'])['price'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
        
        
         
    else:
        df_copy=df_copys.copy()
        df_copy["avg_selling_price"]=df_copy.groupby(['Date','price'])['price'].\
            transform(lambda x:x.mean())
        df_copy=df_copy.drop_duplicates(subset=["Date"])
        
    try:    
        fig = px.line(df_copy, y="avg_selling_price", x="Date",title="Average_selling_price")
    except:
        fig = px.line(df_copy, y="avg_selling_price", x="Date",title="Average_selling_price")
    fig=fig.update_layout(template="plotly_dark")
    
    return fig