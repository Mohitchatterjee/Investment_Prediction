from Investment_Prediction.predictor import ModelResolver
from Investment_Prediction.entity import artifact_entity,config_entity
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.logger import logging
import os,sys
from Investment_Prediction.utils import load_object,save_object

class ModelPusher:
    def __init__(self,modelPusherConfig:config_entity.ModelPusherConfig,
                dataTransformerArtifact:artifact_entity.DataTransformationArtifact,
                modelTrainerArtifact:artifact_entity.ModelTrainerArtifact):
        try:
            self.modelPusherConfig = modelPusherConfig
            self.dataTransformerArtifact = dataTransformerArtifact
            self.modelTrainerArtifact =modelTrainerArtifact
            self.modelResolver = ModelResolver(modelRegistry=self.modelPusherConfig.outsideSavedModel)

        except Exception as e:
            InvestmentPredictionException(e,sys)

    def initiateModelPusherConfig(self):
        try:
            
            # Load Obj
            transformer = load_object(self.dataTransformerArtifact.transformationObjPath)
             
            model = load_object(self.modelTrainerArtifact.modelPath)
            
            # save Obj
            
            save_object(self.modelPusherConfig.insideModelPath,obj=model)
            
            save_object(self.modelPusherConfig.insideTransformerPath,obj=transformer)
            
            
            
            modelPath = self.modelResolver.getLatestSaveModelPath()
            print(modelPath)
            transformerPath = self.modelResolver.getLatestTransformerPath()
            print(transformerPath)
            
            save_object(file_Path=modelPath,obj=model)
            save_object(file_Path=transformerPath,obj=transformer)

            modelPusherArtifacts = artifact_entity.ModelPusherArtifact(dataPusherDIR=self.modelPusherConfig.insideSavedModel,
            savedModelDIR=self.modelPusherConfig.outsideSavedModel)
            print('Model Pusher Done...')
            return modelPusherArtifacts

        except Exception as e:
            InvestmentPredictionException(e,sys)