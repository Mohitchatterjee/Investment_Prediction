import pymongo
import json
import pandas as pd
from Investment_Prediction.config import Mongo_client


# client = pymongo.MongoClient('mongodb+srv://mohit:mohit@cluster0.frbovmx.mongodb.net/test')
# client = pymongo.MongoClient('mongodb+srv://mohit:mohit@cluster0.ietyo8r.mongodb.net/test')
DataBaseName = 'Stocks_Name'
CollectionName = 'Price'
DataSetPath = '/config/workspace/GOOG.csv'

if __name__ == '__main__':
    data = pd.read_csv(DataSetPath)

    #convert Data into Json
    data.reset_index(drop=True, inplace=True)
    json_Data = (json.loads(data.T.to_json(path_or_buf=None, orient=None, date_format=None, double_precision=10, force_ascii=True, date_unit='ms', default_handler=None, lines=False, compression='infer', index=True)))

    ListjsonData = []
    for _ in json_Data.values():ListjsonData.append(_)

# Dumb Json data into mongoDB
Mongo_client[DataBaseName][CollectionName].insert_many(ListjsonData)