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



from dash import dcc
import plotly.express as px

df = tableau_file.copy()  # iris is a pandas DataFrame
df=df.groupby("SKU")[['Opt Cost','naive_cost']]\
    .sum().reset_index().drop_duplicates(subset="SKU").sort_values(by="naive_cost")


fig = go.Figure(data=[
    go.Bar(name="graph",x=df["SKU"], y=df["naive_cost"]),
    go.Bar(name="graph1",x=df["SKU"], y=df["Opt Cost"])
])



fig.update_layout(barmode='stack')



app = Dash(__name__)


app.layout = html.Div([
    html.H4('Interactive data-scaling using the secondary axis'),
    html.P("Select red line's Y-axis:"),
    dcc.RadioItems(
        id='radio',
        options=['Primary', 'Secondary'],
        value='Secondary'
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"), 
    Input("radio", "value"))
def display_(radio_value):

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Bar(name="graph",x=df["SKU"], y=df["naive_cost"],opacity=1,width=0.8), secondary_y=False,
    )

    fig.add_trace(
        go.Bar(name="graph1",x=df["SKU"], y=df["Opt Cost"],opacity=1,width=0.5),
        secondary_y=radio_value == 'Secondary'
    )

    # Add figure title
    fig.update_layout(title_text="Double Y Axis Example")

    # Set x-axis title
    fig.update_xaxes(title_text="xaxis title")

    # Set y-axes titles
    fig.update_yaxes(
        title_text="<b>primary</b> yaxis title", 
        secondary_y=False)
    # fig.update_yaxes(
    #     title_text="<b>secondary</b> yaxis title", 
    #     secondary_y=True)

    return fig


app.run_server(debug=True,port=3003)
