import dash

dash.register_page(__name__, path="/", name="Tabela de Classificação")

import pandas as pd
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dfs.lista_jogos import lista_jogos_df
import dash_ag_grid as dag
from tools.criar_df_classificação import criar_df_classificação

filtro_temporada = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Temporada"),
            dcc.Dropdown(
                [{"label": c, "value": c} for c in lista_jogos_df["Ano"].unique()],
                value=lista_jogos_df["Ano"].unique().max(),
                id="temporada_dpdn",
            ),
        ],
    ),
    class_name="text-center mx-1 my-1",
)

frequencia_minima = dbc.Card(
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
    id="frequencia_minima",
    class_name="mx-1 my-1",
)

tabela_classificação = dag.AgGrid(
    id="tabela_classificação",
    defaultColDef={"sortable": True, "rezisable": True},
    columnDefs=[
        {
            "field": "#",
            "type": "numericColumn",
            "width": 30,
        },
        {"field": "JOGADOR", "width": 200, "sortable": False},
        {
            "field": "PTS",
            "width": 75,
        },
        {
            "field": "APRV",
            "width": 90,
            "valueFormatter": {"function": 'd3.format(".1%")(params.value)'},
        },
        {
            "field": "GOLS",
            "width": 75,
        },
        {
            "field": "MÉDIA",
            "width": 90,
            "valueFormatter": {"function": 'd3.format(".2f")(params.value)'},
        },
        {
            "field": "PJ",
            "width": 50,
        },
        {
            "field": "FREQ",
            "width": 90,
            "valueFormatter": {"function": 'd3.format(".1%")(params.value)'},
        },
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
    dashGridOptions={"animateRows": True, "rowSelection": "multiple"},
    style={"height": 850, "width": "100%"},
)


layout = dbc.Container(
    [
        dbc.Row([dbc.Col(filtro_temporada), dbc.Col(frequencia_minima)]),
        dbc.Row(dbc.Col(tabela_classificação)),
    ],
    fluid=True,
)


@callback(
    Output("df_filtrado_temporada_selecionada", "data"),
    Input("temporada_dpdn", "value"),
)
def filtrar_lista_jogos(temporada):
    df = lista_jogos_df
    df = df.loc[df["Ano"] == temporada]
    return df.to_dict("records")


@callback(
    Output("tabela_classificação", "rowData"),
    Output("linhas_filtradas_tabela_classificação", "data"),
    Input("min_pj", "value"),
    Input("df_filtrado_temporada_selecionada", "data"),
)
def create_table1(pj_min, linhas_temporada_selecionada):
    df = pd.DataFrame(linhas_temporada_selecionada)
    tabela_df = criar_df_classificação(df)
    tabela_df = tabela_df.loc[tabela_df["PJ"] >= pj_min]
    rowData = tabela_df.to_dict("records")

    return (rowData, rowData)


@callback(
    Output("linhas_selecionadas_temporada_classificação", "data"),
    Input("tabela_classificação", "selectedRows"),
)
def selecionar_linhas_tabela(selectedRows):
    return selectedRows
