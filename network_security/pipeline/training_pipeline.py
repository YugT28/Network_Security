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



from network_security.cloud.s3_syncer import S3Sync
from network_security.constant.training_pipeline import TRAINING_BUCKET_NAME,SAVED_MODEL_DIR
class TrainingPipeline:
    is_pipeline_running = False
    def __init__(self):     #initialte TrainingPipelineConfig object
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync=S3Sync()


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

    def start_model_evaluation(self,model_trainer_artifact:ModelTrainerArtifact,data_validation_artifact:DataValidationArtifact):
        try:
            logging.info("Start evaluation")

            model_evaluation_config:ModelEvaluationConfig=ModelEvaluationConfig(self.training_pipeline_config)

            model_evaluation=ModelEvaluation(model_trainer_artifact=model_trainer_artifact,model_eval_config=model_evaluation_config,data_validation_artifact=data_validation_artifact)

            model_evaluation_artifact=model_evaluation.initiate_model_evaluation()

            logging.info(f"Evalution successfuclly ended {model_evaluation_artifact}")

            return model_evaluation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifact):
        logging.info("Start pusher")
        try:
            model_pusher_config=ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher=ModelPusher(model_pusher_config,model_evaluation_artifact)
            model_pusher_artifact=model_pusher.initiate_model_pusher()

            logging.info("end model pushing task")
            return model_pusher_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/{SAVED_MODEL_DIR}"
            self.s3_sync.sync_folder_to_s3(folder=SAVED_MODEL_DIR,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def run_pipeline(self):       #master method
        try:
            data_ingestion_artifact=self.start_data_ingestion()                 #starting ingestion
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)                #starting data Validation
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            model_evaluation_artifact=self.start_model_evaluation(model_trainer_artifact=model_trainer_artifact,data_validation_artifact=data_validation_artifact)

            if not model_evaluation_artifact.is_model_accepted:
                # raise Exception("Trained model is not better than the best model")
                print("Trianed Model is not Better than the best model")

            model_pusher_artifact=self.start_model_pusher(model_evaluation_artifact=model_evaluation_artifact)

            TrainingPipeline.is_pipeline_running=False
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()

        except Exception as e:
            self.sync_artifact_dir_to_s3()
            TrainingPipeline.is_pipeline_running=False
            raise NetworkSecurityException(e,sys)
