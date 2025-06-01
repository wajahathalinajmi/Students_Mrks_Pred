import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_path:str = os.path.join("collection", "preprocessor.pkl")

class TransformationConfig:
    def __init__(self):
        self.Tranformation_config = DataTransformationConfig()

    def get_data_transformer(self,train_data_path,test_data_path):
        try:
            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_data_path)

            combined_df = pd.concat([train_data.drop(columns=['math_score']), test_data.drop(columns=['math_score'])])
            num_columns = combined_df.select_dtypes(include=np.number).columns.to_list()
            cat_columns = combined_df.select_dtypes(exclude=np.number).columns.to_list()

            logging.info(f"Numerical columns: {num_columns}")
            logging.info(f"Categorical columns: {cat_columns}")

            num_pipeline = Pipeline(
                steps=[
                    ("simple_imputing", SimpleImputer(strategy="median")),
                    ("scaling", StandardScaler()),
                ]
                )
            
            cat_pipeline = Pipeline(
                steps=[
                    ("simple_imputing", SimpleImputer(strategy="most_frequent")),
                    ("encoding", OneHotEncoder(handle_unknown="ignore", sparse=True)),
                ]
            )

            preprocessor = ColumnTransformer(transformers=[
                ("numerical_tranformation", num_pipeline, num_columns),
                ("categorical_tranformation", cat_pipeline, cat_columns),
            ]
            )

            logging.info("data transformation has initiated")


            target_feature = 'math_score'
            input_feature_train_data = train_data.drop(columns = [target_feature], axis=1)
            target_feature_train = train_data[target_feature]
            input_feature_test_data = test_data.drop(columns = [target_feature], axis=1)
            target_feature_test = test_data[target_feature]

            logging.info("fit tranform is about to begin")

            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_data)
            input_feature_test_arr = preprocessor.transform(input_feature_test_data)
            

            logging.info("features are tranformed succssfully")
            logging.info(f"Shape of input_feature_train_arr: {input_feature_train_arr.shape}")
            logging.info(f"Reshaped target_feature_train: {target_feature_train.values.reshape(-1, 1).shape}")
            logging.info(f"Shape of target_feature_train: {target_feature_train.shape}")


            train_arr = np.c_[
                            input_feature_train_arr,
                            target_feature_train.values.reshape(-1, 1)
                        ]
            test_arr = np.c_[
                            input_feature_test_arr,
                            target_feature_test.values.reshape(-1, 1)
                        ]

            logging.info("concatenation succesfull")

            save_object(
                filepath=self.Tranformation_config.preprocessor_obj_path,
                obj=preprocessor
            )

            logging.info("processor saved successfuly")

            return train_arr,test_arr
   
        except Exception as e:
            raise CustomException(e,sys)
        

