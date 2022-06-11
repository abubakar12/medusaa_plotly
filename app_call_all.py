import dash
import pandas as pd
from dash import html
from dash import dcc
from dash.dependencies import Input, Output,State
import dash_bootstrap_components as dbc
# from datetime import date
# from supporting_codes import Average_selling_price
# from supporting_codes import Count_and_MAF
# from supporting_codes import new_customers_daywise
# from supporting_codes import products_per_unq_customers
# from supporting_codes import unique_customers_daywise
# from supporting_codes import Unit_dollar_graph
# from supporting_codes import product_sales
# from supporting_codes import layout_configs as lc
from supporting_codes import call_backs_all
import plotly.io as pio
plotly_template = pio.templates["plotly_dark"]
plotly_template.layout


# ,\
#     Count_and_MAF,new_customers_daywise,product_sales,products_per_unq_customers,\
#         unique_customers_daywise,Unit_dollar_graph


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
# arrays=call_backs_all.array
# revenue,tot_products,unique_skus=arrays.value
# Info Bar
info_bar=call_backs_all.info_bars
# info_bar = html.Div(
#         dbc.Row(
#             [
#                 dbc.Col(
#                     dbc.Alert(
#                         [
#                             html.H6("Total Revenue : "),
#                             html.H6(call_backs_all.array.children[0].data[0]),
#                         ],
#                         color="light",
#                     ),
#                     md=2,
#                 ),
#                 dbc.Col(
#                     dbc.Alert(
#                         [
#                             html.H6("TOtal products sold: "),
#                             html.H6(call_backs_all.array.children[0].data[1]),
#                         ],
#                         color="success",
#                     ),
#                     md=2,
#                 ),
#                 dbc.Col(
#                     dbc.Alert(
#                         [
#                             html.H6("Unique Skus Sold: "),
#                             html.H6(call_backs_all.array.children[0].data[2]),
#                         ],
#                         color="success",
#                     ),
#                     md=2,
#                 ),
#             ]
#         )
# )

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
main_page = html.Div(
    [
        html.Hr(),
        html.H4("Medusa Product Table", style=TEXT_STYLE),
        html.Hr(),
        # report_select,
        html.Hr(),
        info_bar,
        html.Hr(),
        basic_data,
        html.Hr(),
        baseline_data,
        html.Hr(),
        html.H5("Comparison of Data in Broad Category", style=TEXT_STYLE),
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
   debug=True,port=3204
      )
