from flask import Flask,request,render_template
from src.pipeline.predict_pipeline import CustomData,predict_config

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/prediction', methods=['POST','GET'])
def predict_dpnt():
    if request.method == 'GET':
        return render_template("home.html")
    else:
        data = CustomData(
            reading_score = float(request.form.get('reading_score')), 
            writing_score = float(request.form.get('writing_score')),
            gender = request.form.get('gender'), 
            race_ethnicity = request.form.get('race_ethnicity'), 
            parental_level_of_education = request.form.get('parental_level_of_education'), 
            lunch = request.form.get('lunch'), 
            test_preparation_course = request.form.get('test_preparation_course')
            )
        
        pred_df = data.get_dataframe()
        pred_pipe = predict_config()
        results = pred_pipe.predictin(pred_df)

        return render_template("home.html",results=results[0] )
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

