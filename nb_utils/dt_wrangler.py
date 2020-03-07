import pandas as pd
import numpy as np
import datetime as dt
import typing

def extract_dt_cols(df: pd.DataFrame, col: str,
                    drop_original: bool=True)-> pd.DataFrame:
    """Extracts datetime features from a series of timestamps

    Arguments:
        df {pd.Dataframe} -- The pandas dataframe containing the timestamp
        feature
        col {str} -- The name of the column
        drop_original {boolean} -- default is True, drops column passed in col
        argument from the dataframe

    Returns:
        pd.DataFrame -- DataFrame with the extracted features appended
    """
    df[col] = pd.to_datetime(df[col])

    df['year']     = df[col].year
    df['month']    = df[col].month
    df['day']      = df[col].day
    df['call_dow'] = df[col].dayofweek
    df['week']     = df[col].week
    df['hour']     = df[col].hour

    return df

def get_day_part(df: pd.DataFrame, hour_col: str)-> pd.DataFrame:
    """Extacts the time of day from the hour value by dividing by the hour
     knife
    1 = Morning  (0400 - 1000h)
    2 = Midday   (1000 - 1600h)
    3 = Evening  (1600 - 2200h)
    4 = Night    (2200 - 0400h)

    Arguments:
        df {pd.DataFrame} -- dataframe containing the hour column
        hour_col {str} -- name of the hour column

    Returns:
        pd.DataFrame -- pandas dataframe with the new column appended
    """
    hour_knife = 6
    df['part_of_day'] = ((df['hour'] + 2) / hour_knife).astype(int)
    df['part_of_day'] = df['part_of_day'].replace(0, 4)
    
    return df

