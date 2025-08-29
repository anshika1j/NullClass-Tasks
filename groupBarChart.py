import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pytz

df = pd.read_csv("Play Store Data.csv")

df.rename(columns=lambda x: x.strip(), inplace=True)

def size_to_mb(size):
    if pd.isna(size) or size == "Varies with device":
        return None
    size = size.upper().replace(",", "")
    if size.endswith("M"):
        return float(size[:-1])
    elif size.endswith("K"):
        return float(size[:-1]) / 1024  # KB → MB
    elif size.endswith("G"):
        return float(size[:-1]) * 1024  # GB → MB
    else:
        return None

df["Size_MB"] = df["Size"].apply(size_to_mb)

df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")

filtered = df[
    (df["Rating"] >= 4.0) &
    (df["Size_MB"] >= 10) &
    (df["Last Updated"].dt.month == 1)
]

top10 = (
    filtered.groupby("Category")
    .agg({"Rating": "mean", "Reviews": "sum", "Installs": "sum"})
    .sort_values(by="Installs", ascending=False)
    .head(10)
)

ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.datetime.now(ist)
start_time = current_time.replace(hour=15, minute=0, second=0, microsecond=0)
end_time = current_time.replace(hour=17, minute=0, second=0, microsecond=0)

if start_time <= current_time <= end_time:
    x = range(len(top10))
    width = 0.4

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar([i - width/2 for i in x], top10["Rating"], width=width, label="Average Rating")
    ax.bar([i + width/2 for i in x], top10["Reviews"], width=width, label="Total Reviews")

    ax.set_xticks(x)
    ax.set_xticklabels(top10.index, rotation=45)
    ax.set_ylabel("Value")
    ax.set_title("Top 10 App Categories by Installs (Filtered)")
    ax.legend()

    plt.tight_layout()
    plt.show()
else:
    print("The chart is only available between 3 PM and 5 PM IST.")
