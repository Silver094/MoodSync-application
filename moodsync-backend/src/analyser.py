from textblob import TextBlob

def analyze_mood(text):
    """
    Analyze the sentiment of the given text and return the mood.

    Parameters:
    text (str): The text to analyze.

    Returns:
    str: The mood based on the sentiment analysis.
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.5:
        mood = "Happy"
    elif polarity > 0:
        mood = "Calm"
    else:
        mood = "Sad"
    
    return mood
