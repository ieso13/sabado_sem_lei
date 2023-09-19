from dash import dcc, html
import dash_bootstrap_components as dbc


frequencia_minima = (
    dbc.Card(
        dbc.CardBody(
            [
                html.H6("Presença Mínima"),
                dcc.Input(
                    id="min_pj",
                    type="number",
                    placeholder="Número Mínimo de Rodadas",
                    value=0,
                ),
            ],
        ),
        class_name="mx-1 my-1",
    ),
)
