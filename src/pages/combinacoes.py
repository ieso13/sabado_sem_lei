import sys

sys.path.insert(1, "C:\code\dash-app-ssl\sabado_sem_lei\src")

import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dfs.lista_jogos import lista_jogos_df
import pandas as pd
import dash_ag_grid as dag
from tools.criar_df_classificação import criar_df_classificação


dash.register_page(__name__, name="Dados Times", order=5)

check_filtro_jogadores1 = html.Div(
    [
        html.H6("Ativar Filtros Laterais"),
        dcc.Dropdown(
            options=["Sim", "Não"],
            value="Não",
            id="ativar_filtro_jogadores1",
            persistence=True,
            persistence_type="memory",
        ),
    ]
)

selecao_jogador = html.Div(
    [
        html.H6("Selecionar Jogador para Analisar"),
        dcc.Dropdown(
            id="input_jogador", options=sorted(lista_jogos_df["Jogador"].unique())
        ),
    ]
)

slicer_temporadas = html.Div(
    [
        html.H6("Selecionar Temporadas para Analisar"),
        dcc.RangeSlider(
            min=lista_jogos_df["Ano"].unique().min(),
            max=lista_jogos_df["Ano"].unique().max(),
            step=1,
            value=[
                lista_jogos_df["Ano"].unique().min(),
                lista_jogos_df["Ano"].unique().max(),
            ],
            id="slincer_temporadas",
            marks={
                i: "{}".format(i)
                for i in range(
                    lista_jogos_df["Ano"].unique().min(),
                    lista_jogos_df["Ano"].unique().max() + 1,
                    1,
                )
            },
        ),
    ]
)

tabela_junto = dag.AgGrid(
    id="tabela_junto",
    defaultColDef={"sortable": True, "rezisable": True},
    columnDefs=[
        {
            "field": "JOGADOR",
            "width": 175,
            "pinned": True,
        },
        {
            "field": "PJ",
            "width": 50,
        },
        # {
        #     "field": "PTS",
        #     "width": 75,
        # },
        {
            "field": "APRV",
            "width": 90,
            "valueFormatter": {"function": 'd3.format(".1%")(params.value)'},
        },
        # {
        #     "field": "GOLS",
        #     "width": 75,
        # },
        {
            "field": "MÉDIA",
            "width": 90,
            "valueFormatter": {"function": 'd3.format(".2f")(params.value)'},
        },
        # {
        #     "field": "FREQ",
        #     "width": 90,
        #     "valueFormatter": {"function": 'd3.format(".1%")(params.value)'},
        # },
        {
            "field": "S+",
            "width": 50,
        },
        {
            "field": "V",
            "width": 50,
        },
        {
            "field": "E",
            "width": 50,
        },
        {
            "field": "D",
            "width": 50,
        },
    ],
    dashGridOptions={"animateRows": True},
    style={"height": 750},
    columnSize="sizeToFit",
)

tabela_contra = dag.AgGrid(
    id="tabela_contra",
    defaultColDef={"sortable": True, "rezisable": True},
    columnDefs=[
        {
            "field": "JOGADOR",
            "width": 175,
            "pinned": True,
        },
        {
            "field": "PJ",
            "width": 50,
        },
        # {
        #     "field": "PTS",
        #     "width": 75,
        # },
        {
            "field": "APRV",
            "width": 90,
            "valueFormatter": {"function": 'd3.format(".1%")(params.value)'},
        },
        # {
        #     "field": "GOLS",
        #     "width": 75,
        # },
        {
            "field": "MÉDIA",
            "width": 90,
            "valueFormatter": {"function": 'd3.format(".2f")(params.value)'},
        },
        # {
        #     "field": "FREQ",
        #     "width": 90,
        #     "valueFormatter": {"function": 'd3.format(".1%")(params.value)'},
        # },
        {
            "field": "S+",
            "width": 50,
        },
        {
            "field": "V",
            "width": 50,
        },
        {
            "field": "E",
            "width": 50,
        },
        {
            "field": "D",
            "width": 50,
        },
    ],
    dashGridOptions={"animateRows": True},
    style={"height": 750},
    columnSize="sizeToFit",
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(check_filtro_jogadores1, width=2),
                dbc.Col(selecao_jogador, width=4),
                dbc.Col(slicer_temporadas, width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([html.H6("Estatísticas no Mesmo Time"), tabela_junto], width=6),
                dbc.Col(
                    [html.H6("Estatísticas no Time Adversário"), tabela_contra], width=6
                ),
            ]
        ),
    ],
    fluid=True,
    class_name="gx-2",
)


@callback(
    Output("tabela_junto", "rowData"),
    Output("tabela_contra", "rowData"),
    Input("slincer_temporadas", "value"),
    Input("input_jogador", "value"),
    Input("ativar_filtro_jogadores1", "value"),
    Input("linhas_filtradas_tabela_classificação", "data"),
)
def criar_tabelas_comp(temporadas, jogador, ativar_filtro_jogadores, jogadores_tabela):
    if len(temporadas) == 1:
        temporadas_selecionadas = temporadas
    else:
        temporadas_selecionadas = range(temporadas[0], temporadas[1] + 1, 1)

    df = lista_jogos_df.loc[lista_jogos_df["Ano"].isin(temporadas_selecionadas)]

    if ativar_filtro_jogadores == "Sim":
        jogadores_selecionados_df = pd.DataFrame(jogadores_tabela)
        df = df.loc[df["Jogador"].isin(jogadores_selecionados_df["JOGADOR"])]
    else:
        pass

    times_df = (
        df.groupby(["Ano", "Rodada", "Time"])["Jogador"].apply(list).reset_index()
    )

    if jogador:
        times_df["Jogador"] = times_df["Jogador"].apply(lambda x: jogador in x)
    else:
        pass

    times_df["Ano-Rodada"] = (
        times_df[["Ano", "Rodada"]].astype(str).apply("-".join, axis=1)
    )

    times_df = times_df.pivot(index="Ano-Rodada", columns="Time", values="Jogador")

    times_df = times_df.loc[(times_df[1] == True) | (times_df[2] == True)].replace(
        [True, False], ["Junto", "Contra"]
    )

    times_df = times_df.reset_index().melt(
        id_vars="Ano-Rodada", var_name="Time", value_name="Jogando"
    )

    times_df["Ano-Rodada-Time"] = (
        times_df[["Ano-Rodada", "Time"]].astype(str).apply("-".join, axis=1)
    )
    df["Ano-Rodada-Time"] = (
        df[["Ano", "Rodada", "Time"]].astype(str).apply("-".join, axis=1)
    )

    times_junto_df = times_df.loc[times_df["Jogando"] == "Junto"]

    lista_jogos_junto_df = df.loc[
        df["Ano-Rodada-Time"].isin(times_junto_df["Ano-Rodada-Time"])
    ]

    row_data_juntos = criar_df_classificação(lista_jogos_junto_df).to_dict("records")

    times_contra_df = times_df.loc[times_df["Jogando"] == "Contra"]

    lista_jogos_contra_df = df.loc[
        df["Ano-Rodada-Time"].isin(times_contra_df["Ano-Rodada-Time"])
    ]

    row_data_contra = criar_df_classificação(lista_jogos_contra_df).to_dict("records")

    return row_data_juntos, row_data_contra
