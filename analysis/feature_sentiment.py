from collections import defaultdict


# =====================================================
# POSITIVE / NEGATIVE WORDS
# =====================================================

POSITIVE_WORDS = [

    "excellent",
    "great",
    "amazing",
    "smooth",
    "premium",
    "fast",
    "good",
    "durable",
    "comfortable",
    "reliable",
    "worth",
    "best",
    "love",
    "awesome",
    "perfect"
]


NEGATIVE_WORDS = [

    "bad",
    "poor",
    "slow",
    "issue",
    "problem",
    "heating",
    "drain",
    "weak",
    "worst",
    "delay",
    "broken",
    "noise",
    "expensive",
    "overpriced"
]


# =====================================================
# COMMON PRODUCT FEATURES
# =====================================================

FEATURE_KEYWORDS = {

    "Battery": [
        "battery",
        "charging",
        "backup"
    ],

    "Camera": [
        "camera",
        "photo",
        "photography"
    ],

    "Display": [
        "display",
        "screen",
        "brightness"
    ],

    "Performance": [
        "performance",
        "speed",
        "gaming",
        "multitasking"
    ],

    "Heating": [
        "heating",
        "heat",
        "thermal"
    ],

    "Build Quality": [
        "build",
        "design",
        "premium"
    ],

    "Audio": [
        "speaker",
        "audio",
        "sound"
    ],

    "Delivery": [
        "delivery",
        "shipping"
    ],

    "Packaging": [
        "packaging",
        "box"
    ],

    "Customer Support": [
        "support",
        "service"
    ],

    "Keyboard": [
        "keyboard",
        "typing"
    ],

    "Trackpad": [
        "trackpad"
    ],

    "Fan Noise": [
        "fan",
        "noise"
    ],

    "Price": [
        "price",
        "value",
        "expensive",
        "overpriced"
    ]
}


# =====================================================
# ANALYZE FEATURE SENTIMENT
# =====================================================

def analyze_feature_sentiment(reviews):

    scores = defaultdict(int)

    for review in reviews:

        review_lower = review.lower()

        for feature, keywords in FEATURE_KEYWORDS.items():

            if any(

                keyword in review_lower

                for keyword in keywords
            ):

                # positive words
                for word in POSITIVE_WORDS:

                    if word in review_lower:

                        scores[feature] += 1

                # negative words
                for word in NEGATIVE_WORDS:

                    if word in review_lower:

                        scores[feature] -= 1

    # =================================================
    # KEEP ONLY DETECTED FEATURES
    # =================================================

    final_scores = {}

    for feature, score in scores.items():

        if score != 0:

            final_scores[feature] = score

    return final_scores