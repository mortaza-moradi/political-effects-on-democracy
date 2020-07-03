import pandas as pd
import numpy as np
import plotly.express as pl
import plotly.io as pio
import plotly.graph_objects as go
#import statsmodels.formula.api as smf
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
x_inc = np.linspace(3, 4.7, 240)
y_hat = f(x_inc)
##r^2 = .17 :(

fig_demscoreVSdemderiv.add_trace(go.Scatter(x=x_inc, y=y_hat, name="Trendline", hoverinfo="skip", mode="lines",
                                            line={
                                                'color': '#24470A',
                                                'dash': 'solid',
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
#pio.write_html(fig_demscoreVSdemderiv, file="demscoreVSdemderiv.html")

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
                                                'color': '#24470A',
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
    xaxis_title="American Political Leaning",
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

##########------------------------##############

##### SECOND GRAPH (DIVIDED BY THE THREE BRANCHES) #######


###~ Legislative ~###
fig_liberalVSdemscore = pl.box(x =df["Legislative (-1, 0, +1)"], y=df["Democratic Score"], points="all")

fig_liberalVSdemscore.update_traces(marker={
    'size': 10,
    'color': 'rgba(71, 71, 71, .6)',
    'opacity': .2
})

fig_liberalVSdemscore.update_layout(
    template="ggplot2",
    showlegend=False,
    title={
        'text': 'Leaning of Legislative Branch vs Democratic Score',
        'x': .1,'y': .925
    },
    xaxis_title="Legislative Branch",
    yaxis_title="Democratic Score",
    plot_bgcolor="rgba(242, 242, 242, 0.75)",
    yaxis={
        #Values here are meaningless to viewer
        'tickvals': [3.5, 4.5],
        'tickcolor': '#FFF',
        'range': [3, 4.8], 'zeroline': False
    },
    xaxis={
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


#fig_liberalVSdemscore.show()
#pio.write_html(fig_liberalVSdemscore, file="liberalVSdemscore.html")

###~ Executive ~###
fig_executiveVSdemscore = pl.box(x =df["Executive (-1, +1)"], y=df["Democratic Score"], points="all")

fig_executiveVSdemscore.update_traces(marker={
    'size': 10,
    'color': 'rgba(71, 71, 71, .6)',
    'opacity': .2
})

fig_executiveVSdemscore.update_layout(
    template="ggplot2",
    showlegend=False,
    title={
        'text': 'Leaning of Executive Branch vs Democratic Score',
        'x': .1,'y': .925
    },
    xaxis_title="Executive Branch",
    yaxis_title="Democratic Score",
    plot_bgcolor="rgba(242, 242, 242, 0.75)",
    yaxis={
        #Values here are meaningless to viewer
        'tickvals': [3.5, 4.5],
        'tickcolor': '#FFF',
        'range': [3, 4.8], 'zeroline': False
    },
    xaxis={
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

#fig_executiveVSdemscore.show()
#pio.write_html(fig_executiveVSdemscore, file="executiveVSdemscore.html")


###~ Judicial ~###
fig_judicialVSdemscore = pl.box(x =df["Judicial (-1, +1)"], y=df["Democratic Score"], points="all")

fig_judicialVSdemscore.update_traces(marker={
    'size': 10,
    'color': 'rgba(71, 71, 71, .6)',
    'opacity': .2
})

fig_judicialVSdemscore.update_layout(
    template="ggplot2",
    showlegend=False,
    title={
        'text': 'Leaning of Judicial Branch vs Democratic Score',
        'x': .1,'y': .925
    },
    xaxis_title="Judicial Branch",
    yaxis_title="Democratic Score",
    plot_bgcolor="rgba(242, 242, 242, 0.75)",
    yaxis={
        #Values here are meaningless to viewer
        'tickvals': [3.5, 4.5],
        'tickcolor': '#FFF',
        'range': [3, 4.8], 'zeroline': False
    },
    xaxis={
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

#fig_judicialVSdemscore.show()
#pio.write_html(fig_judicialVSdemscore, file="judicialVSdemscore.html")
