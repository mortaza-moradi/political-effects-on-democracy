import pandas as pd
import plotly.express as pl
import plotly.io as pio
import chart_studio.tools as tls
from sklearn.preprocessing import PolynomialFeatures

def import_clean_data():
    #Import data as dataframe
    df = pd.read_csv("_data/LeanValues_New.csv")
    
    #Drop the attributes column, and corresponding empty rows
    df = df.drop(columns=['Unnamed: 9', 'OVERALL AMERICAN (L) CHANGE', 'OVERALL AMERICAN (C) CHANGE'])
    df = df.drop(df.index[49:60])
    
    #Rename columns to be more explanatory
    df = df.rename(columns={'demscore': 'Democratic Score',
                           'demderiv**': 'DemScore Change',
                           'Judicial (-1, +1)*': 'Judicial (-1, +1)'})
    
    return df
    
df = import_clean_data()

fig = pl.scatter(df, x="Democratic Score", y="DemScore Change")
fig.update_traces(marker={
    'size': 10,
    #'line': {
    #    'width': 1,
    #    'color': '#381817'
    #},
    'color': '#B84F4C'
    })

##TODO: Change font!
fig.update_layout(
    template="ggplot2+ygridoff+xgridoff", 
    title="<b>Democratic Score vs Yearly Change</b>",
    yaxis_title="Democratic Change",
    titlefont={
        'size': 20
    },
    font={
        'family': 'Centabel Book'
    }
)

#fig.show()
#pio.write_html(fig, file="demscoreVSdemderiv.html")
