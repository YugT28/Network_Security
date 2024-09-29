import os
import sys
import pandas as pd
import numpy as np
from network_security.exception.exception import NetworkSecurityException
from network_security.logger.logger import logging
from network_security.utils.ml_utils.model.estimator import ModelResolver
from network_security.utils.main_utils.utils import load_object
from datatime import datetime
from network_security.constant.training_pipeline import PRECTION_DIR
from network_security.constant.training_pipeline import SAVED_MODEL_DIR

print(PRECTION_DIR)

def start_batch_prediction(input_file_path):
    try:
        os.makedirs(PRECTION_DIR,exist_ok=True)

        logging.info(f"creating model resolver object")
        model = ModelResolver(model_dir=SAVED_MODEL_DIR)
        latest_model_path = model.get_best_model_path()

        logging.info(f"Reading file : {input_file_path}")
        df=pd.read_csv(input_file_path)

        input_arr=df.values

        logging.info(f"Target encoder to convert predicted column into categorical")
        latest_model = load_object(file_path=latest_model_path)

        prediction = latest_model.predict(input_arr)

        df['prediction']=prediction

        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PRECTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path,index=False,header=True)
        return prediction_file_path
    except Exception as e:
        raise NetworkSecurityException(e,sys)







