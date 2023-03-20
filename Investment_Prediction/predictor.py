import os
from typing import Optional

class ModelResolver:

    def __init__(self,modelRegistry:str='saved_models',modelPath='model', transformerDirName="transformer"):
        self.modelRegistry = modelRegistry
        self.modelPath = modelPath
        self.transformerDirName = transformerDirName
        os.makedirs(self.modelRegistry,exist_ok=True)
                
    def getLatestDirPath(self):
        try:
           
            dirName = os.listdir(self.modelRegistry)
            
            if len(dirName) == 0:
                return None
            dirName = list(map(int,dirName))
            latestFolderName = max(dirName)
            
            return os.path.join(self.modelRegistry,f"{latestFolderName}")
        except Exception as e:
            raise e

    

    def getLatestModelPath(self):
        try:
            latest_dir = self.getLatestDirPath()
            if latest_dir is None:
                raise Exception(f"Model is not available")
            return os.path.join(latest_dir,self.modelPath,'predictionModel.pkl')
        except Exception as e:
            raise e

    def getLatestTransformerPath(self):
        try:
            latestpath = self.getLatestDirPath()
            if latestpath is None:
                raise Exception(f"Transformer is not available")    
            return os.path.join(latestpath,self.transformerDirName,'transformer.pkl')      
        except Exception as e:
            raise e


    def getLatestSaveDirPath(self):
        try:
            latestDir = self.getLatestDirPath()    
            if latestDir == None:
               return os.path.join(self.modelRegistry,'0') 
            latestDirNum = int(os.path.basename(self.getLatestDirPath()))
            return os.path.join(self.modelRegistry,f"{latestDirNum+1}")   
        except Exception as e:
            raise e  
  
    def getLatestSaveModelPath(self):
        try:
            latestModel = self.getLatestSaveDirPath()       
            return os.path.join(latestModel,self.modelPath,'predictionModel.pkl')
        except Exception as e:
            raise e

    def getLatestSaveTransformerPath(self):
        try:
            latestModel = self.getLatestSaveDirPath()        
            return os.path.join(latestModel,self.transformerDirName,'transformer.pkl')
        except Exception as e:
            raise e

    

class Predictor:
    def __init__(self,modelResolver:ModelResolver):
        self.modelResolver = modelResolver

    