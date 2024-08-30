import os
import sys

#importing logging and exception
from network_security.logger.logger import logging
from network_security.exception.exception import NetworkSecurityException

#importing component we have to configure
from network_security.components.data_ingestion import DataIngestion
from network_security.components.data_validation import DataValidation
from network_security.components.data_transformation import DataTransformation
from network_security.components.model_trainer import ModelTrainer
from network_security.components.model_evaluation import ModelEvaluation
from network_security.components.model_pusher import ModelPusher


#importing config class for every component and training_pipeline also
from network_security.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig,
    ModelEvaluationConfig,
    ModelPusherConfig
)

#import artifact class for every component
from network_security.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
    ModelEvaluationArtifact,
    ModelPusherArtifact
)

class TrainingPipeline:
    def __init__(self):     #initialte TrainingPipelineConfig object
        self.training_pipeline_config = TrainingPipelineConfig()


    def start_data_ingestion(self):
        try:
            data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)        #config class
            logging.info("Starting Data INgestion")
            data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)       #create component by inserting config
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()                     #initialting data ingestion which return artifact
            logging.info(f"Data Ingestion completed {data_ingestion_artifact}")
            return data_ingestion_artifact                                                       #returning this artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_data_validation(self,data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info("Starting Data Validation")
            #datavalidationconfig->TrainingPielineCongig
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)

            #Validation component -> DataValidation config, Data Igestion Artifact
            data_validation=DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)

            #initiate data validation this output data validation

            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Data Validation completed {data_validation_artifact}")

            return data_validation_artifact


        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            logging.info("Starting Data Transformation")
            #configuration
            data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)

            #component
            data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact, data_transformation_config=data_transformation_config)

            #initiate data transformation
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info(f"Data Transformation completed {data_transformation_artifact}")

            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info("Starting Model Traininig")

            #configuration
            model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)

            model_trainer=ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_trainer_config=model_trainer_config)

            model_trainer_artifact=model_trainer.initiate_model_trainer()

            logging.info(f"Model Training completed {model_trainer_artifact}")

            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def run_pipeline(self):       #master method
        try:
            data_ingestion_artifact=self.start_data_ingestion()                 #starting ingestion
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)                #starting data Validation
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
        except Exception as e:
            raise NetworkSecurityException(e,sys)