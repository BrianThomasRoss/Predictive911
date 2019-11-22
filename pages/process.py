import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            # Process

            #### The dataset for this model can be found at the [City of Detroit Open Data Portal](https://data.detroitmi.gov/datasets/911-calls-for-service)

            ## Goal
            The goal of this project is to predict the frequency of 911 calls to the police for a given geographic area on a specified date.
            
            ## Processing The Data
            I started with loading the data set and pruning it down to only the necessary information. The original dataset contains all information
             for every 911 call within Detroit over a 3 year period. This amounts to almost 3 million observations. To start with I pruned the
             data down to only those columns that would be needed later. 
            
            Next step was to parse through the call descriptions and retain only those observations which contained calls directed to the police.
            The information that was valid for the purposes of this model was that relating to location and time. The call timestamp was broken 
            down to year, week, month, day of week, day and the part of day using the following funciton:
            
          

            The next step was to seperate the locations into distinct geographical spaces. After filtering for geographic outliers a function was 
             designed to create essentially what is a grid of the Detroit area and then assign to each observation the latitude and longitude 
             gridspace in which it exists.

            After all this has been done then we can group all the observations by their locations in time and space allowing us to have 
             a tally of the total number of events for each gridspace during a given date and time.


            ## Modelling

            As is best practice I began with a baseline which produced the following:

            After trying a few different models, and parameters the prevailing model was a Random Forest Regressor with 100 trees which 

            




             






        


            """
        ),


    ],
)

layout = dbc.Row([column1])