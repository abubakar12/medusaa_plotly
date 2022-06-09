from dash import dcc
import plotly.express as px
import pandas as pd
from dash import Dash,dcc, html, Input, Output, callback
tableau_file=pd.read_csv(r"C:\Users\hp\Desktop\medusaa_plotly\opt_tableau.csv")
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import json
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go



df = tableau_file.copy()  # iris is a pandas DataFrame
df=df.groupby("SKU")[['Opt Cost','naive_cost']]\
    .sum().reset_index().drop_duplicates(subset="SKU").sort_values(by="naive_cost")
   
app = Dash(__name__) 
    
app.layout = html.Div([
    html.H4('Naive Cost'),
    html.P("Select red line's Y-axis:"),
    dcc.RadioItems(
        id='radio',
        options=[df["SKU"].unique()],
        value='Secondary'
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("radio", "value"))
def display_(radio_value):

    df_copy=df[df["SKU"]==radio_value]

    return fig


app.run_server(debug=True)
