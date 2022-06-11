from dash import Dash, dcc, html
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

# This stylesheet makes the buttons and table pretty.
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    # The memory store reverts to the default on every page refresh
    dcc.Store(id='session',storage_type='session'),

    html.Button(id="butt",n_clicks=0)

])

# Create two callback for every store.
for store in ('session'):

    # add a click to the appropriate store.
    @app.callback(Output(store, 'data'),
                  Input("butt", 'n_clicks'),
                  State(store, 'data'))
    def on_click(n_clicks, data):
        if n_clicks is None:
            # prevent the None callbacks is important with the store component.
            # you don't want to update the store for nothing.
            raise PreventUpdate

        # Give a default data dict with 0 clicks if there's no data.
        data = data or {'clicks': 0}
        
        data['clicks'] = data['clicks'] + 1
        return data




if __name__ == '__main__':
    app.run_server(debug=False, port=8077, threaded=True)