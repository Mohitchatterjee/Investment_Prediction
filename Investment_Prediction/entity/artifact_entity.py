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
    transformationObjPath:str
    X_TrainPath:str
    X_TestPath:str
    Y_TrainPath:str
    Y_TestPath:str

@dataclass
class ModelTrainerArtifact:
    modelPath:str
    trainingAccuracy:float
    testingAccuracy:float

@dataclass
class ModelEvaluateArtifact:
    isModelAccepted:bool
    improveAccuracy:float

@dataclass
class ModelPusherArtifact:
    dataPusherDIR:str
    savedModelDIR:str