import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dfs.lista_jogos import lista_jogos_df
from PIL import Image
import dash_ag_grid as dag
import dash


# Criar DF tabela
def criar_df_classificação(df):
    num_jogos = df.groupby("Ano")["Rodada"].max().sum()
    dff = df.groupby("Jogador")[["Pontos", "Gols", "Destaques"]].sum()
    dff["Presença"] = df.groupby("Jogador")["Rodada"].count().astype(int)
    dff["Presença%"] = dff["Presença"] / num_jogos
    dff["Gols/Jogo"] = dff["Gols"] / dff["Presença"]
    dff["Aproveitamento%"] = dff["Pontos"] / (dff["Presença"] * 3)
    dff["Vitórias"] = (
        df.loc[df["Pontos"] == 3].groupby("Jogador")["Pontos"].size().astype(int)
    )
    dff["Empates"] = (
        df.loc[df["Pontos"] == 1].groupby("Jogador")["Pontos"].size().astype(int)
    )
    dff["Derrotas"] = (
        df.loc[df["Pontos"] == 0].groupby("Jogador")["Pontos"].size().astype(int)
    )
    dff = dff.replace(np.nan, 0)
    dff = dff.reset_index()
    dff = dff.sort_values(by=["Pontos"], ascending=False)
    dff.insert(0, "#", range(1, len(dff) + 1, 1))
    dff = dff[
        [
            "#",
            "Jogador",
            "Pontos",
            "Aproveitamento%",
            "Gols",
            "Gols/Jogo",
            "Presença",
            "Presença%",
            "Destaques",
            "Vitórias",
            "Empates",
            "Derrotas",
        ]
    ]
    dff = dff.rename(
        columns={
            "Jogador": "JOGADOR",
            "Pontos": "PTS",
            "Aproveitamento%": "APRV",
            "Gols": "GOLS",
            "Gols/Jogo": "MÉDIA",
            "Presença": "PJ",
            "Presença%": "FREQ",
            "Destaques": "S+",
            "Vitórias": "V",
            "Empates": "E",
            "Derrotas": "D",
        }
    )

    return dff


# COMPONENTS OF THE LAYOUT
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

grafico_gols_pontos = (
    html.Div(
        dcc.Graph(figure={}, style={"height": "80vh"}, id="gráfico_pontos_gols"),
    ),
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

check_filtro_jogadores = html.Div(
    [
        html.H6("Filtrar Conforme Filtro da Temporada"),
        dcc.Dropdown(
            options=["Sim", "Não"],
            value="Não",
            id="ativar_filtro_jogadores",
        ),
    ]
)

tabela_historica = dag.AgGrid(
    id="tabela_historica",
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
    dashGridOptions={"animateRows": True},
    style={"height": 850, "width": "100%"},
)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    use_pages=True,
)

SSL_LOGO = "C:\Code\sabado_sem_lei\src\assets\Escudo.jpg"

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    [
                        html.Img(src=SSL_LOGO, height="30px"),
                        dbc.NavbarBrand("Sábado Sem Lei", className="ms-2"),
                    ],
                    width={"size": "auto"},
                ),
                align="center",
                class_name="g-0",
            ),
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Nav(
                            [
                                dbc.NavItem(
                                    dbc.NavLink(page["name"], href=page["path"])
                                )
                                for page in dash.page_registry.values()
                            ],
                            navbar=True,
                        )
                    ],
                    width={"size": "auto"},
                ),
                align="center",
            ),
        ],
        fluid=True,
    ),
    color="primary",
    dark=True,
)

app.layout = dbc.Container(
    [
        navbar,
        dcc.Store(id="linhas_filtradas_tabela_classificação"),
        dcc.Store(id="df_filtrado_temporada_selecionada"),
        dcc.Store(id="linhas_selecionadas_temporada_classificação"),
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


@callback(
    Output("tabela_historica", "rowData"),
    Input("slincer_temporadas", "value"),
    Input("ativar_filtro_jogadores", "value"),
    Input("linhas_filtradas_tabela_classificação", "data"),
)
def criar_tabela_historica(temporadas, ativar_filtro_jogadores, jogadores_tabela):
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

    row_data = criar_df_classificação(df).to_dict("records")

    return row_data


@callback(
    Output("gráfico_pontos_gols", "figure"),
    Input("slincer_temporadas", "value"),
    Input("ativar_filtro_jogadores", "value"),
    Input("linhas_filtradas_tabela_classificação", "data"),
)
def criar_graph2(temporadas, ativar_filtro_jogadores, jogadores_tabela):
    if len(temporadas) == 1:
        temporadas_selecionadas = temporadas
    else:
        temporadas_selecionadas = range(temporadas[0], temporadas[1] + 1, 1)

    df = lista_jogos_df.loc[lista_jogos_df["Ano"].isin(temporadas_selecionadas)]
    tabela_df = pd.DataFrame(jogadores_tabela)

    if ativar_filtro_jogadores == "Sim":
        df = df.loc[df["Jogador"].isin(tabela_df["JOGADOR"])]
    else:
        pass

    dff = df.groupby("Jogador")[["Pontos", "Gols"]].sum()
    dff["PJ"] = df.groupby("Jogador")["Rodada"].count()
    dff["Gols/PJ"] = dff["Gols"] / dff["PJ"]
    dff["Pontos/PJ"] = dff["Pontos"] / dff["PJ"]
    grafico_gols_pontos = px.scatter(
        data_frame=dff,
        x="Pontos",
        y="Gols",
        size="PJ",
        color=dff.index,
        size_max=50,
        # text=dff.index,
    )
    grafico_gols_pontos.update_layout(showlegend=False, template="none")
    grafico_gols_pontos.update_traces(
        textposition="middle right", marker_color="rgba(0,0,0,0)"
    )

    for i, row in dff.iterrows():
        jogador = i.replace(" ", "-")
        grafico_gols_pontos.add_layout_image(
            dict(
                source=Image.open(f"src/assets/fotos/{jogador}.png"),
                xref="x",
                yref="y",
                xanchor="center",
                yanchor="middle",
                x=row["Pontos"],
                y=row["Gols"],
                sizex=int(row["PJ"] * 0.35),
                sizey=int(row["PJ"] * 0.35),
                sizing="contain",
                layer="above",
            )
        )

    return grafico_gols_pontos


if __name__ == "__main__":
    app.run_server(debug=True)
