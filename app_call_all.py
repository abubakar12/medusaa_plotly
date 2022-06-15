import dash
import pandas as pd
from dash import html
from dash import dcc
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
from supporting_codes import call_backs_all
import plotly.io as pio
plotly_template = pio.templates["plotly_dark"]
plotly_template.layout
import time

#############################################################################
# Style modifications
#############################################################################
CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
}

TEXT_STYLE = {"textAlign": "center"}

DROPDOWN_STYLE = {"textAlign": "left"}

#############################################################################
# Content
#############################################################################
# Create drop-down selector and initial date picker

filter_bar = call_backs_all.option_selected

# # Container for raw data charts
basic_data = dbc.Row(
    [
        dbc.Col(
            call_backs_all.layout1,
            
            md=12,
        ),
    ]
)

# Container for periodic charts
baseline_data = dbc.Row(
    [
        dbc.Col(
            call_backs_all.layout2,
            md=6,
        ),
        dbc.Col(
            call_backs_all.layout7,
            md=6,
        ),
    ]
)

# Container for category survey charts
category_data = dbc.Row(
    [
        dbc.Col(
            call_backs_all.layout6,
            md=6,
        ),
        dbc.Col(
            call_backs_all.layout3,
            md=6,
        ),
    ]
)

category_data2 = dbc.Row(
    [
        dbc.Col(
            call_backs_all.layout5,
            md=6,
        ),
        dbc.Col(
            call_backs_all.layout4,
            md=6,
        ),
    ]
)





####################################################
# Layout Creation Section
####################################################
main_page = dbc.Container(
    [
        html.Hr(),
        html.H4("Medusa Product Table", style=TEXT_STYLE),
        # html.Hr(),
        # html.Hr(),
        # info_bar,
        html.Hr(),
        html.H4("Options Selected ", style=TEXT_STYLE),
        html.Hr(),
        filter_bar,
        html.Hr(),
        basic_data,
        html.Hr(),
        baseline_data,
        html.Hr(),
        # html.H5("Comparison of Data in Broad Category", style=TEXT_STYLE),
        html.Hr(),
        category_data,
        html.Hr(),
        category_data2,
        html.Hr(),
    ],
    style=CONTENT_STYLE,
)

#############################################################################
# Application parameters
#############################################################################
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.CYBORG],
)
app.config.suppress_callback_exceptions = True
app.title = "Federal Reserve Data Analysis"
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Multi-page selector callback - not really used, but left in for future use
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    # Left in because I'm not sure if this will be a muli-page app at some point

    # if pathname == "/market-sentiment":
    #     return volumes
    # else:
    return main_page


###################################################
# Server Run
###################################################
if __name__ == "__main__":

    app.run_server(
   debug=True,port=4204
      )
