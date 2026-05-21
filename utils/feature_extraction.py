from urllib.parse import urlparse

def extract_features(url):

    features = []

    # 1. Using IP
    features.append(1 if url.replace('.', '').isdigit() else 0)

    # 2. Long URL
    features.append(1 if len(url) > 75 else 0)

    # 3. Short URL
    shorteners = ['bit.ly', 'tinyurl', 'goo.gl']
    features.append(1 if any(short in url for short in shorteners) else 0)

    # 4. @ symbol
    features.append(1 if '@' in url else 0)

    # 5. Redirecting //
    features.append(1 if url.rfind('//') > 7 else 0)

    # Fill remaining features with 0 temporarily
    while len(features) < 31:
        features.append(0)

    return features