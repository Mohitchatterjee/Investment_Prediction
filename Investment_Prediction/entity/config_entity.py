import os
from datetime import datetime

class TrainingPipeLineConfig:
    def __init__(self):
        self.artifactDir = os.path.join(os.getcwd(),'artifacts',f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")

class DataIngestionConfig:
    def __init__(self,trainingPipelineConfig):
        self.databaseName = 'Stocks_Price'
        self.colectionName = 'Company'
        self.dataIngestionDIR = os.path.join(trainingPipelineConfig.artifactDir,'Data Ingestion')
        self.featureStoreDIR = os.path.join(self.dataIngestionDIR,'StocksPrice')
        self.trainingDataDIR = os.path.join(self.featureStoreDIR,'TrainingData.csv')
        self.testDataDIR = os.path.join(self.featureStoreDIR,'TestData.csv')
        
    def to_dict(self):
        return self.__dict__
        
class DataValidationConfig:...
class DataTransformationConfig:...
class ModelTranerConfig:...
class ModelEvaluateConfig:...
class ModelPusherConfig:...