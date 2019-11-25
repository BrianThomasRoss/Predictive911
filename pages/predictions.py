# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import datetime as dt
from joblib import load

# Imports from this application
from app import app

#
model = load('assets/pipeline.joblib')
token = ('pk.eyJ1IjoiYnJpYW50aG9tYXNyb3NzIiwiYSI6ImNrMzY5ZTFyeDFvbm0zbXBwcGU4eW9wZWYifQ.BdRmQ9Q7siK7XNnFTvuasQ')

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        
        html.Hr('Select A Date'),

        dcc.DatePickerSingle(
        id = 'datepicker',
        month_format ='MMMM Y',
        placeholder='MMMM Y',
        date=dt.datetime(2020,11,21)),
    ],
    md=4,
)

df = pd.read_csv('assets/raw-csvs/scatter_data.csv')

fig = go.Figure(go.Densitymapbox(lat=df.latitude, lon=df.longitude, radius=5))
fig.update_layout(
    mapbox = {
        'accesstoken': token,
        'style': "dark"},
    showlegend = False,
    mapbox_center_lon =-83,
    mapbox_center_lat =42.4)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

@app.callback(
        Output('graph','figure'),
        [Input('javascript','event'),
            Input('datepicker','date')])

column2 = dbc.Col(
    [
        dcc.Graph(id='graph',figure=fig),
    ]
)

# def update_graph(date):
#     date = pd.to_datetime(date)

#     year = date.dt.year
#     month = date.dt.month
#     day = date.dt.day
#     week = date.dt.week
#     dow = date.dt.dayofweek
    
#     df = pd.read_csv(r'assets\raw_csvs\pred_template.csv')
#     df = df.drop(columns='Unnamed: 0')
#     length = len(df)
    
#     df['year'] = [year]*length
#     df['month'] = [month]*length
#     df['day'] = [day]*length
#     df['week'] = [week]*length
#     df['dow'] = [dow]*length

#     lat_max =  42.46
#     lon_max = -82.91
#     lat_min =  42.25
#     lon_min = -83.28

#     lon_range = lon_max - lon_min
#     lat_range = lat_max - lat_min

#     lat_length = lat_range / 10
#     lon_length = lon_range / 15
    
#     df['lat_center'] = lat_min + ((lat_length * df['lat_grid']) + (.5*lat_length))
#     df['lon_center'] = lon_min - ((lon_length * df['lon_grid']) + (.5*lon_length))
    
#     preds = pipeline.predict(df)
    
#     df['count'] = preds


#     fig = go.Figure(go.Densitymapbox(lat=df.lat_center, lon=df.lon_center, z=df.count, radius=10, showscale=False))
#     fig.update_layout(
#         mapbox = {
#             'accesstoken': token,
#             'style': "dark"},
#     showlegend = False)
#     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#     return fig

#     fig = update_graph(date)

layout = dbc.Row([column1, column2])