import os,sys
from pathlib import Path
import pandas as pd
import numpy as np

from network_security.exception.exception import NetworkSecurityException
from network_security.logger.logger import logging

from network_security.entity.config_entity import DataTransformationConfig
from network_security.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact)

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security.constant.training_pipeline import TARGET_COLUMN

from network_security.utils.main_utils.utils import ( save_numpy_array_data,save_object,load_numpy_array_data,load_object)


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    @staticmethod
    def read_data(filepath)->pd.DataFrame:
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def get_data_transformer_object(cls)-> Pipeline:
        logging.info(
            "Entered get_data_transformer_object method of DataTransformation class"
        )

        try:
            imputer: KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(
            f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )

            preprocessor :Pipeline = Pipeline([('imputer',imputer)])

            logging.info(
                "Exited get_data_transformer_object method of DataTransformation class"
            )

            return preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self)-> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")

        try:
            logging.info("Starting data transformation")

            #getting everything here
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            preprocessor=self.get_data_transformer_object()

            logging.info("Got the preprocessor object")

            #training split into input and target
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)

            #testing split into input and output
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df=test_df[TARGET_COLUMN]
            target_feature_test_df=target_feature_test_df.replace(-1,0)

            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)


            train_arr=np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr=np.c_[(transformed_input_test_feature,np.array(target_feature_test_df))]

            #save numpy array date
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)

            #preparing artifact
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            logging.info(f"Data transformation artifact: {data_transformation_artifact}")

            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)













