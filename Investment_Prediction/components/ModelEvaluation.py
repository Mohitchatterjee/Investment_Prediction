from Investment_Prediction.predictor import ModelResolver
from Investment_Prediction.entity import config_entity,artifact_entity
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.logger import logging
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
        except Exception as e:
            raise e