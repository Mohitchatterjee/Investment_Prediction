from dataclasses import dataclass
@dataclass
class DataIngestionArtifact:
    featureStoreDIR:str
    trainingDataDIR:str
    testDataDIR:str 
@dataclass
class DataValidationArtifact:
    reportFilePath:str

@dataclass
class DataTransformationArtifact:
    # transformationObjPath:str
    X_TrainPath:str
    X_TestPath:str
    Y_TrainPath:str
    Y_TestPath:str

@dataclass
class ModelTranerArtifact:
    modelPath:str
    trainingAccuracy:float
    testingAccuracy:float

class ModelEvaluateArtifact:...
class ModelPusherArtifact:...