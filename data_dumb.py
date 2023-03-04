import pymongo
import json
import pandas as pd

client = pymongo.MongoClient('mongodb+srv://mohit:mohit@cluster0.frbovmx.mongodb.net/test')

DataBaseName = 'Stocks_Price'
CollectionName = 'Company'
DataSetPath = '/config/workspace/Google_Stock_Price_Train.csv'

if __name__ == '__main__':
    data = pd.read_csv(DataSetPath)

    #convert Data into Json
    data.reset_index(drop=True, inplace=True)
    json_Data = (json.loads(data.T.to_json(path_or_buf=None, orient=None, date_format=None, double_precision=10, force_ascii=True, date_unit='ms', default_handler=None, lines=False, compression='infer', index=True)))

    ListjsonData = []
    for _ in json_Data.values():ListjsonData.append(_)

# Dumb Json data into mongoDB
client[DataBaseName][CollectionName].insert_many(ListjsonData)