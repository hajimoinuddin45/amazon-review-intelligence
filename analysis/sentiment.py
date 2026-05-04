from textblob import TextBlob


def get_sentiment_distribution(reviews):

    positive = 0
    negative = 0
    neutral = 0

    for review in reviews:

        polarity = TextBlob(review).sentiment.polarity

        if polarity > 0:

            positive += 1

        elif polarity < 0:

            negative += 1

        else:

            neutral += 1

    # prevent empty chart
    if positive == 0 and negative == 0 and neutral == 0:

        positive = 1

    return {

        "Positive": positive,

        "Negative": negative,

        "Neutral": neutral
    }