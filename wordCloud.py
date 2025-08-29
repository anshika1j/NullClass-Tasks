import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Load your dataset
df = pd.read_csv("Play Store Data.csv")

# Keep only Health & Fitness category and 5-star reviews
filtered = df[(df["Category"] == "HEALTH_AND_FITNESS") & (df["Rating"] == 5.0)]

# Drop rows with missing reviews
filtered = filtered.dropna(subset=["Reviews"])

# Combine all reviews into one text
text = " ".join(review for review in filtered["Reviews"].astype(str))

# Exclude stopwords + app names
stopwords = set(STOPWORDS)
stopwords.update(df["App"].dropna().astype(str).unique())

# Generate WordCloud
wordcloud = WordCloud(
    stopwords=stopwords,
    background_color="white",
    width=1200,
    height=800
).generate(text)

# Plot
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Most Frequent Keywords in 5-Star Health & Fitness App Reviews", fontsize=14)
plt.show()
