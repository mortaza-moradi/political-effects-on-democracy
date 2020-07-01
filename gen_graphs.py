import pandas as pd
import numpy as np
import plotly.express as pl
import plotly.io as pio
import plotly.graph_objects as go
from sklearn.metrics import r2_score
#import chart_studio.tools as tls
#from sklearn.preprocessing import PolynomialFeatures

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

#### FIRST GRAPH (DEM SCORE VS DEM DERIV) ####
fig_demscoreVSdemderiv = pl.scatter(df, x="Democratic Score", y="DemScore Change")

#Fit polynomial regression (quadratic)

#Remove row 0, 10, 48 due to no data
x = np.array(df["Democratic Score"].drop([0, 10, 48]))
y = np.asarray(df["DemScore Change"].drop([0, 10, 48]), dtype=np.float32)

poly_fit = np.polyfit(np.array(x), np.array(y), 2)
f = np.poly1d(poly_fit)

#Calculate new expected points
x_inc = np.linspace(3, 4.7, 200)
y_hat = f(x_inc)
##r^2 = .17 :(
fig_demscoreVSdemderiv.add_trace(go.Scatter(x=x_inc, y=y_hat, name="Trendline", hoverinfo="skip",
                                            line={
                                                'color': '#474747',
                                                'dash': 'dash',
}))


fig_demscoreVSdemderiv.update_traces(marker={
    'size': 10,
    'color': '#24470A'
    })

fig_demscoreVSdemderiv.update_layout(
    template="ggplot2",
    showlegend=False,
    title={
        'text': "Democratic Score vs Yearly Change",
        'x': .1,'y': .925
    },
    yaxis_title="Democratic Change",
    plot_bgcolor="rgba(242, 242, 242, 0.75)",
    yaxis={
        #Dinstinguish between increasing and decreasing
        'tickvals': [0], 'ticktext': [0],
        'tickcolor': '#FFF',
        'range': [-.35, .25]
    },
    xaxis={
        #Only label the range, as values are meaningless to viewer
        'tickvals': [3.1, 4.6],
        'ticktext': [3.1, 4.6],
        'range': [2.7, 4.9],
        'tickcolor': '#FFF'
    },
    hoverlabel={
        'font_family': 'Didot',
        'font_size': 11,
        'bgcolor': 'rgba(242, 242, 242, 0.75)'
    },
    titlefont={'size': 20},
    font={'family': 'Didot', 'color': 'rgba(40, 40, 40)'}
)

#fig_demscoreVSdemderiv.show()
pio.write_html(fig_demscoreVSdemderiv, file="demscoreVSdemderiv.html")

############~~~~~~~~~~~~~~~~~~~~~~~~~###############
