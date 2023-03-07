from Investment_Prediction.entity import config_entity
from Investment_Prediction.entity import artifact_entity
from Investment_Prediction.exception import InvestmentPredictionException
from Investment_Prediction.logger import logging
from scipy.stats import ks_2samp
import os,sys
import pandas as pd
from Investment_Prediction import utils


class DataValidation:
    def __init__(self,dataValidationConfig:config_entity.DataValidationConfig):
        try:
            logging.info('====Data Validation===')
            self.dataValidationConfig = dataValidationConfig   
            self.validationError = dict() 
        except Exception as e:
            raise InvestmentPredictionException(e,sys) 
    

    def dropMissingColumn(self,df):
        try:
            threshold = self.dataValidationConfig.missingThreshold
            missingColumnList = []
            for i,j in zip((df.isnull().sum()/df.shape[0]).index,(df.isnull().sum()/df.shape[0]).values):
                if j > threshold:
                    missingColumnList.append(i)
                    self.validationError['Dropped_Columns'] = i
            df.drop(missingColumnList,axis=1,inplace=True)
            if len(df.columns) == 0:
                return None
            return df
        except Exception as e:
            raise InvestmentPredictionException(e,sys) 


    def isRequiredColumsExist(self,base_df, present_df):
        try:
            base_columns = base_df.columns
            present_columns = present_df.columns
            missingColumnListAfterDrop = []
            for baseCol in base_columns:
                if baseCol not in present_columns:
                    missingColumnListAfterDrop.append(baseCol)
            
            if len(missingColumnListAfterDrop) > 0:
                self.validationError['Missing Columns'] = missingColumnListAfterDrop
                return False
            return True
            
        except Exception as e:
            raise InvestmentPredictionException(e,sys) 

    
    def dataDrift(self, base_df, present_df):
        try:
            driftReport = dict()
            base_columns = base_df.columns
            present_columns = present_df.columns

            for baseCol in base_columns:
                baseData, currentData = base_df[baseCol],present_df[baseCol]
                sameDistribution = ks_2samp(baseData,currentData)
                                
                if sameDistribution.pvalue > 0.5:
                    driftReport[baseCol] = {
                        "p-value":float(sameDistribution.pvalue),
                        "same Distribution": True
                    }
                else:
                    driftReport[baseCol] = {
                        "p-value":float(sameDistribution.pvalue),
                        "same Distribution": False
                    }

            return driftReport

        except Exception as e:
            raise InvestmentPredictionException(e,sys)
            

    def initiateDataValidationConfig(self,df):
        try:
            presentDataFrame = self.dropMissingColumn(df)

            if self.isRequiredColumsExist(df,presentDataFrame):print('All Good in Validation Part')
            else:print('Column Mistmatch !!')

            driftReport = self.dataDrift(df,presentDataFrame)

            utils.insertintoYamlFile(self.dataValidationConfig.reportFilePath,driftReport)


        except Exception as e:
            raise InvestmentPredictionException(e,sys)

    