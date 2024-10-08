from datetime import datetime
import os
from pathlib import Path

#importing constant from package used for configuration
from network_security.constant import training_pipeline  #constant



class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):                #capturing current time
        timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=Path(self.artifact_name,timestamp)
        self.timestamp: str = timestamp
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):         #pass trainingpipeline Config
        self.database_name=training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.collection_name=training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO

        self.data_ingestion_dir: str=Path(training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME)

        self.feature_store_file_path: str=Path(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME)
        self.training_file_path: str=Path(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTION_DIR,training_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path: str=Path(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTION_DIR,training_pipeline.TEST_FILE_NAME)


class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir: str= Path(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir: str= Path(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str= Path(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = Path(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = Path(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path: str=Path(self.invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = Path(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path: str= Path(self.data_validation_dir,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)



class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        #base location
        self.data_transformation_dir: str=Path(training_pipeline_config.artifact_dir,training_pipeline.DATA_TRANSFORMATION_DIR_NAME)
        self.data_transformation_transformed: str=Path(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR)
        self.data_transformation_object: str=Path(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR)
        #subdirectory for train and test
        self.transformed_train_file_path: str=Path(self.data_transformation_transformed,training_pipeline.TRAIN_FILE_NAME.replace("csv","npy"))
        self.transformed_test_file_path: str=Path(self.data_transformation_transformed,training_pipeline.TEST_FILE_NAME.replace("csv","npy"))
        #subdirectory for object
        self.transformed_object_file_path: str=Path(self.data_transformation_object,training_pipeline.PREPROCESSING_OBJECT_FILE_NAME)

class ModelTrainerConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trainer_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.MODEL_TRAINER_DIR_NAME
        )
        self.trained_model_file_path: str = os.path.join(
            self.model_trainer_dir, training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,
            training_pipeline.MODEL_FILE_NAME
        )
        self.expected_accuracy: float= training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold = training_pipeline.MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD

class ModelEvaluationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_evaluation_dir = Path(training_pipeline_config.artifact_dir,training_pipeline.MODEL_EVALUATION_DIR_NAME)
        self.report_file_path= Path(self.model_evaluation_dir,training_pipeline.MODEL_EVALUATION_REPORT_NAME)
        self.change_threshold = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE

class ModelPusherConfig:
     def __init__(self,training_pipeline_config:TrainingPipelineConfig):
         self.model_evaluation_dir:str=Path.joinpath(training_pipeline_config.artifact_dir,training_pipeline.MODEL_FILE_NAME)
         timestamp=round(datetime.now().timestamp())
         self.saved_model_path=Path.joinpath(training_pipeline.SAVED_MODEL_DIR,f"{timestamp}",training_pipeline.MODEL_FILE_NAME)



if __name__=='__main__':
    x=TrainingPipelineConfig()
    y=DataIngestionConfig(x)
    print(y.data_ingestion_dir)
    print(Path(y.feature_store_file_path).parent)
    with open(r"Artifact/08_24_2024_22_22_48/data_ingestion/feature_store/NetworkData.csv",mode='r') as f:
        print(f)
