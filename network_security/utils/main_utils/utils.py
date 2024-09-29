import yaml
from pathlib import Path
from network_security.exception.exception import NetworkSecurityException
from network_security.logger.logger import logging

import os,sys

import numpy as np
import pandas as pd

import dill   #dill can be used to store Python objects to a file
import pickle


def read_yaml_file(file_path: str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def write_yaml_file(file_path: str, content: object,replace: bool= False)-> None:
    try:
        if replace:
            if Path(file_path).exists():
                Path(file_path).unlink()
        x = Path(file_path).parent
        x.mkdir(parents=True, exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path=Path(file_path).parent
        dir_path.mkdir(exist_ok=True,parents=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_numpy_array_data(file_path: str) -> np.array:
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
def save_object(file_path: str,obj: object)->None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        dir_path=Path(file_path).parent
        dir_path.mkdir(exist_ok=True,parents=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e,sys)

#load object
def load_object(file_path:Path)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys)

