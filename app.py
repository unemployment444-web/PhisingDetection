from flask import Flask, render_template, request
import pandas as pd
import joblib

from utils.feature_extraction import extract_features


app = Flask(__name__)


# Load trained ML model
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


    # Get URL from user
    url = request.form['url']


    # Extract URL features
    features = extract_features(url)



    # Convert features into dataframe
    input_data = pd.DataFrame(
        [features],
        columns=feature_names
    )



    # ML prediction
    prediction = model.predict(input_data)


    # Confidence score
    confidence = round(
        max(model.predict_proba(input_data)[0]) * 100,
        2
    )



    print("Features:", features)
    print("Prediction:", prediction)



    # Detection reasons

    reasons = []


    danger_words = [
        "login",
        "verify",
        "secure",
        "update",
        "bank",
        "payment",
        "account"
    ]


    bad_domains = [
        ".xyz",
        ".tk",
        ".ml",
        ".ga",
        ".cf"
    ]



    if any(word in url.lower() for word in danger_words):

        reasons.append(
            "Suspicious keywords detected"
        )



    if any(domain in url.lower() for domain in bad_domains):

        reasons.append(
            "Suspicious domain extension"
        )



    if "-" in url:

        reasons.append(
            "Contains unusual hyphen pattern"
        )



    if not url.startswith("https"):

        reasons.append(
            "Website does not use HTTPS"
        )



    if len(url) > 75:

        reasons.append(
            "Very long URL"
        )



    if len(reasons) == 0:

        reasons.append(
            "No suspicious behaviour detected"
        )




    # Final result

    if (
        any(word in url.lower() for word in danger_words)
        or
        any(domain in url.lower() for domain in bad_domains)
    ):

        result = "Phishing Website"


    elif prediction[0] == -1:

        result = "Legitimate Website"


    else:

        result = "Phishing Website"




    return render_template(
        'result.html',
        prediction=result,
        url=url,
        confidence=confidence,
        reasons=reasons
    )




if __name__ == '__main__':

    app.run(debug=True)