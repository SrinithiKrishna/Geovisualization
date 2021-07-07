import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)
app.title = 'Geovisualization of crime in Indian states'

# Boostrap CSS for styling.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})

df = pd.read_csv('Data/folimap.csv')
df1=pd.read_excel('Data/crime against women 2001-2020.xlsx')
opts = [ dict(label=t, value=t)
         for t in df1['Year'].unique() ]
fig = px.line(
    df1,
    x='Year',
    y='Rape',
    color='State/UT',
    #facet_col='Type',
    #template='presentation',
    )
fig1= px.line(
    df1,
    x='Year',
    y='Cruelty by Husband or his Relatives',
    color='State/UT',
    #facet_col='Type',
    #template='presentation',
    )
#fig.update_traces(mode='lines+markers')

# Mapbox API key
mapbox_access_token = 'pk.eyJ1Ijoia2VsbHlubSIsImEiOiJjanM0eDF0ZngwMjZ0M3lwYjV5MWxqZm1xIn0.49GaijkpupewHcHf2niUDA'

# layout for map
layout_map = dict(
    #autosize=True,
    #height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='10'),
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=12), orientation='h'),
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict( # Specify where map should be centered and starting zoom level.
            lon=28.6600,	
            lat=77.2300,
        ),
        zoom=2,
    )
)

about= html.Div(children=[
    html.H1(
        children='Statewise Major Crime',
        style={
            'textAlign': 'center'
        }
    ),
    html.H3(
        children='''2001-2020''',
         style={
            'textAlign': 'center'
        }
    ),    
    html.Div(
    [html.H1("Rape:"),
    dcc.Graph(figure=fig)
    ]),
    html.Div(
    [html.H1("Domestic Violence: (Cruelty by Husband or his Relatives)"),
    dcc.Graph(figure=fig1)
    ]),
    html.H1(
        children='Crime Map:',
        style={
            'textAlign': 'center'
        }
    ),
     html.Div(
        [
            html.Div(
                [
                    dcc.Graph(
                        id='map-graph', 
                        figure= {
                            "data": [
                                    go.Scattermapbox(
                                    lat= list(df['LAT']),
                                    lon= list(df['LON']), 
                                    hoverinfo='text',
                                    mode= "markers",
                                    text=["Crime Rate:{}".format(i) for i in df['crimerate']],  
                                    
                                    marker= {
                                        "size": 6,
                                        "opacity": 0.7
                                    },
                                    name=i
                                    ) for i in df.NAME.unique() 
                            ],
                            "layout": layout_map
                        },
                        animate=True, 
                        #style={'margin-top': '20','height': '500','width':'500'}
                    ),
                ], className = 'row justify-content-center'        
       
     ),    
],
)
])
