import pandas as pd
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
from dfs.lista_jogos import lista_jogos_df
import dash_ag_grid as dag
from tools.criar_df_classificação import criar_df_classificação
import dash


dash.register_page(__name__, name="Tabela de Classificação", order=2)


filtro_temporada = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Temporada"),
            dcc.Dropdown(
                [{"label": c, "value": c} for c in lista_jogos_df["Ano"].unique()],
                value=lista_jogos_df["Ano"].unique().max(),
                id="temporada_dpdn",
                persistence=True,
                persistence_type="memory",
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
                persistence=True,
                persistence_type="memory",
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
            "field": "make",
            "checkboxSelection": True,
            "headerCheckboxSelection": True,
            "width": 5,
        },
        {
            "field": "#",
            "type": "numericColumn",
            "width": 45,
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
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            filtro_temporada,
                        ),
                        dbc.Row(frequencia_minima),
                    ],
                    width=3,
                ),
                dbc.Col(tabela_classificação),
            ]
        ),
        dbc.Row(),
    ],
    # fluid=True,
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
    [
        Output("tabela_classificação", "rowData"),
        Output("linhas_filtradas_tabela_classificação", "data"),
        Output("tabela_classificação", "selectedRows"),
        Input("min_pj", "value"),
        Input("df_filtrado_temporada_selecionada", "data"),
        State("linhas_selecionadas_temporada_classificação", "data"),
    ],
)
def create_table1(pj_min, linhas_temporada_selecionada, linhas_ja_selecionadas):
    df = pd.DataFrame(linhas_temporada_selecionada)
    tabela_df = criar_df_classificação(df)
    tabela_df = tabela_df.loc[tabela_df["PJ"] >= pj_min]
    rowData = tabela_df.to_dict("records")
    selectedRows = linhas_ja_selecionadas

    return (rowData, rowData, selectedRows)


@callback(
    Output("linhas_selecionadas_temporada_classificação", "data"),
    Input("tabela_classificação", "selectedRows"),
)
def selecionar_linhas_tabela(selectedRows):
    return selectedRows
