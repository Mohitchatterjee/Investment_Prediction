from Investment_Prediction.predictor import ModelResolver
from Investment_Prediction.entity import config_entity,artifact_entity
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.components import DataTransformation
from Investment_Prediction.logger import logging
from Investment_Prediction.utils import load_object
from sklearn import metrics
import pandas as pd

class ModelEvaluation:
    def __init__(self,modelEvalConfig:config_entity.ModelEvaluateConfig,
    dataIngestionArtifacts:artifact_entity.DataIngestionArtifact,dataTransformationArtifacts:artifact_entity.DataTransformationArtifact,modelTrainerArtifacts:artifact_entity.ModelTrainerArtifact):

        try:
            self.modelEvalConfig = modelEvalConfig
            self.dataIngestionArtifacts = dataIngestionArtifacts
            self.dataTransformationArtifacts = dataTransformationArtifacts
            self.modelTrainerArtifacts = modelTrainerArtifacts
            self.modelResolver = ModelResolver()

        except Exception as e:
            raise e
        
    def initiateModelEvaluation(self):
        try:
            latestDirpath = self.modelResolver.getLatestDirPath()
            if latestDirpath == None:
                modelEvalArtifact = artifact_entity.ModelEvaluateArtifact(isModelAccepted=True, improveAccuracy=None)
                return modelEvalArtifact
            
            transformerPath = self.modelResolver.getLatestTransformerPath()
            modelPath = self.modelResolver.getLatestModelPath()

            # Previously Trained Object
            transformerObj = load_object(file_Path=transformerPath)
            modelObj = load_object(file_Path=modelPath)

            # Current Trained Object
            currentTransformerObj = load_object(file_Path=self.dataTransformationArtifacts.transformationObjPath)
            currentModelObj = load_object(file_Path=self.modelTrainerArtifacts.modelPath)

            testDF = pd.read_csv(self.dataIngestionArtifacts.testDataDIR)

            testDataFrame = DataTransformation.addReleventFeatures(testDF)
            featureDF = testDataFrame[['open-close','low-high','is_quarter_end']]
            targetDF = testDataFrame[['target']]

            # previous data accuracy
            inputArr = transformerObj.transform(featureDF) 
            y_pred = modelObj.predict_proba(inputArr)
            Previous_Validation_Accuracy = metrics.roc_auc_score(targetDF, modelObj.predict_proba(y_pred))

            # current data accuracy
            inputArr = currentTransformerObj.transform(featureDF) 
            y_pred = currentModelObj.predict_proba(inputArr)
            Current_Validation_Accuracy = metrics.roc_auc_score(targetDF, modelObj.predict_proba(y_pred))

            if Current_Validation_Accuracy < Previous_Validation_Accuracy:
                raise('Current Model Accuracy is not better than previous model..')
            
            modelEvalArtifact = artifact_entity.ModelEvaluateArtifact(isModelAccepted=True, improveAccuracy=Current_Validation_Accuracy-Previous_Validation_Accuracy)
            return modelEvalArtifact


        except Exception as e:
            raise e