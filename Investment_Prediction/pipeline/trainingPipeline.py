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
from Investment_Prediction.components.ModelEvaluation import ModelEvaluation
from Investment_Prediction.components.ModelPusher import ModelPusher

def startTrainingPipeline():

    try:
        trainingPipelineConfig = config_entity.TrainingPipeLineConfig()
        dataIngestionConfig = config_entity.DataIngestionConfig(trainingPipelineConfig)
        data_ingestion_config = DataIngestion(dataIngestionConfig)
        dataIngestionArtifacts = data_ingestion_config.initiateDataIngestionConfig()
        
        DataFrame = pd.read_csv(dataIngestionArtifacts.featureStoreDIR)
        
        dataValidationConfig = config_entity.DataValidationConfig(trainingPipelineConfig)
        dataValidationConfig = DataValidation(dataValidationConfig)
        dataValidationArtifacts = dataValidationConfig.initiateDataValidationConfig(DataFrame)

        dataTransformConfig = config_entity.DataTransformationConfig(trainingPipelineConfig)
        data_transformation_config = DataTransformation(dataTransformConfig,dataIngestionConfig)
        dataTransformationArtifacts = data_transformation_config.initiateDataTransformConfig(DataFrame)

        modelTrainingConfig = config_entity.ModelTrainerConfig(trainingPipelineConfig)
        model_trainer_config = ModelTrainer(modelTrainingConfig,dataTransformationArtifacts)
        modelTrainerArtifacts = model_trainer_config.initiateModelTraingConfig()

        
        modelEvaluationConfig = config_entity.ModelEvaluateConfig(trainingPipelineConfig)
        modelEvalConfig = ModelEvaluation(modelEvaluationConfig, dataIngestionArtifacts, dataTransformationArtifacts, modelTrainerArtifacts)
        modelEvalArtifacts = modelEvalConfig.initiateModelEvaluation()

        
        modelPusherConfig = config_entity.ModelPusherConfig(trainingPipelineConfig)
        modelPushConfig = ModelPusher(modelPusherConfig,dataTransformationArtifacts,modelTrainerArtifacts)
        modelPusherArtifacts = modelPushConfig.initiateModelPusherConfig()
    
    except Exception as e:
        raise InvestmentPredictionException(e,sys)