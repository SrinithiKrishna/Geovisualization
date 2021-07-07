import dash
from dash_bootstrap_components._components.NavItem import NavItem
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
navbar = dbc.NavbarSimple(
    children=[
        #html.H1("Geovisualization Portal", style={"textAlign": "center","textColor":"white"}),
        #html.Img(src="assets/indiaglobe.png", width="60", height="50",style={"imgAlign": "left"}),                 
        dbc.NavItem(dbc.NavLink("Home", href="/home")),
        dbc.NavItem(dbc.NavLink("Crime Trends", href="/about")),
        #dbc.NavItem(dbc.NavLink("Crime Against women", href="/caw")),
        dbc.DropdownMenu(
            children=[                
                dbc.DropdownMenuItem("CAG visualization", href="/caw"),
                dbc.DropdownMenuItem("Other crimes", href=""),
            ],
            nav=True,
            in_navbar=True,
            label="Crime Insights",
        ),
    ],
    brand="Geovisualization Portal",
    brand_href="home",
    color="#280668",
    dark=True,
    sticky="top",
)