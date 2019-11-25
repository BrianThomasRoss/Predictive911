# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """        
            # **Force Projection**. 
            ## *Simplified*.

            ##### Now more than ever police departments across the country face expanding and dynamic challenges. From traditional policing, to new spectres like counter-terrorism, the requirements of a police force are evolving. Add to this the current reality of budget constraints and these concerns become even more difficult to manage.

            Thankfully technology is evolving alongside your department's law enforcement demands. Combining state of the art predictive modelling techniques with modern computing power
             your department can draw on its existing wealth of data to build a comprehensive picture of where the demands are and where they will come from next.
             Allowing your department to shift it's focus from logistics and analysis to maintaining **law and order**. 
            """
        ),
        dcc.Link(dbc.Button('Behind The Curtain', color='primary'), href='/predictions')
    ],
    md=4,
)

data = pd.read_csv('assets\raw-csvs\scatter_data.csv')

token = ('pk.eyJ1IjoiYnJpYW50aG9tYXNyb3NzIiwiYSI6ImNrMzY5ZTFyeDFvbm0zbXBwcGU4eW9wZWYifQ.BdRmQ9Q7siK7XNnFTvuasQ')

fig = px.scatter_mapbox(data, lat = 'latitude', lon = 'longitude', hover_name='calldescription',zoom=10.25)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(mapbox_style="dark", mapbox_accesstoken = token)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

column2 = dbc.Col(
    [
        dcc.Graph(figure=fig),
    ]
)

layout = dbc.Row([column1, column2])