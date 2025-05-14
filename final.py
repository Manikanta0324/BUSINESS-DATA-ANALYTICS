import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt
import seaborn as sns
# Load the 'feedback' sheet from the Excel file
df = pd.read_excel('customer2.xlsx', sheet_name='feedback')

# Extract the specific columns you need from the feedback sheet
df_filtered = df[['feedback_id', 'customer_id', 'product_id', 'rating', 'comments']]
print(df_filtered )
# Check for missing values
print(df_filtered.isnull().sum())

# Drop rows with missing values (if needed)
df_filtered = df_filtered.dropna()
print(df_filtered)

# Step 1: Average Rating per Product (Converted to integer)
average_rating_per_product = df_filtered.groupby('product_id')['rating'].mean().astype(int)

# Print the result
print("Average Rating per Product:")
print(average_rating_per_product)

# Step 2a: Word Frequency Analysis (from customer feedback comments)
# Preprocess the comments (remove punctuation and convert to lowercase)
df_filtered['comments_clean'] = df_filtered['comments'].apply(lambda x: re.sub(r'[^\w\s]', '', str(x).lower()))

# Print the DataFrame with both columns
print(df_filtered[['comments', 'comments_clean']])

# Joining all the comments into a single string (if needed for word frequency analysis)
all_comments = ' '.join(df_filtered['comments_clean'])
print(df_filtered[['comments', 'comments_clean']])


# Tokenize the words and count their frequency
word_count = Counter(all_comments.split())
print(word_count)


#Print the 10 most common words in the comments
print("\nMost Common Words in Comments:")
print(word_count.most_common(10))
# Step 2b: Sentiment Analysis Based on Rating
# Create a function to classify the sentiment based on rating
def classify_sentiment(rating):
    if rating >= 4:
        return 'Positive'
    elif rating == 3:
        return 'Neutral'
    else:
        return 'Negative'
# Apply the sentiment classification
df_filtered['sentiment'] = df_filtered['rating'].apply(classify_sentiment)

# Print the sentiment distribution
print("\nSentiment Distribution:")
print(df_filtered['sentiment'].value_counts())

# Step 3: Calculate Purchase Frequency per Customer-Product Pair
purchase_frequency = df_filtered.groupby(['customer_id', 'product_id']).size().reset_index(name='purchase_count')

# Merge the purchase frequency data with the feedback data to correlate with ratings
df_with_purchase_frequency = pd.merge(df_filtered, purchase_frequency, on=['customer_id', 'product_id'], how='left')

# Step 4: Correlating Purchase Frequency with Feedback

# Group by product_id to calculate the average rating and total purchase frequency for each product
product_feedback_analysis = df_with_purchase_frequency.groupby('product_id').agg(
    average_rating=('rating', 'mean'),
    total_purchase_count=('purchase_count', 'sum')
).reset_index()

# Print the result to analyze the correlation
print("\nProduct Feedback Analysis:")
print(product_feedback_analysis)

# graph
# Graph 1: Average Rating per Product
plt.figure(figsize=(8, 5))
sns.barplot(x='product_id', y='average_rating', data=product_feedback_analysis, palette='Blues_d')
plt.title('Average Rating per Product')
plt.xlabel('Product ID')
plt.ylabel('Average Rating')
plt.ylim(0, 5)
plt.tight_layout()
plt.show()

# Graph 2: Pie Chart - Sentiment Distribution
plt.figure(figsize=(6, 6))
sentiment_counts = df_filtered['sentiment'].value_counts()
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%',
        colors=['green', 'gray', 'red'], startangle=140)
plt.title('Sentiment Distribution')
plt.axis('equal')
plt.tight_layout()
plt.show()

# Graph 3: Total Purchase Count per Product
plt.figure(figsize=(8, 5))
sns.barplot(x='product_id', y='total_purchase_count', data=product_feedback_analysis, palette='Oranges_d')
plt.title('Total Purchase Count per Product')
plt.xlabel('Product ID')
plt.ylabel('Total Purchase Count')
plt.tight_layout()
plt.show()
