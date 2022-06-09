from dash import dcc
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



df = tableau_file.copy()  # iris is a pandas DataFrame
df=df.groupby(["product_type","product_id"])['quantity']\
    .sum().reset_index().drop_duplicates(subset=["product_type","product_id"]).sort_values(by="quantity")

df["product_type"]=df["product_type"].astype(str)
df["product_id"]=df["product_id"].astype(str)
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server
    
app.layout = html.Div([
    # html.H4('Naive Cost'),
    html.Button("Toggle sort",id="toggle_sort",n_clicks=0),
    dcc.RadioItems(
        id='radio',
        options=df["product_type"].unique(),
        value=df["product_type"].unique()[0]
    ),
    dcc.Graph(id="graph")

])

@app.callback(
    Output("graph", "figure"), 
    Input("radio", "value"),
    Input("toggle_sort","n_clicks"),
    )
def display_(radio_value,toggle):

    df_copy=df[df["product_type"]==radio_value].drop("product_type",1)
    fig = px.bar(df_copy, y="product_id", x="quantity",orientation='h')
    if toggle%2==0:
        fig=fig.update_layout(yaxis={'categoryorder':'total ascending'})   
    else:
        print(toggle%2)
        fig=fig.update_layout(yaxis={'categoryorder':'total descending'})
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=False,port=3003)