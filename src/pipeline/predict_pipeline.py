import pandas as pd
import os
from src.utils import load_object

class predict_config:
    def __init__(self):
        pass

    def predictin(self,pred_df):
        preprocessor_pth = os.path.join("collection", "preprocessor.pkl" )
        preprocessor = load_object(preprocessor_pth)
        model_pth = os.path.join("collection", "model.pkl" )
        model = load_object(model_pth)

        scaled_df = preprocessor.transform(pred_df)
        results = model.predict(scaled_df)

        return results

class CustomData:
    def __init__(self, reading_score, writing_score,gender, race_ethnicity, parental_level_of_education, lunch, test_preparation_course):
        self.reading_score = reading_score
        self.writing_score = writing_score
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course

    def get_dataframe(self):
        dict = {
            "reading_score" : float(self.reading_score),
            "writing_score" : float(self.writing_score),
            "gender" : self.gender,
            "race_ethnicity" : self.race_ethnicity, 
            "parental_level_of_education" : self.parental_level_of_education, 
            "lunch" : self.lunch,
            "test_preparation_course" : self.test_preparation_course
        }
        return pd.DataFrame([dict])
    
