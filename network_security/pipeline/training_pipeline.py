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
    def __init__(self):
        pass
    def start_data_ingestion(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def run_pipeline(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)