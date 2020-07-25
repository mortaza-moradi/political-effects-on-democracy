import pandas as pd
import numpy as np
import plotly.express as pl
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#import statsmodels.formula.api as smf
#import chart_studio.tools as tls
#from sklearn.preprocessing import PolynomialFeatures
#from sklearn.linear_model import LinearRegression

def import_clean_data():
    #Import data as dataframe
    df = pd.read_csv("_data/LeanValues_New.csv")
    
    #Drop the attributes column, and corresponding empty rows
    df = df.drop(columns=['Unnamed: 11', 'OVERALL AMERICAN (L) CHANGE', 'OVERALL AMERICAN (C) CHANGE'])
    df = df.drop(df.index[49:60])
    
    #Rename columns to be more explanatory
    df = df.rename(columns={'demscore': 'Democratic Score',
                           'demderiv**': 'DemScore Change',
                           'Judicial (-1, +1)*': 'Judicial (-1, +1)',
                           'demderiv_backwards': 'DemScore Forward Change',
                           'apl_derivative': 'Political Lean Derivative'})
    
    return df
    
df = import_clean_data()


#Graph democratic scores against the political leaning derivative to see any large scale trends
fig_leanDerivVSdemscore = go.Figure()
fig_leanDerivVSdemscore.add_trace(go.Scatter(x=df["Democratic Score"], y=df["Political Lean Derivative"], mode="markers"))

#fig_leanDerivVSdemscore.show()


####Make a graph with year vs demscore, its going down but can we see if there are differences between more liberal and less liberal america and its effect on demscore.

fig_yearVSdemscore = go.Figure()
fig_yearVSdemscore.add_trace(go.Scatter(x=df["Year"], y=df["Democratic Score"], line_shape="spline", connectgaps=True, line={'color': 'rgba(40, 40, 40, .4)', 'width':4}))

fig_yearVSdemscore.update_yaxes(fixedrange=True)
fig_yearVSdemscore.update_xaxes(fixedrange=True)

fig_yearVSdemscore.update_layout(
    template="ggplot2",
    showlegend=False,
    title={
        'text': "Democratic Score Over Time",
        'x': .1,'y': .925
    },
    yaxis_title="Democratic Score",
    xaxis_title="fig a. Year",
    plot_bgcolor="rgba(242, 242, 242, 0.75)",
    yaxis={
        #Dinstinguish between min and max
        'tickvals': [3.2, 4.5],
        'range': [3, 4.7],
        'tickcolor': '#FFF'
    },
    xaxis={
        #Only label the range, as values are meaningless to viewer
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

#fig_yearVSdemscore.show()
#pio.write_html(fig_yearVSdemscore, 'yearVSdemscore.html')


#### LAST GRAPH (DEM SCORE VS DEM DERIV) ####
fig_demscoreVSdemderiv = pl.scatter(df, x="Democratic Score", y="DemScore Change")

#Fit polynomial regression (quadratic)

#Remove row 0, 10, 48 due to no data
x = np.array(df["Democratic Score"].drop([0, 10, 48]))
y = np.asarray(df["DemScore Change"].drop([0, 10, 48]), dtype=np.float32)

poly_fit = np.polyfit(np.array(x), np.array(y), 2)
f = np.poly1d(poly_fit)

#Calculate new expected points
x_inc = np.linspace(3, 4.7, 240)
y_hat = f(x_inc)
##r^2 = .17 :(

fig_demscoreVSdemderiv.add_trace(go.Scatter(x=x_inc, y=y_hat, name="Trendline", hoverinfo="skip", mode="lines",
                                            line={
                                                'color': '#004609',
                                                'dash': 'dash',
                                                'width': 4
}))


fig_demscoreVSdemderiv.update_traces(marker={
    'size': 10,
    'color': 'rgba(71, 71, 71, .4)'
    })

fig_demscoreVSdemderiv.update_layout(
    template="ggplot2",
    showlegend=False,
    title={
        'text': "Democratic Score vs Yearly Change",
        'x': .1,'y': .925
    },
    yaxis_title="Democratic Change",
    xaxis_title="fig d. Democratic Score",
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

fig_demscoreVSdemderiv.show()
pio.write_html(fig_demscoreVSdemderiv, file="demscoreVSdemderiv.html")

############~~~~~~~~~~~~~~~~~~~~~~~~~###############


####### SECOND GRAPH (Political Leaning VS Demscore) #######

fig_leanVSdemscore = pl.scatter(x = df["American Political Leaning"], y=df["Democratic Score"])

fig_leanVSdemscore.update_traces(marker={
    'size': 10,
    'color': 'rgba(71, 71, 71, .4)'
    })

## Add linear regression
# Remove nan lines
x = np.asarray(df["American Political Leaning"].drop([10, 48]))
y = np.asarray(df["Democratic Score"].drop([10, 48]))

poly_fit = np.polyfit(np.array(x), np.array(y), 1)
f = np.poly1d(poly_fit)

#Calculate new expected points
x_inc = np.linspace(-1.8, 3.8, 8)
y_hat = f(x_inc)

fig_leanVSdemscore.add_trace(go.Scatter(x=x_inc, y=y_hat, name="TrendLine", hoverinfo="skip", mode="lines", 
                                        line={
                                                'color': '#004609',
                                                'dash': 'solid',
                                                'width': 4
}))

fig_leanVSdemscore.update_layout(
    template="ggplot2",
    showlegend=False,
    title={
        'text': "American Political Leaning vs Democratic Score",
        'x': .1,'y': .925
    },
    yaxis_title="Democratic Score",
    xaxis_title="fig b. American Political Leaning",
    plot_bgcolor="rgba(242, 242, 242, 0.75)",
    yaxis={
        #Dinstinguish between increasing and decreasing
        'tickvals': [3.5, 4.5],
        'tickcolor': '#FFF',
        'range': [3, 5.5], 'zeroline': False
    },
    xaxis={
        #Only label the range, as values are meaningless to viewer
        'tickvals': [-1, 0, 1, 2, 3],
        'range': [-2.4, 4.4],
        'tickcolor': '#FFF',
        'showgrid': False, 'zeroline': False
    },
    hoverlabel={
        'font_family': 'Didot',
        'font_size': 11,
        'bgcolor': 'rgba(242, 242, 242, 0.75)'
    },
    titlefont={'size': 20},
    font={'family': 'Didot', 'color': 'rgba(40, 40, 40)'}
)


#fig_leanVSdemscore.show()
#pio.write_html(fig_leanVSdemscore, file="leanVSdemscore.html")

###########------------------------##############

##### SECOND GRAPH (DIVIDED BY THE THREE BRANCHES) #######


fig_branchesVSdemscore = make_subplots(rows=1, cols=3)

fig_branchesVSdemscore.add_trace(go.Box(
    y=df["Democratic Score"],
    x=df["Legislative (-1, 0, +1)"],
    name="Legislative",
    marker_color="rgba(40, 40, 40, .6)"
    ),
              row=1, col=1
 )

fig_branchesVSdemscore.add_trace(go.Box(
    y=df["Democratic Score"],
    x=df["Executive (-1, +1)"],
    name="Executive",
    opacity=.24,
    marker_color="rgba(40, 40, 40)"
    ),
             row=1, col=2
)
fig_branchesVSdemscore.add_trace(go.Box(
    y=df["Democratic Score"],
    x=df["Judicial (-1, +1)"],
    name="Judicial",
    opacity=.24,
    marker_color= "rgba(40, 40, 40)"
    ),
             row=1, col=3
)

fig_branchesVSdemscore.update_layout(
    template="ggplot2+xgridoff",
    title={
        'text': "Branches of US Government vs Democratic Scores",
        'x': .1,'y': .925
    },
    xaxis={
        'showgrid': False,
        'zeroline': False
    },
    showlegend=False,
    plot_bgcolor="rgba(242, 242, 242, 0.75)",
    hoverlabel={
        'font_family': 'Didot',
        'font_size': 11,
        'bgcolor': 'rgba(242, 242, 242, 0.75)'
    },
    font={'family': 'Didot', 'color': 'rgba(40, 40, 40)'}
)

fig_branchesVSdemscore.update_yaxes(title_text="Democratic Scores", fixedrange=True, tickvals=[3.5, 4, 4.5], tickcolor="#FFF", range=[3, 4.8], row=1, col=1)
fig_branchesVSdemscore.update_yaxes(tickvals=[3.5, 4, 4.5], fixedrange=True, tickcolor="#FFF", tickfont={'color':'#FFF'}, range=[3, 4.8], row=1, col=2)
fig_branchesVSdemscore.update_yaxes(tickvals=[3.5, 4, 4.5], fixedrange=True, tickcolor="#FFF", tickfont={'color':'#FFF'}, range=[3, 4.8], row=1, col=3)

fig_branchesVSdemscore.update_xaxes(title_text="fig c. Legislative", zeroline=False, fixedrange=True, tickcolor="#FFF", row=1, col=1)
fig_branchesVSdemscore.update_xaxes(title_text="fig c. Executive", zeroline=False, fixedrange=True, tickcolor="#FFF", row=1, col=2)
fig_branchesVSdemscore.update_xaxes(title_text="fig c. Judicial", zeroline=False, fixedrange=True, tickcolor="#FFF",row=1, col=3)

#fig_branchesVSdemscore.show()
#pio.write_html(fig_branchesVSdemscore, file="branchesVSdemscore.html")