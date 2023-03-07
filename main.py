import os, sys
import pandas as pd
from Investment_Prediction.utils import getCollectionAsDataFrame
from Investment_Prediction.logger import logging
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.entity import config_entity
from Investment_Prediction.components.DataIngestion import DataIngestion
from Investment_Prediction.components.DataValidation import DataValidation

if __name__ == "__main__":
    try:
        # data = getCollectionAsDataFrame(DataBaseName='Stocks_Price',CollectionName='Company')
        trainingPipelineConfig = config_entity.TrainingPipeLineConfig()
        dataIngestionConfig = config_entity.DataIngestionConfig(trainingPipelineConfig)
        data_ingestion_config = DataIngestion(dataIngestionConfig)
        
        trainingDataFrame = pd.read_csv(data_ingestion_config.initiateDataIngestionConfig().trainingDataDIR)
        
        dataValidationConfig = config_entity.DataValidationConfig(trainingPipelineConfig)
        data_validation_config = DataValidation(dataValidationConfig)
        data_validation_config.initiateDataValidationConfig(trainingDataFrame)

    except Exception as e:
        raise InvestmentPredictionException(e,sys)