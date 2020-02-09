


import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from datetime import date
from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
r = json.loads(requests.get('https://cwhong.carto.com/api/v2/sql?q=select distinct agency from public.table_311_1').content)
agency_options = [{'label':i['agency'], 'value':i['agency']} for i in r['rows']]
headers = {'X-App-Token':os.environ['API_TOKEN']}
url='https://data.cityofnewyork.us/resource/erm2-nwe9.json'

app.layout = html.Div([
    dcc.Dropdown(
        id='agency-dropdown',
        options=agency_options,
        value='TLC'
    ), 
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=date.today()-timedelta(days=7),
        max_date_allowed=date.today(),
        initial_visible_month=date.today(),
        start_date=date.today()-timedelta(days=7),
        end_date=date.today()
    ),
    html.Div(id='map-area')
])

@app.callback(
    dash.dependencies.Output('map-area', 'children'),
    [dash.dependencies.Input('agency-dropdown', 'value'),
    dash.dependencies.Input('date-picker', 'start_date'),
    dash.dependencies.Input('date-picker', 'end_date')])
def update_output(agency, start_date, end_date):
    params = {
            '$select':'longitude,latitude', 
            '$where':f"agency='{agency}' AND longitude IS NOT NULL AND latitude IS NOT NULL AND created_date>'{start_date}' AND created_date<'{end_date}'",
            '$limit':50000
            }

    r = json.loads(
            requests.get(f"{url}", headers=headers, params=params).content)
    return html.Div([
    dcc.Graph(
        id='agency-plot',
        figure={
            'data': [{
                'type': 'densitymapbox',
                'lon': [float(i['longitude']) for i in r],
                'lat': [float(i['latitude']) for i in r],
                'radius':10
            }],
            'layout': {
                'height': 700,
                'margin': {"r":0,"t":0,"l":0,"b":0},
                'mapbox': {
                    'center': {"lat": 40.722469759433, "lon": -73.9871350560601},
                    'zoom' : 11,
                    'style':"carto-positron"
                }    
            }
        })
    ])

if __name__ == '__main__':
    app.run_server(debug=True, port=5000)




