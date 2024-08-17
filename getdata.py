import os
import sys
import json
from pathlib import Path


from dotenv import load_dotenv  #to interact with .env file
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)


import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo

from network_security.exception.exception import NetworkSecurityException
from network_security.logger.logger import logging

class NetworkDataExtraction():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def csv_to_json_converter(self,file_path):
        """Convert From CSV TO DATAFRAME THEN TO JSON and Then Again Convert TO Python Object"""
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def pushing_data_to_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)

            self.database=self.mongo_client[self.database]

            self.collection=self.database[self.collection]

            self.collection.insert_many(self.records)

            return len(self.records)

        except Exception as e:
            raise NetworkSecurityException(e,sys)


if __name__=='__main__':
    CWD=Path.cwd()
    FILE_PATH=CWD/'Network_Data/NetworkData.csv'
    DATABASE='xyz'
    COLLECTION='NetworkData'
    networkobj=NetworkDataExtraction()
    records=networkobj.csv_to_json_converter(FILE_PATH)
    no_of_records=networkobj.pushing_data_to_mongodb(records,DATABASE,COLLECTION)
    print(no_of_records)






