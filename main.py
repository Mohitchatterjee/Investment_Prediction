import os, sys
import pandas as pd
from Investment_Prediction.utils import getCollectionAsDataFrame
from Investment_Prediction.logger import logging
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.entity import config_entity
from Investment_Prediction.components.DataIngestion import DataIngestion
from Investment_Prediction.components.DataValidation import DataValidation
from Investment_Prediction.components.DataTransformation import DataTransformation
from Investment_Prediction.components.ModelTrainer import ModelTrainer

if __name__ == "__main__":
    try:
       
        # data = getCollectionAsDataFrame(DataBaseName='Stocks_Price',CollectionName='Company')
        trainingPipelineConfig = config_entity.TrainingPipeLineConfig()
        dataIngestionConfig = config_entity.DataIngestionConfig(trainingPipelineConfig)
        data_ingestion_config = DataIngestion(dataIngestionConfig)
        dataIngestionConfig = data_ingestion_config.initiateDataIngestionConfig()
        
        DataFrame = pd.read_csv(dataIngestionConfig.featureStoreDIR)
        
        dataValidationConfig = config_entity.DataValidationConfig(trainingPipelineConfig)
        data_validation_config = DataValidation(dataValidationConfig)
        data_validation_config.initiateDataValidationConfig(DataFrame)

        dataTransformConfig = config_entity.DataTransformationConfig(trainingPipelineConfig)
        data_transformation_config = DataTransformation(dataTransformConfig,dataIngestionConfig)
        dataTransformationConfig = data_transformation_config.initiateDataTransformConfig(DataFrame)

        modelTrainingConfig = config_entity.ModelTrainerConfig(trainingPipelineConfig)
        model_trainer_config = ModelTrainer(modelTrainingConfig,dataTransformationConfig)
        modelTrainingConfig = model_trainer_config.initiateModelTraingConfig()

    except Exception as e:
        raise InvestmentPredictionException(e,sys)