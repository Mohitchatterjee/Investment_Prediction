import pandas as pd
import numpy as np
from Investment_Prediction.logger import logging
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.config import Mongo_client
import os,sys
import yaml
import csv
import dill

def getCollectionAsDataFrame(DataBaseName,CollectionName):
    try:
        df = pd.DataFrame(list(Mongo_client[DataBaseName][CollectionName].find()))
        if '_id' in df.columns:
            df = df.drop('_id',axis=1)
        logging.info('Reading data from mongo db')
        logging.info(f'Found Column : {df.columns}')
        return df
    except Exception as e:
        raise InvestmentPredictionException(e,sys)

def insertintoYamlFile(filePath,data):
    file_Path = os.path.dirname(filePath)
    os.makedirs(file_Path,exist_ok=True)
    
    with open(filePath,'w') as file:
        yaml.dump(data,file)

def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise InvestmentPredictionException(e,sys)

def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        print(str(e))
        raise InvestmentPredictionException(e, sys)

def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:return dill.load(file_obj)
    except Exception as e:
        print(str(e))
        raise InvestmentPredictionException(e, sys) from e
