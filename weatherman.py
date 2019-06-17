from flask import Flask, render_template, request, url_for
from werkzeug import security
import os
import sys
import logging
import json
import unittest
from packages.logger import Logger
from packages.weatherapi import WeatherApi
from tests.test_weatherman import TestWeatherman
import packages.environ_support

app = Flask(__name__)
api = WeatherApi()
error = os.environ['frontend_error']
logger = Logger()  # initalises the logger config


@app.route('/')
def main():
    return render_template('home.html')

@app.route('/summary', methods=['POST', 'GET'])
def summary():
    if request.method == 'POST':
        location = request.form['city'] 
        api_key = api.get_apikey() 
        weather = api.call_weatherapi(api_key, location)
        if len(weather) == 16:
            logging.info('API call processed successfully')
            return render_template('summary.html', weather=weather)
        else:
            logging.warning('API call failed. Please retry and check below')    
    return render_template('home.html', error=error)        

        
if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000) # dev only
    unittest.main()