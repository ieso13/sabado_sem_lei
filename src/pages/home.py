import dash

dash.register_page(__name__, path="/", order=1)

from dash import html

layout = html.H1("Home")
