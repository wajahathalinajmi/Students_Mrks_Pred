import logging
import os
import sys
from datetime import datetime
from src.exception import CustomException

try:
    dir_name = os.path.join(os.getcwd(), "logs")
    os.makedirs(dir_name, exist_ok=True)

    
    log_file = f"{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}.log"
    LOG_FILE_PATH = os.path.join(dir_name,log_file)

    for handler in logging.root.handlers:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        filename=LOG_FILE_PATH,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        level=logging.INFO,
)

except Exception as e:
    raise CustomException(e,sys)



