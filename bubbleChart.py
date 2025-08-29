import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
from datetime import datetime
import pytz

df = pd.read_csv("Play Store Data.csv")

def clean_reviews(x):
    x = str(x).replace(",", "").replace("+", "").strip()
    try:
        if "M" in x:
            return float(x.replace("M", "")) * 1_000_000
        elif "K" in x:
            return float(x.replace("K", "")) * 1_000
        elif x.isdigit():
            return float(x)
        else:
            return float(x)
    except:
        return 0.0

df["Reviews_Clean"] = df["Reviews"].apply(clean_reviews)

df["Installs_Clean"] = (
    df["Installs"]
    .astype(str)
    .str.replace("[+,]", "", regex=True)
    .replace("Free", "0")
)

df["Installs_Clean"] = pd.to_numeric(df["Installs_Clean"], errors="coerce").fillna(0)

df["Sentiment_Subjectivity"] = df["App"].apply(lambda x: TextBlob(str(x)).sentiment.subjectivity)

valid_categories = [
    "GAME", "BEAUTY", "BUSINESS", "COMICS", "COMMUNICATION",
    "DATING", "ENTERTAINMENT", "SOCIAL", "EVENT"
]

df = df[
    (df["Rating"] > 3.5) &
    (df["Category"].isin(valid_categories)) &
    (df["Reviews_Clean"] > 500) &
    (~df["App"].str.contains("S", case=False, na=False)) &
    (df["Sentiment_Subjectivity"] > 0.5) &
    (df["Installs_Clean"] > 50000)
]

translations = {
    "BEAUTY": "सौंदर्य",     # Hindi
    "BUSINESS": "வணிகம்",   # Tamil
    "DATING": "Dating (Deutsch)"  # German 
}

df["Category_Translated"] = df["Category"].replace(translations)

ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist)

if 17 <= current_time.hour < 19:  # 5 PM to 7 PM IST
    
    plt.figure(figsize=(12, 8))

    for category in df["Category_Translated"].unique():
        sub_df = df[df["Category_Translated"] == category]
        color = "pink" if "GAME" in category else None  
        plt.scatter(
            sub_df["Size"].str.replace("M", "").str.replace("k", "").str.replace("Varies with device", "0").astype(float),
            sub_df["Rating"],
            s=sub_df["Installs_Clean"] / 1000,  # bubble size
            alpha=0.6,
            label=category,
            color=color
        )

    plt.xlabel("App Size (MB)")
    plt.ylabel("Average Rating")
    plt.title("Bubble Chart: App Size vs Rating (Bubble = Installs)")
    plt.legend()
    plt.show()

else:
    print(" Outside allowed time (5 PM - 7 PM IST). Chart will not be shown.")
