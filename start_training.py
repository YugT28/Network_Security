#Master File
import os
import sys


#import logging and exception
from network_security.logger.logger import logging
from network_security.exception.exception import NetworkSecurityException

#importing class we are using in the file
from network_security.pipeline.training_pipeline import TrainingPipeline

def start_training():
    try:
        model_training=TrainingPipeline()           #creAting obejct
        model_training.run_pipeline()               #master method
    except Exception as e:
        raise NetworkSecurityException(e,sys)

if __name__ == '__main__':
    start_training()