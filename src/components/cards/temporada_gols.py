from dash import dcc, html
import dash_bootstrap_components as dbc


temporada_gols = (
    dbc.Card(
        dbc.CardBody(
            [
                html.H6("Gols"),
                html.H4(num_gols),
            ],
        ),
        class_name="text-center mx-1 my-1",
    ),
)
