import os
import sys
import dill
import pandas as pd
from sklearn.metrics import r2_score
from src.logger import logging
from src.exception import CustomException

def save_object(filepath,obj):
    try:
        os.makedirs(os.path.dirname(filepath),exist_ok=True)
        with open(filepath,"wb") as file_obj:
            dill.dump(obj,file_obj)

        return filepath
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(X_train,y_train,X_test,y_test,models):
    logging.info("model evaluation has started")
    try:
        scores = []

        for name,model in models.items():
            model.fit(X_train,y_train)

            y_train_pred = model.predict(X_train)
            train_r2s = r2_score(y_train, y_train_pred)

            y_test_pred = model.predict(X_test)
            test_r2s = r2_score(y_test, y_test_pred)
            scores.append({"model_name":name, "r2s":test_r2s})

            df = pd.DataFrame(scores).sort_values(by="r2s", ascending=False)

            return df
        
    except Exception as e:
        raise CustomException(e,sys)