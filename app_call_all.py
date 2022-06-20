import dash
import pandas as pd
from dash import html
from dash import dcc
from dash_extensions.enrich import DashProxy, Output, Input, State, ServersideOutput, html, dcc, \
    ServersideOutputTransform,callback
import dash_bootstrap_components as dbc
from supporting_codes import call_backs_all
from supporting_codes import call_backs_all_for_prodid
from supporting_codes import call_backs_all_for_Variant
import plotly.io as pio
plotly_template = pio.templates["plotly_dark"]
plotly_template.layout
import time
import base64 
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

# data = "encrypt this"

def encrypt(data):
        key = '!!!!kfk9072p!!!!' #16 char for AES128
        iv =  'aaiissyysstteemm'.encode('utf-8') #16 char for AES128
        data= pad(data.encode(),16)
        cipher = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
        return base64.b64encode(cipher.encrypt(data))
    
# encrypted = encrypt(data)

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


#############################################################################
# Content prod_id
#############################################################################
# Create drop-down selector and initial date picker

filter_bar_id = call_backs_all_for_prodid.option_selected

# # Container for raw data charts
basic_data_id = dbc.Row(
    [
        dbc.Col(
            call_backs_all_for_prodid.layout1,
            
            md=6,
        ),
        dbc.Col(
            call_backs_all_for_prodid.prod_id_percent_sales,
            
            md=6,
        ),
    ]
)

# Container for periodic charts
baseline_data_id = dbc.Row(
    [
        dbc.Col(
            call_backs_all_for_prodid.layout2,
            md=6,
        ),
        dbc.Col(
            call_backs_all_for_prodid.layout7,
            md=6,
        ),
    ]
)

# Container for category survey charts
category_data_id = dbc.Row(
    [
        dbc.Col(
            call_backs_all_for_prodid.layout6,
            md=6,
        ),
        dbc.Col(
            call_backs_all_for_prodid.layout3,
            md=6,
        ),
    ]
)

category_data2_id = dbc.Row(
    [
        dbc.Col(
            call_backs_all_for_prodid.layout5,
            md=6,
        ),
        dbc.Col(
            call_backs_all_for_prodid.layout4,
            md=6,
        ),
    ]
)


####################################################
# Layout Creation Section
####################################################
main_page_id = dbc.Container(
    [   html.Div(dcc.Loading(dcc.Store(id="store-data2", storage_type='session'), fullscreen=True, type="dot")),
        html.Hr(),
        html.H4("Medusa Product Table", style=TEXT_STYLE),
        # html.Hr(),
        # html.Hr(),
        # info_bar,
        html.Hr(),
        html.H4("Options Selected ", style=TEXT_STYLE),
        html.Hr(),
        filter_bar_id,
        html.Hr(),
        basic_data_id,
        html.Hr(),
        baseline_data_id,
        html.Hr(),
        # html.H5("Comparison of Data in Broad Category", style=TEXT_STYLE),
        html.Hr(),
        category_data_id,
        html.Hr(),
        category_data2_id,
        html.Hr(),
    ],
    style=CONTENT_STYLE,
)



#############################################################################


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


#####################################################Variant _age#######################################
#############################################################################
# Content prod_id
#############################################################################
# Create drop-down selector and initial date picker

filter_bar_var = call_backs_all_for_Variant.option_selected

# # Container for raw data charts
basic_data_var = dbc.Row(
    [
        dbc.Col(
            call_backs_all_for_Variant.layout1,
            
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 79d96f782ee434188c7de23372bb2979e0bd437d
            md=6,
        ),
        
        dbc.Col(
            call_backs_all_for_Variant.var_percent_sales,
            
            md=6,
<<<<<<< HEAD
=======
=======
            md=12,
>>>>>>> c9713e7ef9f6e4f87027f0fe5fc820f91db233ba
>>>>>>> 79d96f782ee434188c7de23372bb2979e0bd437d
        ),
    ]
)

# Container for periodic charts
baseline_data_var = dbc.Row(
    [
        dbc.Col(
            call_backs_all_for_Variant.layout2,
            md=6,
        ),
        dbc.Col(
            call_backs_all_for_Variant.layout7,
            md=6,
        ),
    ]
)

# Container for category survey charts
category_data_var = dbc.Row(
    [
        dbc.Col(
            call_backs_all_for_Variant.layout6,
            md=6,
        ),
        dbc.Col(
            call_backs_all_for_Variant.layout3,
            md=6,
        ),
    ]
)

category_data2_var = dbc.Row(
    [
        dbc.Col(
            call_backs_all_for_Variant.layout5,
            md=6,
        ),
        dbc.Col(
            call_backs_all_for_Variant.layout4,
            md=6,
        ),
    ]
)


####################################################
# Layout Creation Section
####################################################
main_page_var = dbc.Container(
<<<<<<< HEAD
    [   
=======
    [   html.Div(dcc.Loading(dcc.Store(id="store-data2", storage_type='session'), fullscreen=True, type="dot")),
        html.Div(dcc.Loading(dcc.Store(id="store-data3", storage_type='session'), fullscreen=True, type="dot")),
>>>>>>> 79d96f782ee434188c7de23372bb2979e0bd437d
        html.Hr(),
        html.H4("Medusa Product Table", style=TEXT_STYLE),
        # html.Hr(),
        # html.Hr(),
        # info_bar,
        html.Hr(),
        html.H4("Options Selected ", style=TEXT_STYLE),
        html.Hr(),
        filter_bar_var,
        html.Hr(),
        basic_data_var,
        html.Hr(),
        baseline_data_var,
        html.Hr(),
        # html.H5("Comparison of Data in Broad Category", style=TEXT_STYLE),
        html.Hr(),
        category_data_var,
        html.Hr(),
        category_data2_var,
        html.Hr(),
    ],
    style=CONTENT_STYLE,
)
#############################################################################
# Application parameters
#############################################################################
<<<<<<< HEAD
style_link={ "width":"300px","margin": "0 auto","font-size": "1.2rem","font-family": "sans-serif",\
            "color":"white","border-style": "solid",}
=======

>>>>>>> 79d96f782ee434188c7de23372bb2979e0bd437d
app = DashProxy(__name__,transforms=[ServersideOutputTransform()],\
                external_stylesheets=[dbc.themes.CYBORG],suppress_callback_exceptions=True,)
app.title = "Shopify Data Analysis"
app.layout = html.Div(
<<<<<<< HEAD
    [dcc.Store(id='store-data',storage_type='session'),
     dcc.Store(id='client-id-store', storage_type='session'),
     dcc.Store(id="store-data2", storage_type='session'),
     dcc.Store(id="store-data3", storage_type='session'),
     dcc.Location(id="url", refresh=True), 
     dbc.Row([dbc.Col(dbc.Alert(dcc.Link('Product_type page', href="/",className="alert-link"))),
             dbc.Col(dbc.Alert(dcc.Link('Product id  page', href="/prod_id_page/",className="alert-link"))),
             dbc.Col(dbc.Alert(dcc.Link('Variant page', href="/variant_id_page/",className="alert-link")))]),
     dbc.Row(html.Div(id="page-content"),)
     ]
=======
    [dcc.Store(id='store-data', data=[1,2,3,4], storage_type='session'),
     dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
>>>>>>> 79d96f782ee434188c7de23372bb2979e0bd437d
)

# Multi-page selector callback - not really used, but left in for future use
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    # Left in because I'm not sure if this will be a muli-page app at some point
    # link=f"/prod_id_page/?client_id={}"
    if pathname == "/prod_id_page/":
        return main_page_id
    elif pathname == "/variant_id_page/":
        return  main_page_var
    else:
        return main_page


###################################################
# Server Run
###################################################
app.config['suppress_callback_exceptions'] = True
if __name__ == "__main__":

    app.run_server(
<<<<<<< HEAD
   debug=True,port=6504
=======
   debug=True,port=6204
>>>>>>> 79d96f782ee434188c7de23372bb2979e0bd437d
      )
