import os 
import sys
import pandas as pd
from src.utils import CustomException
from src.logger import logging
from src.utils import save_object
from dataclasses import dataclass
from src.utils import evaluate_model

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
import catboost

@dataclass
class ModelTrainerConfig:
    model_file_path: str = os.path.join("collection", "model.pkl")

class TrainerConfig:
    def __init__(self):
        self.trainer_config = ModelTrainerConfig()

    def initiate_model_training(self,train_arr,test_arr):
        logging.info("model ttaining is initiated")
        try:
            X_train,y_train,X_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            models = {
                    "linear_regression": LinearRegression(),
                    "ridge": Ridge(),
                    "lasso": Lasso(),
                    
                    "decision_tree_regressor": DecisionTreeRegressor(),
                    "random_forest_regressor": RandomForestRegressor(),
                    "gradient_boosting_regressor": GradientBoostingRegressor(),
                    "ada_boost_regressor": AdaBoostRegressor(),
                    
                    "svr": SVR(),
                    "knn_regressor": KNeighborsRegressor(),

                    "xgb": XGBRegressor(),
                    "catb": CatBoostRegressor()
                }
            
            model_report: pd.DataFrame = evaluate_model(X_train,y_train,X_test,y_test,models)
            if model_report.empty:
                logging.info("model report is empty")
                raise CustomException("model is empy cannot return anything")

            

            best_model_row = model_report.iloc[0]
            best_model_name = best_model_row["model_name"]
            best_model_score = best_model_row["r2s"]
            if best_model_score<0.6:
                logging.info("no best model found")
            logging.info(f"best model is {best_model_name} with r2s {best_model_score}")
            logging.info("model_evaluatin and training is succsfull")

            best_model = models[best_model_name]
            
            save_object(
                filepath=self.trainer_config.model_file_path,
                obj = best_model
            )
            logging.info("model saved succesfully")

            return best_model_name, best_model_score

            
        except Exception as e:
            raise CustomException(e,sys)
