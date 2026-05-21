from flask import Flask, render_template, request
import pandas as pd
import joblib

from utils.feature_extraction import extract_features

app = Flask(__name__)

# Load trained model
model = joblib.load("model.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    url = request.form['url']

    # Extract features
    features = extract_features(url)

    # Convert to dataframe
    input_data = pd.DataFrame([features])

    # Prediction
    prediction = model.predict(input_data)

    if prediction[0] == 1:
        result = "Legitimate Website"
    else:
        result = "Phishing Website"

    return render_template(
        'result.html',
        prediction=result,
        url=url
    )

if __name__ == '__main__':
    app.run(debug=True)