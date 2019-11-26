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
# model = load('assets/pipeline.joblib')
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

fig = go.Figure(go.Densitymapbox(lat=df.latitude, lon=df.longitude, radius=5, zoo))
fig.update_layout(
    mapbox = {
        'accesstoken': token,
        'style': "dark",
        'zoom': 10},
    showlegend = False,
    mapbox_center_lon =-83,
    mapbox_center_lat =42.4)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})




column2 = dbc.Col(
    [
    dcc.Graph(id='graph', figure=fig),
    ]
    ,md=8)



layout = dbc.Row([column1, column2])