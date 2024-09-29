from network_security.exception.exception import NetworkSecurityException
from network_security.logger.logger import logging

from network_security.entity.artifact_entity import ModelPusherArtifact, ModelTrainerArtifact,ModelEvaluationArtifact
from network_security.entity.config_entity import ModelEvaluationConfig,ModelPusherConfig

import os,sys

from network_security.utils.ml_utils.metric.classification_metric import get_classification_score
from network_security.utils.main_utils.utils import save_object, load_object, write_yaml_file

import shutil

from pathlib import Path


class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,model_eval_artifact:ModelEvaluationArtifact):
        try:
            self.model_pusher_config = model_pusher_config
            self.model_eval_artifact = model_eval_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_model_pusher(self)->ModelPusherArtifact:
        try:
            trained_model_path= self.model_eval_artifact.trained_model_path

            model_file_path = self.model_pusher_config.model_evaluation_dir

            # Creating model pusher dir to save model
            dir_name=Path(model_file_path)
            dir_name.mkdir(exist_ok=True,parents=True)
            shutil.copy(src=trained_model_path,dst=model_file_path)

            #saved model dir
            saved_model_path = self.model_pusher_config.saved_model_path
            dir_name=Path(saved_model_path).parent
            dir_name.mkdir(exist_ok=True,parents=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)

            #preparing artifact
            model_pusher_artifact = ModelPusherArtifact(saved_model_path=saved_model_path,model_file_path=model_file_path)
            return model_pusher_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)


