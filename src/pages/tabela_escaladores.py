import pandas as pd
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

import dash_ag_grid as dag

import dash

from dfs.lista_jogos import lista_jogos_df


dash.register_page(__name__, name="Tabela de Escaladores", order=10)

# Estatísticas dos escaladores
escaladores_df = lista_jogos_df.loc[
    lista_jogos_df["Escalador"] == lista_jogos_df["Jogador"]
]

tabela_escaladores = escaladores_df.groupby("Jogador")[
    ["Pontos", "Gols", "Destaques"]
].sum()

tabela_escaladores["Presença"] = (
    escaladores_df.groupby("Jogador")["Rodada"].count().astype(int)
)

tabela_escaladores["Aproveitamento%"] = tabela_escaladores["Pontos"] / (
    tabela_escaladores["Presença"] * 3
)

tabela_escaladores = tabela_escaladores.reset_index().sort_values(
    by=["Presença"], ascending=False
)

tabela_escaladores = tabela_escaladores.rename(
    columns={
        "Jogador": "ESCALADOR",
        "Pontos": "PTS",
        "Aproveitamento%": "APRV",
        "Gols": "GOLS",
        "Presença": "PJ",
        "Destaques": "S+",
    }
)

tabela_escaladores = dag.AgGrid(
    id="tabela_escaladores",
    defaultColDef={"sortable": True, "rezisable": True},
    dashGridOptions={"animateRows": True, "rowSelection": "multiple"},
    style={"height": 850},
    rowData=tabela_escaladores.to_dict("records"),
    columnSize="sizeToFit",
    columnDefs=[
        {
            "field": "ESCALADOR",
            "width": 200,
            "sortable": False,
            "pinned": True,
        },
        {
            "field": "PJ",
            "width": 50,
        },
        {
            "field": "APRV",
            "width": 90,
            "valueFormatter": {"function": 'd3.format(".1%")(params.value)'},
        },
        {
            "field": "GOLS",
            "width": 50,
        },
        {
            "field": "S+",
            "width": 50,
        },
    ],
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(tabela_escaladores),
            ]
        ),
        dbc.Row(),
    ],
)
