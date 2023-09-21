import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
from dash.dash_table import DataTable, FormatTemplate
import dash_bootstrap_components as dbc
from dfs.lista_jogos import lista_jogos_df

# COMPONENTS OF THE LAYOUT

filtro_temporada = (
    dbc.Card(
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
    ),
)

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
        id="frequencia_minima",
        class_name="mx-1 my-1",
    ),
)

temporada_partidas_jogadas = (
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H6("Partidas Jogadas"),
                    html.H4(children=[], id="temporada_partidas_jogadas"),
                ],
            ),
        ],
        class_name="text-center mx-1 my-1",
    ),
)

temporada_gols = (
    dbc.Card(
        dbc.CardBody(
            [
                html.H6("Gols"),
                html.H4(children=[], id="temporada_gols"),
            ],
        ),
        class_name="text-center mx-1 my-1",
    ),
)

temporada_media_gols = (
    dbc.Card(
        dbc.CardBody(
            [
                html.H6("Gols/Partida"),
                html.H4(children=[], id="temporada_media_gols"),
            ],
        ),
        class_name="text-center mx-1 my-1",
    ),
)
grafico_classificação = (
    html.Div(
        id="graph1",
        children=[],
    ),
)

tabela_classificação = (
    html.Div(
        id="table1",
        children=[],
        style={"max-height": "70vh", "overflow": "auto"},
    ),
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
                        dbc.CardImg(src="./assets/Escudo.jpg"),
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
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    tabela_classificação,
                                    width=12,
                                ),
                            ]
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    grafico_classificação,
                    width=8,
                ),
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

    media_gols_partida = num_gols // num_jogos

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


@callback(
    Output("graph1", "children"),
    Input("datatable-interactivity", "derived_virtual_selected_rows"),
    Input("linhas_selecionadas", "data"),
    Input("temporada_partidas_jogadas", "children"),
    Input("temporada_selecionada", "data"),
)
def criar_graph1(selecionados, data, num_jogos, jogos_filtrados):
    df = pd.DataFrame(jogos_filtrados)

    lista_jogos_completa_df = df[["Rodada", "Jogador", "Pontos", "Gols"]]

    lista_jogos_completa_df = (
        lista_jogos_completa_df.groupby(["Rodada", "Jogador"])
        .sum()
        .unstack(fill_value=0)
        .stack()
        .reset_index()
    )

    lista_jogos_completa_df["Pontos Acc"] = lista_jogos_completa_df.groupby("Jogador")[
        "Pontos"
    ].cumsum()

    lista_jogos_completa_df["Gols Acc"] = lista_jogos_completa_df.groupby("Jogador")[
        "Gols"
    ].cumsum()

    lista_jogos_completa_df["Posição"] = (
        lista_jogos_completa_df.sort_values(["Pontos Acc", "Gols Acc"], ascending=False)
        .groupby("Rodada")
        .cumcount()
        .add(1)
    )

    df = pd.DataFrame(data)

    jog_selecionados = [df["JOGADOR"][x] for x in selecionados]

    if len(selecionados) == 0:
        pass
    else:
        lista_jogos_completa_df = lista_jogos_completa_df[
            lista_jogos_completa_df["Jogador"].isin(jog_selecionados)
        ]

    line_classificação = px.line(
        lista_jogos_completa_df,
        x="Rodada",
        y="Posição",
        range_x=[1, num_jogos + 10],
        range_y=[20, 0],
        color="Jogador",
        title="Corrida do Título",
        template="none",
    )

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
    return dcc.Graph(figure=line_classificação, style={"height": "85vh"})


if __name__ == "__main__":
    app.run_server(debug=True)
