import os
import sys
import dill
from src.exception import CustomException

def save_object(filepath,obj):
    try:
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,"wb") as file_obj:
            dill.dump(obj,file_obj)

        return filepath
    except Exception as e:
        raise CustomException(e,sys)