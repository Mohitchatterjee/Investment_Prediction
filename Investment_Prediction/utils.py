import pandas as pd
from Investment_Prediction.logger import logging
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.config import Mongo_client
import os,sys
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