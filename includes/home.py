import dash
from dash.dependencies import Input, Output
import dash_gif_component as gif
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_player as player
import json
import pandas as pd
df = pd.read_csv('Data/state wise centroids.csv')
home= html.Div(children=[   
     html.Div([
                html.Div([
                    html.Div([                        
                        html.Div([
                        html.Div([
                             gif.GifPlayer(
                             gif='assets/Images/wallcrop.gif',
                             still='assets/Images/wall.png',
                             autoplay=True,
                             )
                            ], className="media-body")                          
                    ], className="media pb-6 pt-4"),
                    html.Div([
                        html.Br(),
                        html.P("Geovisualization provides a deep insights of various Socio-economic problems of Indian States.", className="lead"),
                        
                    ])                  
                ], className="d-flex flex-column justify-content-start align-items-center rounded-lg shadow-lg p-3 rounded dashboard-header")
            ],className="w-85 mb-9" ), 
    html.Div([
                html.Div([

                        html.Img(src="assets/Images/indiaglobe.png", width="120", height="120", className="img-logo align-self-center"),
                        html.Div([
                            html.H1(['Geospatial', html.Br(),"visualization", html.Br() ,'Dashboard'])
                        ], className="media-body")
                    ], className="media pb-5 pt-2"),
                    html.P("A web-based visualization tool that allows users to connect to geospatial datasets of varying structure and complexity and flexibly explore patterns by performing spatial, temporal or attribute-level queries through interaction. By making exploratory geospatial data analysis accessible to non-technical users thus supports planning experts in formulating evidence-based decisions and, when used by the public, contributes to a more informed citizenship.A step towards collobarative decision making allows the top level higher authorities and Decision makers to foster the Decision making process.Exploratory visualizations of Complex and Large Datasets helps to understand the Complex Problems and area of improvements of different states in a clear visualization makes it understandable even for a novice. In this reasearch project we are focussing on Crime against women under IPC ", className="lead"),
                    
                ], className="d-flex flex-column justify-content-start align-items-center rounded-lg shadow-lg p-3 rounded dashboard-header")
            ], className="w-75 mb-4"),            
        html.Div([
                html.Div([
                    html.Div([ 
                        dbc.CardBody(
            [
                html.H4("      Crime Against women   ", className="card-title"),
                html.P(
                    "Major crime against women in our country are : Rape,Kidnapping & Abduction,Dowry Deaths,Assault on women with intent to outrage her modesty"
                    "Insult to modesty of women,Cruelty by husband or his relatives.",
                    className="card-text",
                ),             ]
        ),                       
        html.Img(src="assets/Images/crimeeye.png", width="680", height="300", className="img-logo align-self-center"),
                        
                    ], className="mb-4"),                    
                ], className="d-flex flex-column justify-content-start align-items-center rounded-lg shadow-lg p-3 rounded dashboard-header")
            ], className="col-sm-8 col-lg-6"),
    html.Div(        
        className="d-flex flex-column justify-content-start align-items-center rounded-lg shadow-lg p-3 rounded dashboard-header",
        children=dcc.Graph(
            id='graph',
            figure={
                'data': [{
                    'lat': df.Latitude, 'lon': df.Longitude, 'type': 'scattermapbox'
                }],
                'layout': {
                    'mapbox': {
                        'accesstoken': (
                            'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3M' +
                            'DBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw'
                        )
                    },
                    'margin': {
                        'l': 0, 'r': 0, 'b': 0, 't': 0
                    },
                }
            }
        )
    ),    
], className="row justify-content-center")
