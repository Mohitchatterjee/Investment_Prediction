import pandas as pd
import os
from Investment_Prediction import utils
from Investment_Prediction.entity import config_entity
from Investment_Prediction.entity import artifact_entity
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.logger import logging
from Investment_Prediction.utils import getCollectionAsDataFrame
from sklearn.model_selection import train_test_split

class DataIngestion:
    def __init__(self,dataIngestionConfig:config_entity.DataIngestionConfig):
        self.dataIngestionConfig = dataIngestionConfig
    
    def initiateDataIngestionConfig(self):
        try:
            df =  getCollectionAsDataFrame(DataBaseName=self.dataIngestionConfig.databaseName,
                                        CollectionName=self.dataIngestionConfig.colectionName)


            trainData,testData = train_test_split(df,test_size=0.2,random_state=55)

            featureStorePath = os.path.dirname(self.dataIngestionConfig.featureStoreDIR)
            os.makedirs(featureStorePath,exist_ok=True)

            # trainingPath = os.path.dirname(self.dataIngestionConfig.trainingDataDIR)
            # os.makedirs(trainingPath,exist_ok=True)

            # testPath = os.path.dirname(self.dataIngestionConfig.testDataDIR)
            # os.makedirs(testPath,exist_ok=True)

            df.to_csv(path_or_buf=self.dataIngestionConfig.featureStoreDIR,index=False)  
            # testData.to_csv(path_or_buf=self.dataIngestionConfig.testDataDIR,index=False)

            #Prepare artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                    featureStoreDIR=self.dataIngestionConfig.featureStoreDIR,
                trainingDataDIR=self.dataIngestionConfig.trainingDataDIR, 
                testDataDIR=self.dataIngestionConfig.testDataDIR)
            
            return data_ingestion_artifact    
        except Exception as e:
            raise InvestmentPredictionException(e,sys)