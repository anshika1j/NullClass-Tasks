import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

df = pd.read_csv("Play Store Data.csv")

df['Installs'] = df['Installs'].astype(str).str.replace('[+,]', '', regex=True)
df['Installs'] = pd.to_numeric(df['Installs'], errors='coerce').fillna(0)

df['Country'] = "USA"   

df = df[~df['Category'].str.startswith(('A', 'C', 'G', 'S'))]

category_country = df.groupby(['Category', 'Country'], as_index=False)['Installs'].sum()

top5_categories = (
    category_country.groupby('Category')['Installs']
    .sum()
    .nlargest(5)
    .index
)
category_country = category_country[category_country['Category'].isin(top5_categories)]

category_country['Highlight'] = category_country['Installs'] > 1_000_000

ist = pytz.timezone("Asia/Kolkata")
current_time = datetime.now(ist)

if 18 <= current_time.hour < 20:
    fig = px.choropleth(
        category_country,
        locations="Country",
        locationmode="ISO-3",   
        color="Installs",
        hover_name="Category",
        title="Choropleth Map of Installs by App Category",
        color_continuous_scale="Viridis"
    )

    fig.update_traces(marker=dict(line=dict(width=2, color="red")))
    fig.show()
else:
    print(" The Choropleth map is only available between 6 PM and 8 PM IST.")
