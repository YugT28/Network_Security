#complete data ingestion component
import os
import sys

import pandas as pd
import numpy as np
from pathlib import Path
import pymongo

from typing import List

from sklearn.model_selection import train_test_split


from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv('MONGO_DB_URL')
print(MONGO_DB_URL)


#import logging and exception
from network_security.exception.exception import NetworkSecurityException
from network_security.logger.logger import logging

#importing configuration and artifact related to Data Ingestion
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact





class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):    #start from ConfigFile
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def export_collection_as_dataframe(self)->pd.DataFrame:
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            collection = self.mongo_client[database_name][collection_name]

            df=pd.DataFrame(list(collection.find()))

            if "_id" in df.columns.to_list():
                df = df.drop(columns="_id",axis=1)

            df.replace({"na":np.nan},inplace=True)

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self,dataframe:pd.DataFrame)->pd.DataFrame:    #getting into central repo
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path

            #create folder
            dir_path = Path(feature_store_file_path).parent
            dir_path.mkdir(parents=True, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)  #create csv file and add data
            return dataframe


        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self,dataframe:pd.DataFrame):               #solve problem of data leakage
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)

            dir_path=Path(self.data_ingestion_config.training_file_path).parent
            dir_path.mkdir(parents=True,exist_ok=True)
            dir_path = Path(self.data_ingestion_config.testing_file_path).parent
            dir_path.mkdir(parents=True, exist_ok=True)

            logging.info(f"Exporting Training and Testing File Path")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info(f"Export Training and Testing SUCCESS")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):              #master method create artifact file
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            #artifact Object creation
            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact        #passing to next component

        except Exception as e:
            raise NetworkSecurityException(e,sys)

