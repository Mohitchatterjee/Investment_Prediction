from Investment_Prediction.entity import config_entity
from Investment_Prediction.entity import artifact_entity
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.logger import logging
from Investment_Prediction import utils
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import os,sys
import pickle

class ModelTrainer:

    def __init__(self,modelTrainingConfig:config_entity.ModelTrainerConfig,
                      dataTransformationConfig:config_entity.DataTransformationConfig):
        try:
            self.modelTrainingConfig = modelTrainingConfig
            self.dataTransformationConfig = dataTransformationConfig

        except Exception as e:
                raise InvestmentPredictionException(e,sys)


    def trainModel(self,X_train,Y_train):
        try:
            LR = LogisticRegression()
            LR.fit(X_train,Y_train)
            return LR
        except Exception as e:
            raise InvestmentPredictionException(e,sys)

    def initiateModelTraingConfig(self):
        try:
            
            X_train = utils.load_numpy_array_data(self.dataTransformationConfig.X_TrainPath)
            Y_train = utils.load_numpy_array_data(self.dataTransformationConfig.Y_TrainPath)
            X_test = utils.load_numpy_array_data(self.dataTransformationConfig.X_TestPath)
            Y_test = utils.load_numpy_array_data(self.dataTransformationConfig.Y_TestPath)
           

            ModelObj = self.trainModel(X_train,Y_train)
            
            Training_Accuracy = metrics.roc_auc_score(Y_train, ModelObj.predict_proba(X_train)[:,1])

            Validation_Accuracy = metrics.roc_auc_score(Y_test, ModelObj.predict_proba(X_test)[:,1])

            modelPath = os.path.dirname(self.modelTrainingConfig.modelPath)
            os.makedirs(modelPath,exist_ok=True)

            pickle.dump(ModelObj, open(self.modelTrainingConfig.modelPath, 'wb'))

            model_training_artifact = artifact_entity.ModelTranerArtifact(
                modelPath=modelPath,
                trainingAccuracy=Training_Accuracy,
                testingAccuracy=Validation_Accuracy
            )
            print('Model Training Done...')
            return model_training_artifact
        except Exception as e:
            raise InvestmentPredictionException(e,sys)