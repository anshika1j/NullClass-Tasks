import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz

df = pd.read_csv("Play Store Data.csv")

df["Installs_Clean"] = (
    df["Installs"]
    .astype(str)
    .str.replace("[+,]", "", regex=True)
)
df["Installs_Clean"] = pd.to_numeric(df["Installs_Clean"], errors="coerce").fillna(0)

def clean_size(x):
    try:
        x = str(x).strip()
        if "M" in x:
            return float(x.replace("M", ""))
        elif "k" in x:
            return float(x.replace("k", "")) / 1024  # kB → MB
        elif "G" in x:
            return float(x.replace("G", "")) * 1024  # GB → MB
        else:
            return float(x)
    except:
        return 0.0

df["Size_MB"] = df["Size"].apply(clean_size)

def clean_android_version(x):
    try:
        return float(str(x).split()[0])
    except:
        return 0.0

df["AndroidVersion_Clean"] = df["Android Ver"].apply(clean_android_version)

df["Price_Clean"] = df["Price"].astype(str).str.replace("$", "", regex=False)
df["Price_Clean"] = pd.to_numeric(df["Price_Clean"], errors="coerce").fillna(0)
df["Revenue"] = df["Installs_Clean"] * df["Price_Clean"]

df = df[
    (df["Installs_Clean"] >= 10000) &
    (df["Revenue"] >= 10000) &
    (df["AndroidVersion_Clean"] > 4.0) &
    (df["Size_MB"] > 15) &
    (df["Content Rating"] == "Everyone") &
    (df["App"].str.len() <= 30)
]

top3_categories = df["Category"].value_counts().nlargest(3).index.tolist()
df = df[df["Category"].isin(top3_categories)]

grouped = df.groupby(["Category", "Type"]).agg(
    Avg_Installs=("Installs_Clean", "mean"),
    Avg_Revenue=("Revenue", "mean")
).reset_index()

ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist)

if 13 <= current_time.hour < 14:  # between 1 PM and 2 PM
    
    pivot = grouped.pivot(
        index="Category",
        columns="Type",
        values=["Avg_Installs", "Avg_Revenue"]
    ).fillna(0).reset_index()

  
    fig, ax1 = plt.subplots(figsize=(10, 6))

    categories = pivot["Category"]
    x = range(len(categories))
    width = 0.35

    free_installs = pivot[("Avg_Installs", "Free")] if ("Avg_Installs", "Free") in pivot else [0]*len(categories)
    paid_installs = pivot[("Avg_Installs", "Paid")] if ("Avg_Installs", "Paid") in pivot else [0]*len(categories)

    ax1.bar([i - width/2 for i in x], free_installs, width=width, label="Free - Installs", color="skyblue")
    ax1.bar([i + width/2 for i in x], paid_installs, width=width, label="Paid - Installs", color="orange")

    ax1.set_xlabel("Top 3 Categories")
    ax1.set_ylabel("Average Installs")
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.legend(loc="upper left")

    free_revenue = pivot[("Avg_Revenue", "Free")] if ("Avg_Revenue", "Free") in pivot else [0]*len(categories)
    paid_revenue = pivot[("Avg_Revenue", "Paid")] if ("Avg_Revenue", "Paid") in pivot else [0]*len(categories)

    ax2 = ax1.twinx()
    ax2.plot(x, free_revenue, marker="o", color="blue", label="Free - Revenue")
    ax2.plot(x, paid_revenue, marker="o", color="red", label="Paid - Revenue")
    ax2.set_ylabel("Average Revenue ($)")

    fig.suptitle("Dual Axis Chart: Avg Installs vs Avg Revenue (Free vs Paid Apps)", fontsize=14)
    fig.legend(loc="upper right", bbox_to_anchor=(0.9, 0.9))

    plt.tight_layout()
    plt.show()
else:
    print(" Outside allowed time (1 PM - 2 PM IST). Chart will not be displayed.")
