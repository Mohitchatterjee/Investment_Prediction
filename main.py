import os, sys
from Investment_Prediction.utils import getCollectionAsDataFrame
from Investment_Prediction.logger import logging
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.entity import config_entity
from Investment_Prediction.components.DataIngestion import DataIngestion

if __name__ == "__main__":
    try:
        # data = getCollectionAsDataFrame(DataBaseName='Stocks_Price',CollectionName='Company')
        trainingPipelineConfig = config_entity.TrainingPipeLineConfig()
        dataIngestionConfig = config_entity.DataIngestionConfig(trainingPipelineConfig)
        print(dataIngestionConfig.to_dict())
        data_ingestion_config = DataIngestion(dataIngestionConfig)
        print(data_ingestion_config.initiateDataIngestionConfig())

    except Exception as e:
        raise InvestmentPredictionException(e,sys)