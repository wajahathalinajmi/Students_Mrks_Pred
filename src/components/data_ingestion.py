import os
import sys
from src.logger import logging
from src.exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.utils import save_object

from src.components.data_transformation import DataTransformationConfig
from src.components.data_transformation import TransformationConfig
@dataclass
class DataingestionConfig:
    train_data_path: str = os.path.join("collection", "train.csv")
    test_data_path: str = os.path.join("collection", "test.csv")
    raw_data_path: str = os.path.join("collection", "data.csv")

class DataConfig:
    def __init__(self):
        self.ingestion_config = DataingestionConfig()

    def initiate_data_ingestion(self):
        logging.info("data ingestion has begun")
        try:
            file_dir = os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df = pd.read_csv("data/stud.csv")
            train_data,test_data = train_test_split(df,test_size=0.2,random_state=42)

            logging.info("train,test split done succesfully")

            train_data.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_data.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("files saved succesfully")
            train_path = self.ingestion_config.train_data_path
            test_path = self.ingestion_config.test_data_path

            return train_path,test_path

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    obj = DataConfig()
    train_path, test_path = obj.initiate_data_ingestion()

    Tranformation_obj = TransformationConfig()
    train_arr, test_arr = Tranformation_obj.get_data_transformer(train_data_path=train_path, test_data_path=test_path)

