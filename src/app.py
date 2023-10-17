import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
from dash.dash_table import DataTable, FormatTemplate
import dash_bootstrap_components as dbc
from dfs.lista_jogos import lista_jogos_df
from PIL import Image
import dash_ag_grid as dag


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

temporada_partidas_jogadas = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H6("Partidas Jogadas"),
                html.H4(children=[], id="temporada_partidas_jogadas"),
            ],
        ),
    ],
    class_name="text-center mx-1 my-1",
)

temporada_gols = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Gols"),
            html.H4(children=[], id="temporada_gols"),
        ],
    ),
    class_name="text-center mx-1 my-1",
)


temporada_media_gols = dbc.Card(
    dbc.CardBody(
        [
            html.H6("Gols/Partida"),
            html.H4(children=[], id="temporada_media_gols"),
        ],
    ),
    class_name="text-center mx-1 my-1",
)

grafico_classificação = html.Div(
    dcc.Graph(figure={}, style={"height": "80vh"}, id="graph1"),
)

slicer_rodadas_selecionadas = (
    (
        html.Div(
            id="slicer-rodadas",
        )
    ),
)


tabela_classificação = html.Div(
    id="table1",
    children=[],
    style={"max-height": "85vh", "overflow": "auto"},
)


grafico_gols_pontos = (
    html.Div(
        dcc.Graph(figure={}, style={"height": "80vh"}, id="graph2"),
    ),
)


grafico_mediagols_mediapontos = html.Div(
    dcc.Graph(figure={}, style={"height": "80vh"}, id="graph3"),
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
            id="my-range-slider",
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
        html.H6("Filtrar Jogadores Igual Acima"),
        dcc.Dropdown(
            options=["Sim", "Não"],
            value="Não",
            id="ativar_filtro_jogadores",
        ),
    ]
)

tabela_historica = dag.AgGrid(
    id="tabela_historica",
    columnDefs=[
        {
            "field": "#",
            "resizable": True,
            "type": "numericColumn",
            "width": 30,
            "sortable": True,
        },
        {"field": "JOGADOR", "resizable": True, "width": 200},
        {
            "field": "PTS",
            "resizable": True,
            "width": 75,
            "sortable": True,
        },
        {
            "field": "APRV",
            "resizable": True,
            "width": 90,
            "sortable": True,
            "valueFormatter": {"function": 'd3.format(".1%")(params.value)'},
        },
        {
            "field": "GOLS",
            "resizable": True,
            "width": 75,
            "sortable": True,
        },
        {
            "field": "MÉDIA",
            "resizable": True,
            "width": 90,
            "sortable": True,
            "valueFormatter": {"function": 'd3.format(".2f")(params.value)'},
        },
        {
            "field": "PJ",
            "resizable": True,
            "width": 50,
            "sortable": True,
        },
        {
            "field": "FREQ",
            "resizable": True,
            "width": 90,
            "sortable": True,
            "valueFormatter": {"function": 'd3.format(".1%")(params.value)'},
        },
        {
            "field": "S+",
            "resizable": True,
            "width": 50,
            "sortable": True,
        },
        {
            "field": "V",
            "resizable": True,
            "width": 50,
            "sortable": True,
        },
        {
            "field": "E",
            "resizable": True,
            "width": 50,
            "sortable": True,
        },
        {
            "field": "D",
            "resizable": True,
            "width": 50,
            "sortable": True,
        },
    ],
    dashGridOptions={"animateRows": True},
    style={"height": 850, "width": "100%"},
)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardImg(
                            src="./assets/Escudo.jpg",
                            style={"height": "75px", "width": "75px"},
                        ),
                        class_name="center mx-1 my-1 align-middle",
                    ),
                    width=1,
                ),
                dbc.Col(
                    html.H1(
                        "Sábado sem Lei",
                    ),
                    width=3,
                ),
                dbc.Col(
                    filtro_temporada,
                    width=2,
                ),
                dbc.Col(
                    frequencia_minima,
                    width=2,
                ),
                dbc.Col(
                    temporada_partidas_jogadas,
                    width=2,
                ),
                dbc.Col(
                    temporada_gols,
                    width=1,
                ),
                dbc.Col(
                    temporada_media_gols,
                    width=1,
                ),
            ],
        ),
        dbc.Row(html.Hr()),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    tabela_classificação,
                                ),
                            ]
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            grafico_classificação,
                        ),
                        dbc.Row(slicer_rodadas_selecionadas),
                    ],
                    width=8,
                ),
            ]
        ),
        dbc.Row(html.Hr()),
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        "Dados Históricos",
                    ),
                ),
                dbc.Col(check_filtro_jogadores, width=2),
                dbc.Col(slicer_temporadas, width=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(tabela_historica, width=6),
                dbc.Col(grafico_gols_pontos, width=6),
            ]
        ),
        dcc.Store(id="linhas_selecionadas"),
        dcc.Store(id="temporada_selecionada"),
    ],
    fluid=True,
)


@callback(Output("temporada_selecionada", "data"), Input("temporada_dpdn", "value"))
def filtrar_lista_jogos(temporada):
    df = lista_jogos_df
    df = df.loc[df["Ano"] == temporada]

    return df.to_dict("records")


@callback(
    Output("table1", "children"),
    Output("linhas_selecionadas", "data"),
    Output("temporada_partidas_jogadas", "children"),
    Output("temporada_gols", "children"),
    Output("temporada_media_gols", "children"),
    Input("min_pj", "value"),
    Input("temporada_selecionada", "data"),
)
def create_table1(pj_min, lista_jogos_filtrada):
    df = pd.DataFrame(lista_jogos_filtrada)

    num_jogos = df["Rodada"].max()

    num_gols = df["Gols"].sum()

    media_gols_partida = float("{:.1f}".format(num_gols / num_jogos))

    jogadores_df = df.groupby("Jogador")[["Pontos", "Gols", "Destaques"]].sum()

    jogadores_df["Presença"] = df.groupby("Jogador")["Rodada"].count().astype(int)

    jogadores_df["Presença%"] = jogadores_df["Presença"] / num_jogos

    jogadores_df["Gols/Jogo"] = jogadores_df["Gols"] / jogadores_df["Presença"]

    jogadores_df["Aproveitamento%"] = jogadores_df["Pontos"] / (
        jogadores_df["Presença"] * 3
    )

    jogadores_df["Vitórias"] = (
        df.loc[df["Pontos"] == 3].groupby("Jogador")["Pontos"].size().astype(int)
    )

    jogadores_df["Empates"] = (
        df.loc[df["Pontos"] == 1].groupby("Jogador")["Pontos"].size().astype(int)
    )

    jogadores_df["Derrotas"] = (
        df.loc[df["Pontos"] == 0].groupby("Jogador")["Pontos"].size().astype(int)
    )

    jogadores_df = jogadores_df.replace(np.nan, 0)

    jogadores_df = jogadores_df.reset_index()

    jogadores_df = jogadores_df.sort_values(by=["Pontos"], ascending=False)

    jogadores_df.insert(0, "#", range(1, len(jogadores_df) + 1, 1))

    jogadores_df = jogadores_df[
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
    jogadores_df = jogadores_df.rename(
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

    jogadores_df = jogadores_df.loc[jogadores_df["PJ"] >= pj_min]

    percentage = FormatTemplate.percentage(1)

    tabela = DataTable(
        id="datatable-interactivity",
        data=jogadores_df.to_dict("records"),
        columns=[
            dict(id="#", name="#"),
            dict(id="JOGADOR", name="JOGADOR"),
            dict(id="PTS", name="PTS"),
            dict(id="APRV", name="APRV", type="numeric", format=percentage),
            dict(id="GOLS", name="GOLS"),
            dict(id="MÉDIA", name="MÉDIA", type="numeric", format={"specifier": ".1f"}),
            dict(id="PJ", name="PJ"),
            dict(id="FREQ", name="FREQ", type="numeric", format=percentage),
            dict(id="S+", name="S+"),
            dict(id="V", name="V"),
            dict(id="E", name="E"),
            dict(id="D", name="D"),
        ],
        style_cell_conditional=[{"if": {"column_id": "JOGADOR"}, "textAlign": "left"}],
        sort_action="native",
        sort_mode="single",
        style_as_list_view=True,
        row_selectable="multi",
        derived_virtual_selected_rows=[],
        style_data={
            "whiteSpace": "normal",
            "height": "auto",
        },
    )

    return (
        tabela,
        jogadores_df.to_dict("records"),
        num_jogos,
        num_gols,
        media_gols_partida,
    )


@callback(Output("slicer-rodadas", "children"), Input("temporada_dpdn", "value"))
def slicer_rodadas(temporada):
    df = lista_jogos_df
    df = df.loc[df["Ano"] == temporada]

    slider = dcc.RangeSlider(
        id="rodadas_selecionadas",
        min=lista_jogos_df["Rodada"].unique().min(),
        max=lista_jogos_df["Rodada"].unique().max(),
        step=1,
        value=[
            lista_jogos_df["Rodada"].unique().min(),
            lista_jogos_df["Rodada"].unique().max(),
        ],
    )

    return slider


@callback(
    Output("graph1", "figure"),
    Input("datatable-interactivity", "derived_virtual_selected_rows"),
    Input("linhas_selecionadas", "data"),
    Input("temporada_partidas_jogadas", "children"),
    Input("temporada_selecionada", "data"),
    Input("rodadas_selecionadas", "value"),
)
def criar_graph1(selecionados, data, num_jogos, jogos_filtrados, rodadas):
    df = pd.DataFrame(jogos_filtrados)

    df = df[["Rodada", "Jogador", "Pontos", "Gols"]]

    if len(rodadas) == 1:
        rodadas_selecionadas = rodadas
    else:
        rodadas_selecionadas = range(rodadas[0], rodadas[1] + 1, 1)

    df = df.loc[df["Rodada"].isin(rodadas_selecionadas)]

    df = (
        df.groupby(["Rodada", "Jogador"])
        .sum()
        .unstack(fill_value=0)
        .stack()
        .reset_index()
    )

    df["Pontos Acc"] = df.groupby("Jogador")["Pontos"].cumsum()

    df["Gols Acc"] = df.groupby("Jogador")["Gols"].cumsum()

    df["Posição"] = (
        df.sort_values(["Pontos Acc", "Gols Acc"], ascending=False)
        .groupby("Rodada")
        .cumcount()
        .add(1)
    )

    dff = pd.DataFrame(data)

    jog_selecionados = [dff["JOGADOR"][x] for x in selecionados]

    jog_filtrados_df = dff["JOGADOR"].unique()

    if len(selecionados) == 0:
        df = df[df["Jogador"].isin(jog_filtrados_df)]
    else:
        df = df[df["Jogador"].isin(jog_selecionados)]

    line_classificação = px.line(
        df,
        x="Rodada",
        y="Posição",
        range_x=[1, num_jogos + 10],
        range_y=[20, 0],
        color="Jogador",
        template="none",
    )

    line_classificação.update_traces(line_width=5, opacity=0.6)
    line_classificação.update_layout(
        showlegend=False, template="none", yaxis={"title": ""}, xaxis={"title": ""}
    )

    for i, d in enumerate(line_classificação.data):
        line_classificação.add_scatter(
            x=[d.x[-1]],
            y=[d.y[-1]],
            mode="markers+text",
            text=str(d.y[-1]) + "-" + d.name,
            textfont=dict(color=d.line.color),
            textposition="middle right",
            marker=dict(color=d.line.color, size=12),
            legendgroup=d.name,
            showlegend=False,
        )

    return line_classificação


@callback(
    Output("graph2", "figure"),
    # Output("graph3", "children"),
    Input("my-range-slider", "value"),
    Input("ativar_filtro_jogadores", "value"),
    Input("linhas_selecionadas", "data"),
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
    # dff = dff.reset_index()

    # grafico_mediagols_mediapontos = px.scatter(
    #     data_frame=dff,
    #     x="Pontos/PJ",
    #     y="Gols/PJ",
    #     color=dff.index,
    #     size_max=50,
    #     # text=dff.index,
    # )

    # grafico_mediagols_mediapontos.update_layout(showlegend=False, template="none")
    # grafico_mediagols_mediapontos.update_traces(
    #     textposition="middle right", marker_color="rgba(0,0,0,0)"
    # )P

    # for i, row in dff.iterrows():
    #     jogador = i.replace(" ", "-")
    #     grafico_mediagols_mediapontos.add_layout_image(
    #         dict(
    #             source=Image.open(f"src/assets/fotos/{jogador}.png"),
    #             xref="x",
    #             yref="y",
    #             xanchor="center",
    #             yanchor="middle",
    #             x=row["Pontos/PJ"],
    #             y=row["Gols/PJ"],
    #             sizex=0.5,
    #             sizey=0.5,
    #             opacity=0.9,
    #             sizing="contain",
    #             layer="above",
    #         )
    #     )

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


@callback(
    Output("tabela_historica", "rowData"),
    Input("my-range-slider", "value"),
    Input("ativar_filtro_jogadores", "value"),
    Input("linhas_selecionadas", "data"),
)
def criar_tabela_historica(temporadas, ativar_filtro_jogadores, jogadores_tabela):
    if len(temporadas) == 1:
        temporadas_selecionadas = temporadas
    else:
        temporadas_selecionadas = range(temporadas[0], temporadas[1] + 1, 1)

    df = lista_jogos_df.loc[lista_jogos_df["Ano"].isin(temporadas_selecionadas)]

    jogadores_selecionados_df = pd.DataFrame(jogadores_tabela)

    if ativar_filtro_jogadores == "Sim":
        df = df.loc[df["Jogador"].isin(jogadores_selecionados_df["JOGADOR"])]
    else:
        pass

    num_jogos_hist = df.groupby("Ano")["Rodada"].max().sum()

    num_gols_hist = df["Gols"].sum()

    media_gols_partida_hist = float("{:.1f}".format(num_gols_hist))

    jogadores_df = df.groupby("Jogador")[["Pontos", "Gols", "Destaques"]].sum()

    jogadores_df["Presença"] = df.groupby("Jogador")["Rodada"].count().astype(int)

    jogadores_df["Presença%"] = jogadores_df["Presença"] / num_jogos_hist

    jogadores_df["Gols/Jogo"] = jogadores_df["Gols"] / jogadores_df["Presença"]

    jogadores_df["Aproveitamento%"] = jogadores_df["Pontos"] / (
        jogadores_df["Presença"] * 3
    )

    jogadores_df["Vitórias"] = (
        df.loc[df["Pontos"] == 3].groupby("Jogador")["Pontos"].size().astype(int)
    )

    jogadores_df["Empates"] = (
        df.loc[df["Pontos"] == 1].groupby("Jogador")["Pontos"].size().astype(int)
    )

    jogadores_df["Derrotas"] = (
        df.loc[df["Pontos"] == 0].groupby("Jogador")["Pontos"].size().astype(int)
    )

    jogadores_df = jogadores_df.replace(np.nan, 0)

    jogadores_df = jogadores_df.reset_index()

    jogadores_df = jogadores_df.sort_values(by=["Pontos"], ascending=False)

    jogadores_df.insert(0, "#", range(1, len(jogadores_df) + 1, 1))

    jogadores_df = jogadores_df[
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
    jogadores_df = jogadores_df.rename(
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

    row_data = jogadores_df.to_dict("records")

    return row_data


if __name__ == "__main__":
    app.run_server(debug=True)
