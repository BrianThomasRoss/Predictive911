# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
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

weather_options = {'Clear': 800, 'Light Rain': 500, 'Heavy Rain': 502, 
                   'Thunderstorm': 202, 'Light Snow': 600, 'Heavy Snow':602}

text = {'display':'inline-block','textAlign': 'center'}

column_order = pd.read_csv('assets/raw-csvs/testy.csv')



# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        html.H3('Predict Call Frequency And Location', style = text),
        html.Br(),
        html.Hr(),

        html.H5('Select A Day',
        style={'padding-left':'30%'}),
        html.Br(),
        dcc.DatePickerSingle(
        id = 'datepicker',
        month_format ='MMMM Y',
        placeholder='MMMM Y',
        date=dt.datetime(2020,11,21),
        style={'padding-left':'28%'}),
        html.Br(),
        html.Br(),

        html.H5('Weather Forecast', style={'padding-left':'25%'}),
        html.Br(),
        dcc.Dropdown(
            id = 'weather_dropdown',
            options = [{'label': i, 'value': j} for i,j in weather_options.items()],
            value = 800
        ),
        html.Br(),

        html.H5('Forecasted Temperature', style={'padding-left':'19%'}),
        html.Hr(),

        html.H6('Low', style={'padding-left':'45%'}),
        dcc.Slider(
        id= 'low_temp',
        value=60,
        min = -20,
        max = 110,
        step = 1,
        marks={
            0: {'label': '0 °F', 'style': {'color': '#77b0b1'}},
            32: {'label': '32 °F'},
            68: {'label': '68 °F'},
            100: {'label': '100 °F', 'style': {'color': '#f50'}}
        },
        included=False),

        html.H6('High', style={'padding-left':'44%'}),
        dcc.Slider(
        id= 'high_temp',
        value=70,
        min = -20,
        max = 110,
        step = 1,
        marks={
            0: {'label': '0 °F', 'style': {'color': '#77b0b1'}},
            32: {'label': '32 °F'},
            68: {'label': '68 °F'},
            100: {'label': '100 °F', 'style': {'color': '#f50'}}
        },
        included=False),
        html.Hr(),

        html.H5('Severe Weather', style={'padding-left':'30%'}),
        dcc.RadioItems(
        id = 'severe_flag',
        options = [
            {'label': 'Yes', 'value': 1},
            {'label': 'No', 'value': 0},

        ],
        value = 0,
        labelStyle = {
        'display': 'inline-block',
        'margin-right': 30},
        style={'padding-left':'33%'}
        ),

        html.H5('Holiday Or Event', style={'padding-left':'27%'}),
        dcc.RadioItems(
        id = 'holiday_flag',
        options = [
            {'label': 'Yes', 'value': 1},
            {'label': 'No', 'value': 0}
        ],
        value = 0,
        labelStyle = {
        'display': 'inline-block',
        'margin-right': 30},
        style={'padding-left':'33%'}
        ),
        html.Hr(),
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
    html.Div(id='my-div'),
    dcc.Graph(id='prediction-graph'),
    ]
    ,md=8)




@app.callback(
    Output('prediction-graph', 'figure'),
    [Input('datepicker', 'date'),
     Input('weather_dropdown', 'value'),
     Input('low_temp', 'value'),
     Input('high_temp', 'value'),
     Input('severe_flag', 'value'),
     Input('holiday_flag', 'value')])

def update_pred(date, condition, low, high, severe, holiday):
    date = pd.to_datetime(date)
    year = date.year
    month = date.month
    week = date.week
    dow = date.dayofweek
    day = date.day

    df = pd.read_csv('assets/raw-csvs/pred_template.csv')
    length = len(df)

    df['year'] = [year]*length
    df['month'] = [month]*length
    df['day'] = [day]*length
    df['week'] = [week]*length
    df['dow'] = [dow]*length

    holiday = 0 if holiday == 'No' else 1
    df['is_holiday'] = [holiday]*length

    # Weather

    df['temp_min'] = [low]*length
    df['temp_max'] = [high]*length
    df['weather_id'] = [condition]*length

    severe = 0 if severe == 'No' else 1
    df['severe'] = [severe]*length

    lat_max =  42.46
    lon_max = -82.91
    lat_min =  42.25
    lon_min = -83.28

    # Total size of the gridspace
    lon_range = lon_max - lon_min
    lat_range = lat_max - lat_min

    #length of an individual grid section
    lat_length = lat_range / 10
    lon_length = lon_range / 15
    
    df = df[column_order.columns]
    preds = model.predict(df)

    df['count'] = preds
    
    df['lat_center'] = lat_min + ((lat_length * df['lat_grid']) + (.5*lat_length))
    df['lon_center'] = lon_min + ((lon_length * df['lon_grid']) + (.5*lon_length))

    fig = go.Figure(go.Densitymapbox(lat=df.lat_center, lon=df.lon_center, z=df['count'], radius=70,
                    showscale=False, hovertemplate='Number of Calls Predicted: %{z:.0f}<extra></extra>',
                    colorscale='Jet', zmax=30, zmin=1, zmid=20))
    fig.update_layout(
        mapbox = {
            'accesstoken': token,
            'style': "dark",
            'zoom': 10.25},
        margin={"r":0,"t":0,"l":0,"b":0},
        showlegend = False,
        mapbox_center_lon =-83.09587,
        mapbox_center_lat =42.3425, 
        height = 650,
        width  = 800
    )

    return fig

layout = dbc.Row([column1, column2])
