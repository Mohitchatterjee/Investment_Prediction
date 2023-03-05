import pandas as pd
import os
from Investment_Prediction import utils
from Investment_Prediction.entity import config_entity
from Investment_Prediction.entity import artifact_entity
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.logger import logging
from Investment_Prediction.utils import getCollectionAsDataFrame

class DataIngestion:
    def __init__(self,dataIngestionConfig:config_entity.DataIngestionConfig):
        self.dataIngestionConfig = dataIngestionConfig
    
    def initiateDataIngestionConfig(self):
        df =  getCollectionAsDataFrame(DataBaseName=self.dataIngestionConfig.databaseName,
                                       CollectionName=self.dataIngestionConfig.colectionName)

        featureStorePath = os.path.dirname(self.dataIngestionConfig.featureStoreDIR)
        os.makedirs(featureStorePath,exist_ok=True)

        df.to_csv(path_or_buf=self.dataIngestionConfig.featureStoreDIR,index=False)
        
        #Prepare artifact

        data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                featureStoreDIR=self.dataIngestionConfig.dataIngestionDIR,
            trainingDataDIR=self.dataIngestionConfig.trainingDataDIR, 
            testDataDIR=self.dataIngestionConfig.testDataDIR)

        return data_ingestion_artifact     