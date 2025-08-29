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

df["Reviews"] = pd.to_numeric(df["Reviews"], errors="coerce").fillna(0)

df["Last Updated"] = pd.to_datetime(df["Last Updated"], errors="coerce")
df["YearMonth"] = df["Last Updated"].dt.to_period("M")

df = df[
    (df["Reviews"] > 500) &
    (~df["App"].str.startswith(("x", "y", "z", "X", "Y", "Z"))) &
    (~df["App"].str.contains("S", case=False, na=False)) &
    (df["Category"].str.startswith(("E", "C", "B")))
]

category_translation = {
    "BEAUTY": "सौंदर्य",    # Hindi
    "BUSINESS": "வணிகம்",   # Tamil
    "DATING": "Dating (Deutsch)"  # German
}

df["Category_Translated"] = df["Category"].str.upper().replace(category_translation)

df_grouped = (
    df.groupby(["YearMonth", "Category_Translated"])["Installs_Clean"]
    .sum()
    .reset_index()
)

df_grouped["Pct_Change"] = df_grouped.groupby("Category_Translated")["Installs_Clean"].pct_change()

ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist)

if 18 <= current_time.hour < 21:  # between 6 PM and 9 PM
    plt.figure(figsize=(12, 7))

    categories = df_grouped["Category_Translated"].unique()

    for category in categories:
        cat_data = df_grouped[df_grouped["Category_Translated"] == category]

        # Plot line
        plt.plot(cat_data["YearMonth"].astype(str), cat_data["Installs_Clean"], label=category)

        # Shade where MoM growth > 20%
        growth_mask = cat_data["Pct_Change"] > 0.20
        plt.fill_between(
            cat_data["YearMonth"].astype(str),
            0,
            cat_data["Installs_Clean"],
            where=growth_mask,
            alpha=0.3
        )

    plt.title("Time Series of Installs with Significant Growth Highlighted", fontsize=14)
    plt.xlabel("Month")
    plt.ylabel("Total Installs")
    plt.legend(title="App Category", fontsize=10)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

else:
    print(" Outside allowed time (6 PM - 9 PM IST). Chart will not be displayed.")

