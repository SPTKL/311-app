


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import requests
import json
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
r = json.loads(requests.get('https://cwhong.carto.com/api/v2/sql?q=select distinct agency from public.table_311_1').content)
agency_options = [{'label':i['agency'], 'value':i['agency']} for i in r['rows']]

app.layout = html.Div([
    dcc.Dropdown(
        id='agency-dropdown',
        options=agency_options,
        value='TLC'
    ), 
    html.Div(id='map-area')
])


@app.callback(
    dash.dependencies.Output('map-area', 'children'),
    [dash.dependencies.Input('agency-dropdown', 'value')])
def update_output(agency):
    r = json.loads(requests.get(f"https://cwhong.carto.com/api/v2/sql?q=select * from public.table_311_1 where agency = '{agency}'").content)['rows']
    return html.Div([
    dcc.Graph(
        id='agency-plot',
        figure={
            'data': [{
                'type': 'scattermapbox',
                'lon': [i['longitude'] for i in r],
                'lat': [i['latitude'] for i in r],
            }],
            'layout': {
                'height': 700,
                'margin': {"r":0,"t":0,"l":0,"b":0},
                'mapbox': {
                    'center': {"lat": 40.722469759433, "lon": -73.9871350560601},
                    'zoom' : 14,
                    'style':"carto-positron"
                }    
            }
        })
    ])

if __name__ == '__main__':
    app.run_server(debug=True)




