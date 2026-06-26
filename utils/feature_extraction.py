from urllib.parse import urlparse


def extract_features(url):

    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    features = []


    # Using IP
    features.append(
        1 if domain.replace('.', '').isdigit() else -1
    )


    # Long URL
    features.append(
        1 if len(url) > 75 else -1
    )


    # Short URL
    features.append(
        1 if any(x in url for x in ["bit.ly","tinyurl","goo.gl"])
        else -1
    )


    # @ symbol
    features.append(
        1 if "@" in url else -1
    )


    # Redirect //
    features.append(
        1 if "//" in url[7:] else -1
    )


    # Prefix suffix
    features.append(
        1 if "-" in domain else -1
    )


    # Subdomain
    features.append(
        1 if domain.count(".") > 2 else -1
    )


    # HTTPS
    features.append(
        1 if url.startswith("https") else -1
    )


    # suspicious keywords
    words = [
        "login",
        "verify",
        "secure",
        "update",
        "account",
        "payment",
        "bank"
    ]

    features.append(
        1 if any(w in url.lower() for w in words)
        else -1
    )


    # suspicious TLD
    bad_tld = [
        ".xyz",
        ".tk",
        ".ml",
        ".ga",
        ".cf"
    ]

    features.append(
        1 if any(t in domain for t in bad_tld)
        else -1
    )


    # fill remaining features
    while len(features) < 30:
        features.append(-1)


    return features