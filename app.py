from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load trained model
model = joblib.load("model.pkl")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    # Get values from form
    features = []

    for i in range(1, 32):
        value = request.form.get(f'feature{i}')
        features.append(int(value))

    # Convert to dataframe
    input_data = pd.DataFrame([features])

    # Prediction
    prediction = model.predict(input_data)

    # Result
    if prediction[0] == 1:
        result = "Legitimate Website"
    else:
        result = "Phishing Website"

    return render_template('result.html', prediction=result)

if __name__ == '__main__':
    app.run(debug=True)