import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dfs.lista_jogos import lista_jogos_df
import dash_ag_grid as dag
import dash

dash.register_page(__name__)

layout = dbc.Container(
    [
        dbc.Row(dbc.Col()),
        dbc.Row(dbc.Col()),
    ]
)
