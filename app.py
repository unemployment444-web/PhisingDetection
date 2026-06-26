from flask import Flask, render_template, request
import pandas as pd
import joblib

from utils.feature_extraction import extract_features

app = Flask(__name__)

# Load trained model
model = joblib.load("model.pkl")


# Dataset feature names
feature_names = [
    'UsingIP',
    'LongURL',
    'ShortURL',
    'Symbol@',
    'Redirecting//',
    'PrefixSuffix-',
    'SubDomains',
    'HTTPS',
    'DomainRegLen',
    'Favicon',
    'NonStdPort',
    'HTTPSDomainURL',
    'RequestURL',
    'AnchorURL',
    'LinksInScriptTags',
    'ServerFormHandler',
    'InfoEmail',
    'AbnormalURL',
    'WebsiteForwarding',
    'StatusBarCust',
    'DisableRightClick',
    'UsingPopupWindow',
    'IframeRedirection',
    'AgeofDomain',
    'DNSRecording',
    'WebsiteTraffic',
    'PageRank',
    'GoogleIndex',
    'LinksPointingToPage',
    'StatsReport'
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    url = request.form['url']

    # Extract features
    features = extract_features(url)

    # Convert to dataframe
    input_data = pd.DataFrame(
        [features],
        columns=feature_names
    )


    # ML Prediction
    prediction = model.predict(input_data)


    print("Features:", features)
    print("Prediction:", prediction)


    # Extra phishing checks
    danger_words = [
        "login",
        "verify",
        "secure",
        "update",
        "bank",
        "payment"
    ]


    if any(word in url.lower() for word in danger_words) or ".xyz" in url.lower():

        result = "Phishing Website"


    elif prediction[0] == -1:

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