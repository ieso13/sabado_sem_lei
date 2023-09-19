from dash import dcc, html
import dash_bootstrap_components as dbc

temporada_partidas_jogadas = (
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H6("Partidas Jogadas"),
                    html.H4(num_jogos),
                ],
            ),
        ],
        class_name="text-center mx-1 my-1",
    ),
)
