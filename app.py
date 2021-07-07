from includes.about import about
from includes.navbar import navbar
from includes.home import home
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go 
from dash.dependencies import Input,Output,State
import dash_table
import io
import base64
import json
import datetime
import plotly.express as px
import folium
#import dash_table_experiments as dash_table


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,external_stylesheets])
app.config['suppress_callback_exceptions']=True
app.title = 'Geovisualization of Indian States'
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# ========================== MAP generation ===============================================
india_states = json.load(open("Data\states_india.geojson", "r"))
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]
df = pd.read_csv("Data\india_census.csv")
df["Density"] = df["Density[a]"].apply(lambda x: int(x.split("/")[0].replace(",", "")))
df["id"] = df["State or union territory"].apply(lambda x: state_id_map[x])
df["DensityScale"] = np.log10(df["Density"])
df["crimeScale"] = np.log10(df["Crime Against women"])
df["SexRatioScale"] = df["Sex ratio"] - 1000
fig = px.choropleth_mapbox(
    df,
    locations="id",
    geojson=india_states,
    color="DensityScale",
    #colorscale="Viridis",
    hover_name="State or union territory",
    hover_data=["Density"],
    title="India Population Density",
    mapbox_style="carto-positron",
    center={"lat": 24, "lon": 78},
    zoom=3,
    opacity=0.5,
)
fig1= px.choropleth_mapbox(
    df,
    locations="id",
    geojson=india_states,
    color="SexRatioScale",
    hover_name="State or union territory",
    hover_data=["Sex ratio"],
    title="India Sex Ratio",
    mapbox_style="carto-positron",
    center={"lat": 24, "lon": 78},
    zoom=3,
    opacity=0.5,
    color_continuous_scale=px.colors.diverging.balance,
    color_continuous_midpoint=0,
)
fig1.update_geos(fitbounds="locations", visible=False)
fig2= px.choropleth_mapbox(
    df,
    locations="id",
    geojson=india_states,
    color="crimeScale",
    hover_name="State or union territory",
    hover_data=["Crime Against women"],
    title="India Crime against women statewise",
    mapbox_style="carto-positron",
    center={"lat": 24, "lon": 78},
    zoom=3,
    opacity=0.5,
    color_continuous_scale=px.colors.diverging.balance,
    color_continuous_midpoint=0,
)

df1 = px.data.gapminder().query("year==2007")



# ========================== Data Processing ===============================================
df = pd.read_excel('Data/crime against women 2001-2020.xlsx')

tf = df
# print(df.head())
cols = df.columns
# Year list:
year_options = []
for year in df['Year'].unique():
    year_options.append({'label':str(year),'value':year})
state_options = []
for state in df['State/UT'].unique():
    state_options.append({'label':str(state),'value':state})

minYear = df['Year'].min()
maxYear = df['Year'].max()
#Crime head dictionary-LIST:
#With Sum aggr:
crimeDictS = {'Rape':sum, 'Kidnapping & Abduction':sum,'Dowry Deaths':sum,'Assault on women with intent to outrage her modesty ':sum,'Insult to modesty of women':sum,'Cruelty by Husband or his Relatives':sum,'Importation of Girls from foreign country':sum,'Immoral Traffic (P) Act':sum,'Dowry Prohibition Act':sum,'Indecent Representation of Women(P) Act':sum,'Commission of Sati Prevention Act':sum}
#Without aggr list:
crimeDict = ['Rape', 'Kidnapping & Abduction', 'Dowry Deaths','Assault on women with intent to outrage her modesty ','Insult to modesty of women', 'Cruelty by Husband or his Relatives','Importation of Girls from foreign country', 'Immoral Traffic (P) Act','Dowry Prohibition Act', 'Indecent Representation of Women(P) Act','Commission of Sati Prevention Act']
# crime list:
crimes = ['Rape', 'Kidnapping & Abduction', 'Dowry Deaths','Assault on women with intent to outrage her modesty ','Insult to modesty of women', 'Cruelty by Husband or his Relatives','Importation of Girls from foreign country', 'Immoral Traffic (P) Act','Dowry Prohibition Act', 'Indecent Representation of Women(P) Act','Commission of Sati Prevention Act']


# New df: removing year:
totalc = df.groupby(["State/UT"], as_index=False).agg(crimeDictS)
totalc['Total'] = totalc[crimeDict].sum(axis=1)
print(totalc.columns)
# ==========================  plots =============================================
plottab1 = html.Div(children=[
    # Plot 1:
    html.Div(children=[
        html.H1(style={'textAlign':'center'},children=[
            "Total Crime against Women in India",
        ]),           
        html.P(style={'textAlign':'center'},children=["("+str(minYear)+" - "+str(maxYear)+")"]),
        dcc.Graph(id='totalYear',
              figure={
                  'data':[go.Bar(
                      x=totalc['State/UT'],
                      y=totalc['Total'],
                  )],
                  'layout':go.Layout(title='State wise total crime against women',xaxis={'title':'States/UT'})
              })
    ]),
    # Plot 2:
    html.Div(children=[
        html.Hr(),
        html.H1('Total crime happened in a particular year ',style={'textAlign':'center'}),
        html.Div(children=[
           html.Label('Select Year:'),  
           dcc.Dropdown(id='year-picker',options=year_options,value=df['Year'].min(),style={'width':'500px'}),
           
        ]),
        html.Div(children=[
            dcc.Graph(id='perYear')
        ])
    ])
])
plottab2 =  html.Div([
    html.Div(className='row',children=[
        html.Div(className="col",children=[ 
        # Figure 2.1
           html.Div([
               html.Label('Select State/UT:'),
               dcc.Dropdown(id='selectState',options=state_options,value=df['State/UT'][0])
           ]),
           html.Div([
               html.Label('Select Sub-Crime:'),
               dcc.Dropdown(id='selectCrime',options=[{'label':i,'value':i} for i in crimes],value='Rape')
           ]),
         # Figure 2.2 
           html.H2("Forecast:"),
           dcc.Markdown(id='forecast'),
        ]),
        html.Div(className="col",children=[
           dcc.Graph(id="stateCrime"),
        ]),
    ]),
],style={'padding':10})

plottab3 =  html.Div([
    html.Div(className="row", children=[
        html.Div(className="col", children=[
             html.Div([
                html.Label("Select State: "),
                dcc.Dropdown(id='statez',options=state_options,value='Andhra Pradesh'),
                html.Label("Select Crime 1: "),
                dcc.Dropdown(id='crimex',options=[{'label':i,'value':i} for i in crimeDict ],value='Rape'),
                html.Label("Select Crime 2: "),
                dcc.Dropdown(id='crimey',options=[{'label':i,'value':i} for i in crimeDict ],value='Dowry Deaths'),
                html.Hr(),
                html.P(id='corrRes1',children=[
                        "Correlation value: ",
                    html.B(id='corrRes'),
                    html.Br(),
                        "Correlation degree: ",
                    html.B(id='corrType')
                ],style={'width':'30%','display':'inline-block'})
            ]),
        ]),
        html.Div(className='col',children=[
            dcc.Graph(id='corr-graphic')
        ])
    ])
    
  
],style={'padding':10})

plottab4 =  html.Div([    
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
])
plottab6= html.Div([
        dbc.Button(["Context",
            html.I(className="fas fa-plus plus-icon")
        ], id="open-body-scroll", className="open-modal-btn"),
        dbc.Modal([
            dbc.ModalHeader("Context"),
            dbc.ModalBody([
                html.P("Geovisualization involves the interactive exploration of geographically-referenced information graphics to prompt visual thinking about complex geographic patterns and processes"),
                html.P("Visual thinking informs decision-making regarding investigation of Crime against women incidence across different states and UT of India and foreseen the area of developememt to ensure women safety."),
                html.P("Interactive mapping allows crime analysts to identify crime hot spots with engaging exploratory data analysis, along with other trends and patterns"),
                html.P("Geovisualization integrates visual exploration, analysis, synthesis, and presentation of geospatial data."),
                html.P(["To know more visit: ",
                    html.A('NRSC', href="https://bhuvan-app1.nrsc.gov.in/gisviewer/#", target="_blank", style={"color": "#338267"})
                ], className="source-modal-context-text", style={"fontSize": "0.9em"})
            ], className="modal-context-text"),
            dbc.ModalFooter(
                dbc.Button(
                "Close", id="close-body-scroll", className="ml-auto close-modal-btn"
                )
            ),
        ],
        id="modal-body-scroll",
        scrollable=True
        ),
        dbc.Button(["Inference",
            html.I(className="fas fa-plus plus-icon")
        ], id="open-body-scroll-2", className="open-modal-btn"),
        dbc.Modal([
            dbc.ModalHeader("Interacting with this Dashboard Shows"),
            dbc.ModalBody([
                html.Li([
                        html.Span("Highest crime is Domestic violence followed by Rape"),                         
                ]),
                html.Li([
                        html.Span("Dangerous State for women is uttra pradesh followed by Rajasthan and delhi"),                         
                ]),
                html.Li([
                        html.Span("Whereas South and North east Part of India has reported relatively lower crime"),                         
                ]),                
                html.Li([
                        html.Span("Crime against women increases along with increase in year most of the cases are not even reported"),                         
                ]),               
                
            ], className="modal-tips"),
            dbc.ModalFooter(
                dbc.Button(
                "Close", id="close-body-scroll-2", className="ml-auto close-modal-btn"
                )
            ),
        ],
        id="modal-body-scroll-2",
        scrollable=True
        ),
        dbc.Button(["Data Sources",
            html.I(className="fas fa-plus plus-icon")
        ], id="open-body-scroll-3", className="open-modal-btn"),
        dbc.Modal([
            dbc.ModalHeader("Data Sources"),
            dbc.ModalBody([
                html.Li([
                    html.Span("Crime against women State/UT"),
                    html.Span([
                        html.A("NCRB",href="https://github.com/SrinithiKrishna/Geospatial-Datasets/blob/main/crime%20against%202001-2020.xlsx", target="_blank", style={"fontStyle": "italic", "color": "#338267"}),                        
                    ], style={"fontSize": "0.8em"})
                ], style={"marginLeft": "15px"}),
                html.A([
                    html.Button([
                        html.I(className="fas fa-file-csv", style={"fontSize": "25px", "verticalAlign": "middle"}),
                        html.Span("Download CSV", style={"marginLeft": "10px", "verticalAlign": "middle", "fontWeight": "bolder", "fontSize": "1.2em"})
                    ], className="download-button") 
                ], href="Data/india_census.csv", download="india_census.csv"),
                html.Li([
                    html.Span("India Statewise Centroids "),
                    html.Span([
                        html.Span("(source: ", style={"fontStyle": "italic"}),
                        html.A("Kaggle",href="Data/states_india.geojson", target="_blank", style={"fontStyle": "italic", "color": "#338267"}),
                        html.Span("):", style={"fontStyle": "italic"})
                    ], style={"fontSize": "0.8em"})
                ], style={"marginLeft": "15px"}),
                html.A([
                    html.Button([
                        html.I(className="fas fa-file-csv", style={"fontSize": "25px", "verticalAlign": "middle"}),
                        html.Span("Download Geojson", style={"marginLeft": "10px", "verticalAlign": "middle", "fontWeight": "bolder", "fontSize": "1.2em"})
                    ], className="download-button") 
                ], href="Data/states_india.geojson", download="Data/states_india.geojson"),
                html.Li([
                    html.Span("India Census Data"),
                    html.Span([
                        html.Span("(source: ", style={"fontStyle": "italic"}),
                        html.A("data.gov.in",href="https://data.gov.in/", target="_blank", style={"fontStyle": "italic", "color": "#338267"}),
                        html.Span("):", style={"fontStyle": "italic"})
                    ], style={"fontSize": "0.8em"})
                ], style={"marginLeft": "15px"}),
                html.A([
                    html.Button([
                        html.I(className="fas fa-file-csv", style={"fontSize": "25px", "verticalAlign": "middle"}),
                        html.Span("Download CSV", style={"marginLeft": "10px", "verticalAlign": "middle", "fontWeight": "bolder", "fontSize": "1.2em"})
                    ], className="download-button") 
                ], href="Data/india_census.csv", download="Data/india_census.csv"),                    
            ], className="modal-data-sources"),
            dbc.ModalFooter(
                dbc.Button(
                "Close", id="close-body-scroll-3", className="ml-auto close-modal-btn"
                )
            ),
        ],
        id="modal-body-scroll-3",
        scrollable=True
        ),
        dbc.Button(["Doc. Resources",
            html.I(className="fas fa-plus plus-icon")
        ], id="open-body-scroll-4", className="open-modal-btn"),
        dbc.Modal([
            dbc.ModalHeader("Documentation Sources"),
            dbc.ModalBody([
                    html.Li([
                        html.Span("Dash: "),
                        html.A("https://dash.plot.ly/", href="https://dash.plot.ly/", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                    ]),
                    html.Li([
                        html.Span("Plotly Python: "),
                        html.A("https://plot.ly/python/", href="https://plot.ly/python/", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                    ]),
                    html.Li([
                        html.Span("Plotly/Dash Forum: "),
                        html.A("https://community.plot.ly/c/dash", href="https://community.plot.ly/c/dash", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                    ]),
                    html.Li([
                        html.Span("Dash Bootstrap Components: "),
                        html.A("https://dash-bootstrap-components.opensource.faculty.ai/", href="https://dash-bootstrap-components.opensource.faculty.ai/", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                    ]),
                    html.Li([
                        html.Span("Indian Government Open Source Data Portal: "),
                        html.A("https://data.gov.in/", href="https://data.gov.in/", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                    ]),
                    html.Li([
                        html.Span("NCRB: "),
                        html.A("https://ncrb.gov.in/en/crime-india", href="https://ncrb.gov.in/en/crime-india", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                    ]),
                    html.Li([
                        html.Span("Folium: "),
                        html.A("http://python-visualization.github.io/folium/", href="http://python-visualization.github.io/folium/", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                    ]),
                    html.Li([
                        html.Span("Leaflet: "),
                        html.A("https://leafletjs.com/reference-1.7.1.html", href="https://leafletjs.com/reference-1.7.1.html", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                    ]),
                    html.Li([
                        html.Span("Cyber Crime Portal: "),
                        html.A("https://cybercrime.gov.in/", href="https://cybercrime.gov.in/", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                    ]),
                    html.Li([
                        html.Span("Python & GIS: "),
                        html.A("https://automating-gis-processes.github.io/CSC18/", href="https://automating-gis-processes.github.io/CSC18/", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                    ]),
                    html.Li([
                        html.Span("Mapbox: "),
                        html.A("https://www.mapbox.com/", href="https://www.mapbox.com/", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                    ]),
                    html.Li("Python Libraries: "),
                    html.Ul([
                        html.Li([
                            html.Span("Pandas: "),
                            html.A("https://pandas.pydata.org/pandas-docs/stable/", href="https://pandas.pydata.org/pandas-docs/stable/", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                        ]),
                        html.Li([
                            html.Span("Plotly: "),
                            html.A("https://plotly.com/python/getting-started/", href="https://plotly.com/python/getting-started/", target="_blank", style={"color": "#338267", "fontSize": "0.9em"})
                        ])
                    ])
            ], className="modal-doc-sources", style={"marginLeft": "20px"}),
            dbc.ModalFooter(
                dbc.Button(
                "Close", id="close-body-scroll-4", className="ml-auto close-modal-btn"
                )
            ),
        ],
        id="modal-body-scroll-4",
        scrollable=True
        ),
        html.Br(),
           dcc.Link('Go back to home', href='home'), 
]) 


plottab5= html.Div([
    html.H1('An overview of Indian states Map generated using Folium'),
    html.Iframe(id='map', srcDoc=open('Map1.html', 'r').read(), width='100%', height='900'),
    html.Button(id='map-submit-button', n_clicks=0, children='Submit'),
])

plottab7= html.Div([
    html.H1('Map with Multiple Layer Support,Miles & Distance calculation enabled with canvas and export features:'),
    html.Iframe(id='map', srcDoc=open('Maps.html', 'r').read(), width='100%', height='900'),
    html.Button(id='map-submit-button', n_clicks=0, children='Submit'),
])
plottab8= html.Div([
    html.H1(
        children='Choropleth map',
        style={
            'textAlign': 'center'
        }
    ),   
    dcc.Graph(
        id='example-graph-2',
        figure=fig,style={'width': '90vh', 'height': '90vh','display': 'inline-block'}
    ),
    dcc.Graph(
        id='example-graph-3',
        figure=fig2,style={'width': '90vh', 'height': '90vh','display': 'inline-block'}
    ),
    dcc.Graph(
        id='example-graph-4',
        figure=fig1,style={'width': '90vh', 'height': '90vh','display': 'inline-block'}
    ),   
    dcc.Graph(
            
            id='graph3',
            figure=px.scatter_geo(df1, locations="iso_alpha", color="continent",
                     hover_name="country", size="pop",animation_frame="year",
                     projection="natural earth"),style={'width': '90vh', 'height': '60vh','display': 'inline-block'}
        ),
     ])


# ========================== Routes: ============================================
# Nav bar:
navbar = navbar
# home:
home = home
# about
about = about
#map


# ========================== TABS ===============================================

tab1 = dbc.Card(
    [
      plottab1,
    ],
    body=True,
)

tab2 = dbc.Card(
    [
      plottab2,
    ],
    body=True,
)
tab3 = dbc.Card(
    [
      plottab3,
    ],
    body=True,
)
tab4 = dbc.Card(
    [
        html.Img(src="assets/Images/Tabimage.png"),
        html.P('DataFrame columns names must be same as given below:'),
        html.P(['State/UT, Rape, Kidnapping & Abduction, Dowry Deaths,Assault on women with intent to outrage her modesty,Insult to modesty of women', 'Cruelty by Husband or his Relatives,Importation of Girls from foreign country, Immoral Traffic (P) Act,Dowry Prohibition Act', 'Indecent Representation of Women(P) Act, Commission of Sati Prevention Act,Total']),
        plottab4,
        html.P("Restart app after uploading.")
    ],
    body=True,
)
tab5 = dbc.Card(
    [        
           
        plottab5,
        html.P("Map success.")
    ],
    body=True,
)
tab6 = dbc.Card(
    [
      plottab6,
    ],
    body=True,
)
tab7 = dbc.Card(
    [
      plottab7,
    ],
    body=True,
)
tab8 = dbc.Card(
    [
      plottab8,
    ],
    body=True,
)

caw = dbc.Tabs(
    [ 
          dbc.Tab(tab1, label="Total C.A.W", className="mt-3"),  
          dbc.Tab(tab2, label="States and Sub-Crimes", className="mt-3"),
          dbc.Tab(tab3, label="Crimes Correlation", className="mt-3"),          
          dbc.Tab(tab5, label="Geovisualization", className="mt-3"),          
          dbc.Tab(tab7, label="Heat map", className="mt-3"),
          dbc.Tab(tab8, label="choropleth map", className="mt-3"),
          dbc.Tab(tab4, label="Add DataFrame", className="mt-3"),
          dbc.Tab(tab6, label="Download the dataset", className="mt-3"),
    ]
)




# ========================= page layout =========================================
app.layout = html.Div(
    [        
        dcc.Location(id="url", pathname="/home"),
        navbar,
        html.Div(className="container-fluid", id="content", style={"padding": "20px"}),
      
    ]
)

# ====================== Plotings ============================================

# TAB 1 : STARTS
@app.callback(Output(component_id='perYear',component_property='figure'),
             [Input(component_id='year-picker',component_property='value')])
def update_figure(selected_year):
    filtered_df = df[df['Year']==selected_year]
    traces = [go.Bar(
        x = filtered_df['State/UT'],
        y = filtered_df['Total Crimes Against Women']
    )]
    return {
        'data':traces,
        'layout':go.Layout(title='Total crime in the year '+str(selected_year),xaxis={'title':'States/UT'})
    }
# TAB 1 ENDS
# TAB 2 : STARTS
@app.callback(Output('stateCrime','figure'),
            [Input('selectState','value'),
            Input('selectCrime','value')])
def state_crime_graph(sstate,scrime):
    filter_state = df[df['State/UT']==sstate]
    traces = [go.Scatter(
        x = filter_state['Year'],
        y = filter_state[scrime],
        name = scrime,
        fill = 'tonexty',
        mode = 'lines+markers'
    )]
    return {
        'data':traces,
        'layout':go.Layout(title ='{} cases in {}'.format(scrime,sstate),
                           xaxis={'title':'Year'},
                           yaxis={'title':'cases of '+scrime},
                           hovermode='closest')
    }

# Forecast:
def pattern(a,b,c):
    if(a == 1):
            if(b == 1):
                if(c==1):return "Higher chances of an increase"
                else:return "Medium chances of an decrease"
            elif(b == 0):
                if(c == 1):return "Medium chances of an increase"      
                else:return "High chances of an decrease"
    elif(a == 0):
            if(b == 0):
                if(c == 0):return "Higher chances of decrease"
                else:return "Lower chances of increase"
            elif(b==1):
                if(c == 0):return "Lower chances of decrease"
                else:return "Higher chances of increase"

@app.callback(Output('forecast','children'),
             [Input('selectState','value'),
              Input('selectCrime','value')])
def forecast_update(sstate,scrime):
    y1 = df['Year'].max()
    y2 = y1-1
    y3 = y2-1
    y4 = y3-1
    x1 = list(df[(df['State/UT']==sstate) & (df['Year']==y1)][scrime])
    x2 = list(df[(df['State/UT']==sstate) & (df['Year']==y2)][scrime])
    x3 = list(df[(df['State/UT']==sstate) & (df['Year']==y3)][scrime])
    x4 = list(df[(df['State/UT']==sstate) & (df['Year']==y4)][scrime])
    if((sstate=='Telangana') & (y1 == 2015)):
         s1=0
         s2=0
         if((x1[0] - x2[0]) > 0):
              s3 = 1
         else:
              s3 = 0
    else:
         if((x3[0] - x4[0]) > 0):
              s1 = 1
         else:
              s1 = 0
         if((x2[0] - x3[0]) > 0):
              s2 = 1
         else:
              s2 = 0
         if((x1[0] - x2[0]) > 0):
              s3 = 1
         else:
              s3 = 0
    res = pattern(s1,s2,s3)
    cast = "> {} has {} in {} in the year {} ,considering constant current policies.".format(sstate,res,scrime,str(y1+1))
    return cast
# TAB 2 ENDS
# TAB 3 STARTS
@app.callback(Output('corr-graphic','figure'),
             [Input('crimex','value'),
              Input('crimey','value'),
              Input('statez','value')])
def update_graph(xaxis_name,yaxis_name,state_name):
    filter_tf = tf[tf['State/UT']==state_name]
    total = filter_tf['Total Crimes Against Women'].sum()
    return {'data':[go.Scatter(x=filter_tf[xaxis_name],
                               y=filter_tf[yaxis_name],
                               text = filter_tf['Year'],
                               mode = 'markers',
                               marker=dict(size=(filter_tf['Total Crimes Against Women']/total)*1000,color=filter_tf['Total Crimes Against Women'],showscale=True)   
                               )],
           'layout':go.Layout(title =  'Crime correlation in '+state_name, 
                              xaxis = {'title':xaxis_name},
                              yaxis = {'title':yaxis_name},
                              hovermode='closest')
            }

@app.callback(Output('corrRes','children'),
             [Input('crimex','value'),
              Input('crimey','value'),
              Input('statez','value')])
def corr_result(xvalue,yvalue,zvalue):
    filter_tf = tf[tf['State/UT']==zvalue]
    Correlation = filter_tf[xvalue].corr(filter_tf[yvalue])
    strcorr = str(round(Correlation,1))
    if(strcorr != 'nan'):
        r = strcorr
    else:
        r = '0'
    return r

def corr_check(corr):
    if(corr > 0.0):
        if(corr >= 0.5 and corr < 2.0):
            return 'Highly Positive'
        elif(corr >= 0.3 and corr < 0.5):
            return 'Moderately Positive'
        elif(corr < 0.3):
            return'Low positive'    
    elif(corr == 0):
        return 'No correlation'
    else:
        return 'Negative'

@app.callback(Output('corrType','children'),
             [Input('crimex','value'),
              Input('crimey','value'),
              Input('statez','value')])
def corr_type(xvalue,yvalue,zvalue):
    filter_tf = tf[tf['State/UT']==zvalue]
    Correlation = filter_tf[xvalue].corr(filter_tf[yvalue])
    corri = round(Correlation,1)
    strcorr = str(corri)
    if(strcorr == 'nan'):
        rtype = 'No correlation'
    else:
        rtype = corr_check(corri)
    return rtype

# TAB 3 ENDS
# TAB 4 STARTS:
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            newdf = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
            updatedf = df.append(newdf)
            updatedf.to_excel('Data/crime against women 2001-2020.xlsx',index=False)


        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            newdf = pd.read_excel(io.BytesIO(decoded))
            updatedf = df.append(newdf)
            updatedf.to_excel('Data/crime against women 2001-2020.xlsx',index=False)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
        html.H4("Dataframe added!"),
        # dash_table.DataTable(
        #     data=updatedf.to_dict('rows'),
        #     columns=[{'name': i, 'id': i} for i in updatedf.columns]
        # ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children




#download dataset
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

app.callback(
    Output("modal-body-scroll", "is_open"),
    [
        Input("open-body-scroll", "n_clicks"),
        Input("close-body-scroll", "n_clicks"),
    ],
    [State("modal-body-scroll", "is_open")
    ],
)(toggle_modal)

app.callback(
    Output("modal-body-scroll-2", "is_open"),
    [
        Input("open-body-scroll-2", "n_clicks"),
        Input("close-body-scroll-2", "n_clicks"),
    ],
    [State("modal-body-scroll-2", "is_open")
    ],
)(toggle_modal)

app.callback(
    Output("modal-body-scroll-3", "is_open"),
    [
        Input("open-body-scroll-3", "n_clicks"),
        Input("close-body-scroll-3", "n_clicks"),
    ],
    [State("modal-body-scroll-3", "is_open")
    ],
)(toggle_modal)

app.callback(
    Output("modal-body-scroll-4", "is_open"),
    [
        Input("open-body-scroll-4", "n_clicks"),
        Input("close-body-scroll-4", "n_clicks"),
    ],
    [State("modal-body-scroll-4", "is_open")
    ],
)(toggle_modal)

# ==========================Footer==================================
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>       
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <link href="https://fonts.googleapis.com/css?family=Nunito:400,600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.0/css/all.css" integrity="sha384-REHJTs1r2ErKBuJB0fCK99gCYsVjwxHrSU0N7I1zl9vZbggVJXRMsv/sLlOAGb4M" crossorigin="anonymous">
        {%favicon%}
        {%css%}
    </head>
    <body>              
        {%app_entry%}
        
        <footer>
        {%config%}
            {%scripts%}
            {%renderer%}          
                <div class="footer">
                    <h3 class="footer-title"> &copy; Srinithi Krishna</h3>
                    <div class="footer-icons">
                    
                    <a aria-label="My Github" target="_blank" href="https://github.com/SrinithiKrishna"><i class="icon fab fa-github-alt" aria-hidden="true"></i></a>
                    <a aria-label="Youtube" target="_blank" href="https://www.youtube.com/c/Eduhikethinker/videos"><i class="icon fab fa-youtube" aria-hidden="true"></i></a>
                 
                </div>
                </div>  
        </footer>
    </body>
</html>
'''
# ========================== Route Controller ==================================
@app.callback(Output("content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/home":
        return home
    if pathname == "/about":
        return about
    if pathname == "/caw":
        return caw
    else:
        return html.P("Adding Soon...")         
    # if not recognised, return 404 message
    
# ========================== Server ============================================

if __name__ == "__main__":
    app.run_server(debug=True)
