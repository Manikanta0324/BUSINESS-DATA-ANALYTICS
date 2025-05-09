import pandas as pd
import re
import matplotlib.pyplot as plt

df = pd.read_csv('tweet.csv')

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', str(text))
    return text.lower()
df['CleanText'] = df['Text'].apply(clean_text)
print(df)
positive_keywords = ["love", "great", "good", "awesome", "best", "fantastic", "happy", "like"]
negative_keywords = ["worst", "bad", "terrible", "awful", "hate", "disappointed", "angry"]
def classify_sentiment(text):
    if any(word in text for word in positive_keywords):
        return "Positive"
    elif any(word in text for word in negative_keywords):
        return "Negative"
    else:
        return "Neutral"
df['Sentiment'] = df['CleanText'].apply(classify_sentiment)

avg_likes = df.groupby('Sentiment')['Likes'].mean().round(2)
print("\nAverage Likes per Sentiment:\n", avg_likes)

sentiment_counts = df['Sentiment'].value_counts()
print(df)
plt.figure(figsize=(6,6))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', startangle=140, colors=['lightgreen', 'lightgray', 'salmon'])
plt.title('Tweet Sentiment Distribution')
plt.axis('equal')
plt.show()
