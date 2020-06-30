import pandas as pd
import plotly.express as px
import plotly.io as pio
import chart_studio.tools as tls

def import_clean_data():
    #Import data as dataframe
    df = pd.read_csv("_data/LeanValues_New.csv")
    
    #Drop the attributes column, and corresponding empty rows
    df = df.drop(columns=['Unnamed: 9'])
    df = df.drop(df.index[49:60])
    
    return df
    
df = import_clean_data()

fig = px.scatter(df, x="demscore", y="demderiv**")
fig.update_layout(template="plotly_white")

pio.write_html(fig, file="index.html")
