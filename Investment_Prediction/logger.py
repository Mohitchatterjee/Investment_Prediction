import logging
import os
from datetime import datetime 

LogFileName = f"{datetime.now().strftime('%m%d%Y_%H%M%S')}.log"

LogDirectory = os.path.join(os.getcwd(),'logs')

os.mkdirs(LogDirectory,exist_ok=True)