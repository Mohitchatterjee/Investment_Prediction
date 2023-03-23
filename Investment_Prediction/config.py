import pymongo
import json
import os
import pandas as pd
from dataclasses import dataclass

class EnviromentVariable():
    MongoDbUrl = os.getenv('MongoDbUrl')


envVar = EnviromentVariable()
Mongo_client = pymongo.MongoClient(envVar.MongoDbUrl)

