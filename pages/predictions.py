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

weather_options = ['Clear', 'Light Rain', 'Heavy Rain', ' Thunderstorm', 'Light Snow', 'Heavy Snow']
text = {'display':'inline-block','textAlign': 'center'}

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        html.Hr(),
        html.H2('Predict Call Frequency And Location', style = text),
        html.Br(),

        html.H3('Select A Day', style = text),
        html.Br(),

        dcc.DatePickerSingle(
        id = 'datepicker',
        month_format ='MMMM Y',
        placeholder='MMMM Y',
        date=dt.datetime(2020,11,21)),
        html.Br(),

        html.Hr(),
        html.H3('Weather Forecast', style = text),
        html.Br(),

        dcc.Dropdown(
            id = 'weather_dropdown',
            options = [{'label':option,'value':option} for option in weather_options],
            placeholder = 'Conditions'
        ),

        html.Br(),
        html.H3('Temperature', style = text),
        html.Br(),
        html.H6('Fahrenheit', style = text),
        html.Br(),

        dcc.Input(
        id= 'low_temp',
        placeholder='Forecasted Low',
        type='number',
        value='',
        min = -20,
        max = 110
        ),

        dcc.Input(
        id= 'high_temp',
        placeholder='Forecasted High',
        type='number',
        value='',
        min = -20,
        max = 110
        ),

        html.H3('Severe Weather', style = text),
        html.Br(),
        dcc.RadioItems(
        id = 'severe_flag',    
        options = [
            {'label': 'Yes', 'value': 1},
            {'label': u'No', 'value': 0}
        ],
        value='No'
        ),

        html.H2('Holiday Or Event', style = text),
        html.Br(),
        dcc.RadioItems(
        id = 'holiday_flag',    
        options = [
            {'label': 'Yes', 'value': 1},
            {'label': u'No', 'value': 0}
        ],
        value='No'
        ),
    ],
    md=4,
)

df = pd.read_csv('assets/raw-csvs/scatter_data.csv')

fig = go.Figure(go.Densitymapbox(lat=df.latitude, lon=df.longitude, radius=5))
fig.update_layout(
    mapbox = {
        'accesstoken': token,
        'style': "dark",
        'zoom': 10},
    showlegend = False,
    mapbox_center_lon =-83.07587,
    mapbox_center_lat =42.3625
    )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})




column2 = dbc.Col(
    [
    dcc.Graph(id='graph', figure=fig),
    ]
    ,md=8)



layout = dbc.Row([column1, column2])