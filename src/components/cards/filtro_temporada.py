from dash import dcc, html
import dash_bootstrap_components as dbc
from src.dfs.lista_jogos_temporada import lista_jogos_df

filtro_temporada = (
    dbc.Card(
        dbc.CardBody(
            [
                html.H6("Temporada"),
                dcc.Dropdown(
                    [
                        lista_jogos_df["Ano"].unique(),
                    ],
                    2023,
                    id="temporada_dpdn",
                ),
            ],
        ),
        class_name="text-center mx-1 my-1",
    ),
)
