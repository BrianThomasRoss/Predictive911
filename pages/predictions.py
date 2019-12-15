# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import datetime as dt
from sklearn.ensemble import RandomForestRegressor
from joblib import load

# Imports from this application
from app import app

#
model = load('assets/model.joblib')
token = ('pk.eyJ1IjoiYnJpYW50aG9tYXNyb3NzIiwiYSI6ImNrMzY5ZTFyeDFvbm0zbXBwcGU4eW9wZWYifQ.BdRmQ9Q7siK7XNnFTvuasQ')

weather_options = ['Clear', 'Light Rain', 'Heavy Rain', ' Thunderstorm', 'Light Snow', 'Heavy Snow']
condition_codes = [800, 500, 502, 202, 600, 602]
text = {'display':'inline-block','textAlign': 'center'}

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        html.Hr(),
        html.H2('Predict Call Frequency And Location', style = text),
        html.Br(),
        html.Hr(),

        html.H3('Select A Day', style = text),
        html.Br(),

        dcc.DatePickerSingle(
        id = 'datepicker',
        month_format ='MMMM Y',
        placeholder='MMMM Y',
        date=dt.datetime(2020,11,21)),
        html.Br(),

        html.H3('Weather Forecast', style = text),
        html.Br(),
        dcc.Dropdown(
            id = 'weather_dropdown',
            options = [
                {'label':'Clear','value':800},
                {'label': 'Light Rain', 'value': 500},
                {'label': 'Heavy Rain', 'value': 502},
                {'label': 'Thunderstorm', 'value': 202},
                {'label': 'Light Snow', 'value': 600},
                {'label': 'Heavy Snow', 'value': 602}],
            placeholder = 'Conditions'
        ),
        
        html.H3('Forecasted Temperature', style = text),
        html.Br(),
        html.H6('(Fahrenheit)', style = text),
        html.Br(),
        
        html.H6('Low', style=text),
        dcc.Slider(
        id= 'low_temp',
        value=60,
        min = -20,
        max = 110,
        step = 1,
        marks={
            0: {'label': '0 °F', 'style': {'color': '#77b0b1'}},
            32: {'label': '32 °F'},
            65: {'label': '65 °F'},
            100: {'label': '100 °F', 'style': {'color': '#f50'}}
        },
        included=False),
        
        html.H6('High'),
        dcc.Slider(
        id= 'high_temp',
        value=70,
        min = -20,
        max = 110,
        step = 1,
        marks={
            0: {'label': '0 °F', 'style': {'color': '#77b0b1'}},
            32: {'label': '32 °F'},
            65: {'label': '65 °F'},
            100: {'label': '100 °F', 'style': {'color': '#f50'}}
        },
        included=False),
        html.Br(),
        
        html.H3('Severe Weather', style = text),
        html.Br(),
        dcc.RadioItems(
        id = 'severe_flag',    
        options = [
            {'label': 'Yes', 'value': 'Yes'},
            {'label': 'No', 'value': 'No'},

        ],
        value = 'No',
        labelStyle = {
        'display': 'inline-block',
        'margin-right': 30},
        ),

        html.H3('Holiday Or Event', style = text),
        html.Br(),
        dcc.RadioItems(
        id = 'holiday_flag',    
        options = [
            {'label': 'Yes', 'value': 'Yes'},
            {'label': 'No', 'value': 'No'}
        ],
        value = 'No',
        labelStyle = {
        'display': 'inline-block',
        'margin-right': 30},
        ),
        
        html.Hr(),
        html.Button('Submit', id='click', style = {'margin-left': 150})

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
    margin={"r":0,"t":0,"l":0,"b":0},
    showlegend = False,
    mapbox_center_lon =-83.09587,
    mapbox_center_lat =42.3425, 
    height = 650,
    width  = 800
    )




column2 = dbc.Col(
    [
    dcc.Graph(id='prediction-graph', figure=fig),
    ]
    ,md=8)


@app.callback(
    Output('prediction-graph', 'figure'),
    [Input('datepicker', 'date'),
     Input('weather_dropdown', 'condition'),
     Input('low_temp', 'low'),
     Input('high_temp', 'high'),
     Input('severe_flag', 'severe'),
     Input('holiday_flag', 'holiday')])


def update_pred(date, condition, low, high, severe, holiday):
    
    date = pd.to_datetime(date)
    year = date.year
    month = date.month
    week = date.week
    dow = date.dayofweek
    day = date.day
    holiday = 1 if holiday == 'Yes' else 0
    severe = 1 if severe == 'Yes' else 0

    df = pd.read_csv('assets/raw-csvs/pred_template.csv')
    df = df.drop(columns='Unnamed: 0')
    length = len(df)

    df['year'] = [year]*length
    df['month'] = [month]*length
    df['day'] = [day]*length
    df['week'] = [week]*length
    df['dow'] = [dow]*length

    df['is_holiday'] = [holiday]*length

    # Weather
    df['temp_min'] = [low.astype(int)]*length
    df['temp_max'] = [high.astype(int)]*length
    df['weather_id'] = [800]*length
    df['is_severe'] = [severe]*length

    lat_max =  42.46
    lon_max = -82.91
    lat_min =  42.25
    lon_min = -83.28

    lon_range = lon_max - lon_min
    lat_range = lat_max - lat_min

    lat_length = lat_range / 10
    lon_length = lon_range / 15

    preds = model.predict(df)

    df['count'] = preds    
    
    df['lat_center'] = lat_min + ((lat_length * df['lat_grid']) + (.5*lat_length))
    df['lon_center'] = lon_min + ((lon_length * df['lon_grid']) + (.5*lon_length))

    fig = go.Figure(go.Densitymapbox(lat=df.lat_center, lon=df.lon_center, z=df['count'], radius=20))
    fig.update_layout(
        mapbox = {
            'accesstoken': token,
            'style': "dark",
            'zoom': 10},
        margin={"r":0,"t":0,"l":0,"b":0},
        showlegend = False,
        mapbox_center_lon =-83.09587,
        mapbox_center_lat =42.3425, 
        height = 650,
        width  = 800
    )

    return fig

# fig = update_pred(date, condition, low_temp, high_temp, severe, holiday)




layout = dbc.Row([column1, column2])