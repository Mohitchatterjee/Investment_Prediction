from Investment_Prediction.predictor import ModelResolver
from Investment_Prediction.entity import config_entity,artifact_entity
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.components.DataTransformation import DataTransformation
from Investment_Prediction.logger import logging
from Investment_Prediction.utils import load_object
from Investment_Prediction import utils
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
            # self.dataTransformationConfig = dataTransformationConfig
            # self.dataTransformer = DataTransformation

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
            transformerObj = load_object(transformerPath)
            modelObj = load_object(modelPath)

            # Current Trained Object
            currentTransformerObj = load_object(self.dataTransformationArtifacts.transformationObjPath)
            currentModelObj = load_object(self.modelTrainerArtifacts.modelPath)

            # testDF = pd.read_csv(self.dataIngestionArtifacts.testDataDIR)

            # testDataFrame = DataTransformation.addReleventFeatures(self,testDF)

            X_test = utils.load_numpy_array_data(self.dataTransformationArtifacts.X_TestPath)
            Y_test = utils.load_numpy_array_data(self.dataTransformationArtifacts.Y_TestPath)
            
            # featureDF = testDataFrame[['open-close','low-high','is_quarter_end']]
            # targetDF = testDataFrame[['target']]

            # previous data accuracy
            # inputArr = transformerObj.transform(featureDF)           
            Previous_Validation_Accuracy = metrics.roc_auc_score(Y_test, modelObj.predict_proba(X_test)[:,1])
            
            # current data accuracy
            # inputArr = currentTransformerObj.transform(featureDF) 
            Current_Validation_Accuracy = metrics.roc_auc_score(Y_test, currentModelObj.predict_proba(X_test)[:,1])

            print('Current Data Accuracy-->',Current_Validation_Accuracy)
            print('Previous Data Accuracy-->', Previous_Validation_Accuracy)

            if Current_Validation_Accuracy < Previous_Validation_Accuracy:
                raise('Current Model Accuracy is not better than previous model..')
            
            print('Model Evaluation done...')
            modelEvalArtifact = artifact_entity.ModelEvaluateArtifact(isModelAccepted=True, improveAccuracy=Current_Validation_Accuracy-Previous_Validation_Accuracy)
            return modelEvalArtifact


        except Exception as e:
            raise e