"""Module to fetch weather information"""

import requests as rq

def lookup_weather(city, day, month, year, api_key):
    """Get weather information for a place at a given date, using the
    World Weather Online API. This API is limited to 500 calls / user / day.

    Parameters
    ----------
    city : string
    day : int
    month : int
    year : int
    api_key : string

    Returns
    -------
        json response
    """

    # Build parameters dictionary
    date_string = "{}-{}-{}".format(year, str(month).zfill(2), str(day).zfill(2))
    params = {
        "q": city,
        "date": date_string,
        "key": api_key,
        "format": "json",
        }

    # Fetch data with GET request
    url = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx"
    response = rq.get(url, params)

    return response.json()


def extract_weather_info(json):
    """Extract useful features from a JSON response for a World Weather Online
    API call.

    Parameters
    ----------
    json : dict

    Returns
    -------
    min_temp : int
        minimal temperature in Celsius degrees
    max_temp : int
        maximal temperature in Celsius degrees
    uv_index : int
        UV index
    hourly : dict
        dictionary containing hourly info, with the following format:
        {
            time: {
                'temp': t,
                'windspeed': ws,
                'humidity': hp,
                'precip': milli,
                'description': desc
                }
        }
    """
    try:
        weather = json['data']['weather'][0]

        # Extract general information
        min_temp = int(weather['mintempC'])
        max_temp = int(weather['maxtempC'])
        uv_index = int(weather['uvIndex'])

        # Extract hourly information
        hourly = {}
        for hweather in weather['hourly']:
            time = hweather['time']
            temp = int(hweather['tempC'])
            ws = int(hweather['windspeedKmph'])
            hp = int(hweather['humidity'])
            milli = float(hweather['precipMM'])
            desc = ""
            if len(hweather['weatherDesc']) > 0:
                desc = hweather['weatherDesc'][0]['value']
            hourly[time] = {
                'temp': temp,
                'windspeed': ws,
                'humidity': hp,
                'precip': milli,
                'description': desc
                }

        return min_temp, max_temp, uv_index, hourly
    except KeyError:
        #print("error during parsing of weather info from API")
        raise Exception

