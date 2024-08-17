import os
import sys
import json

from dotenv import load_dotenv


import certifi
import pandas as pd
import numpy as np
import pymongo

from network_security.exception.exception import NetweorkSecurityException
from network_security.logger.logger import logging

class NetworkDataExtraction():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkDataExtraction(e,sys)
    def csv_to_json_converter(self):
        try:
            pass
        except Exception as e:
            raise NetworkDataExtraction(e,sys)

    def pushing_data_to_mongodb(self):
        try:
            pass
        except Exception as e:
            raise NetworkDataExtraction(e,sys)

    if __name__=='__main__':
        pass





