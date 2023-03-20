from Investment_Prediction.logger import logging
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.predictor import ModelResolver
import pandas as pd
import os,sys
from datetime import datetime
from Investment_Prediction.utils import load_object,addReleventFeatures
from Investment_Prediction.entity import config_entity
from Investment_Prediction.components.DataValidation import DataValidation
# from Investment_Prediction.components.DataTransformation import DataTransformation


PREDICTION_DIR = 'prediction'
 
def startBatchPrediction(inputFilePath):
    try:
        
        os.makedirs(PREDICTION_DIR,exist_ok=True)
        logging.info('Create Model Resolver Object in Batch Prediction')
        modelResolver = ModelResolver('saved_models') 
        logging.info('Reading Input File')
        DataFrame = pd.read_csv(inputFilePath)

        logging.info('Loading Transformer and Model Object')
        transformerObj = load_object(modelResolver.getLatestTransformerPath())
        modelObj = load_object(modelResolver.getLatestModelPath())
        
        
        logging.info('Data Validation initialize with new Data')
        trainingPipelineConfig = config_entity.TrainingPipeLineConfig()
        dataValidationConfig = config_entity.DataValidationConfig(trainingPipelineConfig)
        dataValidationConfig = DataValidation(dataValidationConfig)
        dataValidationArtifacts = dataValidationConfig.initiateDataValidationConfig(DataFrame)

        
        logging.info('Add releveant Feature to DataFrame')
        DataFrame = addReleventFeatures(DataFrame)
        featureDF = DataFrame[['open-close','low-high','is_quarter_end']]
        targetDF = DataFrame[['target']]
        
       
        logging.info('Transform the Data')
        transformedData = transformerObj.fit_transform(featureDF)

        
        logging.info('Predict Model')
        prediction = modelObj.predict_proba(transformedData)[:,1]
        
        featureDF['Actual'] = targetDF
        featureDF['Prediction'] = prediction


        # Take file name and add time stamp after fileName
        predictionFileName =  os.path.basename(inputFilePath).replace('.csv',f"{datetime.now().strftime('-%d-%m-%Y__%H:%M:%S')}.csv")
        predictionFileDir = os.path.join(PREDICTION_DIR,predictionFileName)
        featureDF.to_csv(predictionFileDir,index=False, header=True)

        return predictionFileDir
    except Exception as e:
        raise InvestmentPredictionException(e,sys)