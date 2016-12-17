#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Utilities to retrieve weather data for the races"""

import sys
import time
import datetime
import numpy as np
import pandas as pd
import weather


def search_weather(races_df, api_key):
    """Build a dataset with weather information given a dataset containing
    information about races.

    Parameters
    ----------
    races_df : pandas.DataFrame
        dataframe containing the races information
    api_key : string
        API key for historical weather service

    Returns
    -------
    new_dataframe : pandas.DataFrame
        the new dataframe containing previous information and weather
        information
    """

    # Load the races dataset
    dataframe = races_df

    # Create an empty dataframe to store weather
    weather_df = pd.DataFrame(columns=['min_temp', 'max_temp', 'uv_index',
                                       'weather_desc'])

    # For each row (ie race), find the weather and store it
    for index, row in dataframe.iterrows():
        # Extract race information
        date_string = row['Date']
        date_split = date_string.split('.')
        day = int(date_split[1])
        month = int(date_split[2])
        year = int(date_split[3])
        city = row['Place']

        # If date too old (< 1st July 2008), no weather available, put nans and
        # go on...
        if (year < 2008) or (month < 7 and year == 2008):
            #print("old race")
            weather_df.loc[index, 'min_temp'] = np.nan
            weather_df.loc[index, 'max_temp'] = np.nan
            weather_df.loc[index, 'uv_index'] = np.nan
            weather_df.loc[index, 'weather_desc'] = None
        else:
            # Lookup weather
            weather_json = weather.lookup_weather(city, day, month, year, api_key)

            # Extract weather info
            try:
                min_temp, max_temp, uv_index, hourly = weather.extract_weather_info(weather_json)

                weather_df.loc[index, 'min_temp'] = min_temp
                weather_df.loc[index, 'max_temp'] = max_temp
                weather_df.loc[index, 'uv_index'] = uv_index

                descriptions = [hourly[k]['description'] for k in hourly.keys()]
                from collections import Counter
                count = Counter(descriptions)
                if len(set([cnt for (_, cnt) in count.most_common()])) == 1:
                    # All descriptions are unique : take midday
                    desc = hourly['1200']['description']
                else:
                    # Take most common description
                    desc = count.most_common()[0][0]
                weather_df.loc[index, 'weather_desc'] = desc
            except Exception as excep:
                #print(excep)
                weather_df.loc[index, 'min_temp'] = np.nan
                weather_df.loc[index, 'max_temp'] = np.nan
                weather_df.loc[index, 'uv_index'] = np.nan
                weather_df.loc[index, 'weather_desc'] = None

    # Merge dataframes
    new_dataframe = pd.concat([dataframe, weather_df], axis=1)

    return new_dataframe
    # Store new dataframe on CSV file (with timestamp in name)
    # new_dataframe.to_csv('races_weather_{}.csv'.format(int(time.time())))


def build_weather_dataset(races_filename, api_key):
    """Search the weather for all races and add information in a new dataframe.
    This function is needed because of the API limitations.

    Parameters
    ----------
    races_filename : string
        the file containing information about the races
    api_key : string
        API key for historical weather service

    Returns
    -------
        nothing
    """

    # Load data
    races_df = pd.read_csv(races_filename, index_col=0)

    # Split data given API limitation
    api_calls_limit = 450
    num_chunks = round(races_df.shape[0] / api_calls_limit)
    chunks = np.array_split(races_df, num_chunks)
    print("Data divided in {} chunks to fit API limit".format(num_chunks))

    # Create empty dataframe
    final_df = pd.DataFrame()

    # For each chunk, get new dataframe and add it to the final one
    chunk_num = 0
    for chunk in chunks:
        print("Processing chunk {}".format(chunk_num + 1))
        chunk_num += 1

        # Search for weather information
        chunk_new = search_weather(chunk, api_key)
        final_df = pd.concat([final_df, chunk_new], axis=0)

        # Save intermediary step
        chunk_new.to_csv("races-information-{}.csv".format(chunk_num))

        # Wait a bit more than 24 hours :-)
        if (chunk_num != len(chunks)):
            print("Entering sleep mode : see you tomorrow !")
            delta = datetime.timedelta(hours=25)
            time.sleep(delta.total_seconds())

    # Output final dataframe to CSV file
    print("Exporting to CSV file")
    final_df.to_csv('../datasets/races-information-weather.csv')


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) < 2:
        print("Usage : `python weather_utils.py <races_file.csv> <api_key>`")
        sys.exit(1)

    build_weather_dataset(args[0], args[1])
