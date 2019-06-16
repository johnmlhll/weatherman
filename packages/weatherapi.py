import json
import configparser
import requests
import os
import logging
from datetime import datetime as dt


class WeatherApi():
    '''
        Class Definition: Processes OpenWeatherMap API requests
    '''
    def __init__(self):
        self.api_url = "https://api.openweathermap.org/data/2.5/forecast/daily?q={}&cnt=16&appid={}"
        
    def get_apikey(self):
        '''
            Method definition: pulls api key from config file
        '''
        apikey = os.environ['apikey']
        return apikey

    def call_weatherapi(self, api_key, city):
        '''
            Method definition: processes api request
        '''
        try:
            url = self.api_url.format(city, api_key)
            api_call = requests.get(url)
            transformed_api_call = self.transform_weather_update(api_call)
            return transformed_api_call
        except requests.exceptions.RequestException as api_ex:
            logging.error('API Exception in call_weather_app. Details: {}'.format(api_ex))


    def transform_weather_update(self, api_obj):
        '''
            Method definition: helper method to transform the weather api return
        '''
        api_obj = api_obj.text
        api_obj = json.loads(api_obj)
        transformed_call = {}
        weekdays  = {
            '0':'Monday',
            '1':'Tuesday',
            '2':'Wednesday',
            '3':'Thursday',
            '4':'Friday',
            '5':'Saturday',
            '6':'Sunday'
            }
        try:    
            if api_obj is None:
                return None
            else:
                api_count = 1
                for key, value in api_obj.items():
                    if key == 'list':
                        for day_item in value:
                            days_reporting_dict = {}
                            for day_key, day_value in day_item.items():
                                # date/day 
                                if day_key == 'dt':
                                    date_day = dt.utcfromtimestamp(day_value)
                                    weekday_index = str(date_day.weekday())
                                    days_reporting_dict['Day'] = weekdays[weekday_index]
                                    days_reporting_dict['Date'] = date_day.date()
                                # temp
                                if day_key == 'temp':
                                    average_day_temp = (day_value['min'] + day_value['max']) / 2 
                                    temp_celsuis = int(average_day_temp) - 273.15
                                    days_reporting_dict['Average Daily Tempereture (Celsius)'] = round(temp_celsuis, 0)
                                # weather details 
                                if day_key == 'humidity':
                                    days_reporting_dict['Humidity (%)'] = day_value
                                if day_key == 'pressure':
                                    days_reporting_dict['Pressure (bars)'] = day_value
                                if day_key == 'speed':
                                    days_reporting_dict['Windspeed (mph)'] = day_value
                                if day_key == 'weather':
                                    for k,v in day_value[0].items():
                                        if k == 'main':
                                            days_reporting_dict['Predication'] = v 
                                        if k == 'description':
                                            days_reporting_dict['Description'] = v 
                                        if k == 'icon':
                                            days_reporting_dict['icon'] = v   
                            transformed_call[api_count] = days_reporting_dict
                            api_count = api_count + 1 
                return transformed_call
        except Exception as ex:
            logging.debug("General exception in transform_weather_update: {}".format(ex))