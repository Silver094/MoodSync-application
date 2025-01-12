from textblob import TextBlob

def analyze_mood(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.5:
        mood = "Happy"
    elif polarity > 0:
        mood = "Calm"
    else:
        mood = "Sad"
    
    return mood