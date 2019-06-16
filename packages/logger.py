import logging
from logging.handlers import RotatingFileHandler

class Logger():
    '''
        Class definition - to configure logging on 
        initalisation of the class
    '''
    def __init__(self):
        logging.basicConfig(
        handlers=[RotatingFileHandler('logs/app_log.log', maxBytes=100000, backupCount=10)],
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt='%Y-%m-%dT%H:%M:%S')
       


  
       
        

