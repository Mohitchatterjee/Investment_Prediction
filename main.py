from Investment_Prediction.pipeline.trainingPipeline import startTrainingPipeline 
from Investment_Prediction.pipeline.batchPrediction import startBatchPrediction

if __name__ == "__main__":
    try:
        filePath = '/config/workspace/GOOG.csv'
        # startTrainingPipeline()
        print(startBatchPrediction(filePath))

    except Exception as e:
        raise InvestmentPredictionException(e,sys)