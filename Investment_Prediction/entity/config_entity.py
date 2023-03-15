import os
from datetime import datetime

class TrainingPipeLineConfig:
    def __init__(self):
        self.artifactDir = os.path.join(os.getcwd(),'artifacts',f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

class DataIngestionConfig:
    def __init__(self,trainingPipelineConfig):
        self.databaseName = 'Stocks_Name'
        self.colectionName = 'Price'
        self.dataIngestionDIR = os.path.join(trainingPipelineConfig.artifactDir,'Data Ingestion')
        self.featureStoreDIR = os.path.join(self.dataIngestionDIR,'DataSet.csv')
        self.trainingDataDIR = os.path.join(self.dataIngestionDIR,'TrainingData.csv')
        self.testDataDIR = os.path.join(self.dataIngestionDIR,'TestData.csv')
        
    def to_dict(self):
        return self.__dict__
        
class DataValidationConfig:
     def __init__(self,trainingPipelineConfig):
        self.dataValidationDIR = os.path.join(trainingPipelineConfig.artifactDir,'Data Validation')
        self.reportFilePath = os.path.join(self.dataValidationDIR,'report.yaml')
        self.missingThreshold = 0.2
        
class DataTransformationConfig:
    def __init__(self,trainingPipelineConfig):
        # self.dataTransformationDIR = os.path.join(trainingPipelineConfig.artifactDir,'Data Transformation')
        self.transformationObjPath = os.path.join(trainingPipelineConfig.artifactDir,'Data Transformation','transform.pkl')
        self.X_TrainPath = os.path.join(trainingPipelineConfig.artifactDir,'Data Transformation','X_train.npy')
        self.X_TestPath = os.path.join(trainingPipelineConfig.artifactDir,'Data Transformation','X_test.npy')
        self.Y_TrainPath = os.path.join(trainingPipelineConfig.artifactDir,'Data Transformation','Y_train.npy')
        self.Y_TestPath = os.path.join(trainingPipelineConfig.artifactDir,'Data Transformation','Y_test.npy')

class ModelTrainerConfig:
     def __init__(self,trainingPipelineConfig):
        self.modelTrainerDIR = os.path.join(trainingPipelineConfig.artifactDir,'Model Trainer')
        self.modelPath = os.path.join(self.modelTrainerDIR,'model','predictionModel.pkl')

class ModelEvaluateConfig:
    def __init__(self,trainingPipelineConfig):
        self.changeThreshold = 0.01
        


class ModelPusherConfig:
     def __init__(self,trainingPipelineConfig):
        self.dataPusherDIR = os.path.join(trainingPipelineConfig.artifactDir,'Data Pusher')
        self.outsideSavedModel = os.path.join('saved_models')
        
        self.insideSavedModel = os.path.join(self.dataPusherDIR,'saved_models')
        self.insideModelPath = os.path.join(self.insideSavedModel,'model.pkl')
        self.insideTransformerPath = os.path.join(self.insideSavedModel,'transformer.pkl')