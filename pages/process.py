# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

text = {'display':'inline-block','textAlign': 'center'}

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
            Data was acquired using the [City of Detroit Open Data Portal](https://data.detroitmi.gov/)
            """, style={'padding-left':'5%'}),
        html.H2('Goal', style={'padding-left':'40%'}),
        html.Hr(),
        dcc.Markdown("""
        The goal of this project was to be able to predict the frequency of 911 calls for police assistance on
        a specified date in the future.
        """),
        html.H2('Exploratory Data Analysis',style={'padding-left':'15%'}),
        html.Hr(),
        dcc.Markdown(
            """
            The original data contained information for every 911 call to the City of Detroit over a three year
            period, and was by far the largest collection of data that I had worked with thus far, in total almost
            2.5 million observations. Before I could begin to explore the data it was necessary to prune it down to 
            only that information which was valuable for my purposes.

            Cleaning the data included filtering for only those call which were requests for police assistance through
            parsing the call codes. In addition to this it was necessary to filter for geographic outliers as there were
            several entries, which I believe were due to entry errors, that fell well outside the bounds of the city
            limits. The call timestamp feature was broken down into year, week, month, day of week, day and then 
            and engineered feature "part of day" which was achieved through implementation of the function displayed on
            right.
            """
        )

    ],
)

column2 = dbc.Col([
    dcc.Markdown("""
    ![Part of Day Function](/assets/img/part-of-day-func.jpg)
    """, style={'padding-top':'40%', 'padding-left':'20%'})
])

layout = dbc.Row([column1, column2])