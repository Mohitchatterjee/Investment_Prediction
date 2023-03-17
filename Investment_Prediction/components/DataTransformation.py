from Investment_Prediction.entity import config_entity
from Investment_Prediction.entity import artifact_entity
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.logger import logging
from sklearn.pipeline import Pipeline
import os,sys
import pandas as pd
import numpy as np
from numpy import savetxt
from Investment_Prediction import utils
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


class DataTransformation:
    def __init__(self,dataTransformationConfig:config_entity.DataTransformationConfig,
                dataIngestionArtifact:artifact_entity.DataValidationArtifact):
            try:
                self.dataTransformationConfig = dataTransformationConfig
                self.dataIngestionArtifact = dataIngestionArtifact
                

            except Exception as e:
                raise InvestmentPredictionException(e,sys) 
    
    

    def addReleventFeatures(self,DataFrame):
        try:

            splitted = DataFrame['Date'].str.split('-', expand=True)
            DataFrame['day'] = splitted[1].astype('int')
            DataFrame['month'] = splitted[2].astype('int')
            DataFrame['year'] = splitted[0].astype('int')


            DataFrame['is_quarter_end'] = np.where(DataFrame['month']%3==0,1,0)
            DataFrame['open-close']  = DataFrame['Open'] - DataFrame['Close']
            DataFrame['low-high']  = DataFrame['Low'] - DataFrame['High']

            # if today's price is greater than yesterday's price then 1
            DataFrame['target'] = np.where(DataFrame['Close'].shift(-1) > DataFrame['Close'], 1, 0)

            return DataFrame
            
        except Exception as e:
            raise InvestmentPredictionException(e,sys)

    def getTransformerObj(self):
        try:
            scaler = StandardScaler()
            return scaler

        except Exception as e:
            raise InvestmentPredictionException(e,sys)  
    
    def splitingData(self,featureData,targetData):
        try:

            X_train, X_valid, Y_train, Y_valid = train_test_split(
            featureData, targetData, test_size=0.2, random_state=55)
           
            return X_train, X_valid, Y_train, Y_valid

        except Exception as e:
            raise InvestmentPredictionException(e,sys)  
    
    def initiateDataTransformConfig(self,DataFrame):
        try:
            logging.info('==============> Data Transformation <===============')

            logging.info('Adding Relevant Features')
            DataFrame = self.addReleventFeatures(DataFrame)

            logging.info('Create New DataFrame')
            featureDF = DataFrame[['open-close','low-high','is_quarter_end']]
            targetDF = DataFrame[['target']]

            logging.info('Transform Dataframe')
            transformerOBJ = self.getTransformerObj()
            scaledData = transformerOBJ.fit_transform(featureDF)

            logging.info('Splitting Data')
            X_train, X_test, Y_train, Y_test = self.splitingData(scaledData,targetDF)
            
            logging.info('Split Data Saving...')
            X_TrainPath = os.path.dirname(self.dataTransformationConfig.X_TrainPath)
            os.makedirs(X_TrainPath,exist_ok=True)
            np.save(self.dataTransformationConfig.X_TrainPath, X_train, allow_pickle=True)
            

            X_TestPath = os.path.dirname(self.dataTransformationConfig.X_TrainPath)
            os.makedirs(X_TestPath,exist_ok=True)
            np.save(self.dataTransformationConfig.X_TestPath, X_test, allow_pickle=True)
            

            Y_TrainPath = os.path.dirname(self.dataTransformationConfig.Y_TrainPath)
            os.makedirs(Y_TrainPath,exist_ok=True)
            np.save(self.dataTransformationConfig.Y_TrainPath, Y_train, allow_pickle=True)
            

            Y_TestPath = os.path.dirname(self.dataTransformationConfig.Y_TrainPath)
            os.makedirs(Y_TestPath,exist_ok=True)
            np.save(self.dataTransformationConfig.Y_TestPath, Y_test, allow_pickle=True)
            
            print('Data Transformation Done...')

            logging.info('Transformer Object is saving...')
            utils.save_object(file_path=self.dataTransformationConfig.transformationObjPath,obj=transformerOBJ)

            logging.info('Preparing Data Transformer Artifacts')
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transformationObjPath=self.dataTransformationConfig.transformationObjPath,
                X_TrainPath=self.dataTransformationConfig.X_TrainPath,
                X_TestPath=self.dataTransformationConfig.X_TestPath,
                Y_TrainPath=self.dataTransformationConfig.Y_TrainPath,
                Y_TestPath=self.dataTransformationConfig.Y_TestPath
            )

            return data_transformation_artifact



        except Exception as e:
            raise InvestmentPredictionException(e,sys)   






    # def gettingTransformDataFrame(self,UpdatedDataFrame):
    #     try:
    #         featureDF = UpdatedDataFrame[['open-close'],['low-high'],['is_quarter_end']]
    #         targetDF = UpdatedDataFrame[['target']]

           

    #         return DataFrame

    #     except Exception as e:
    #             raise InvestmentPredictionException(e,sys) 

    