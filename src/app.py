import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
from dash.dash_table import DataTable, FormatTemplate
import dash_bootstrap_components as dbc
from itertools import combinations
from dfs import tabela_escaladores

lista_jogos_df = pd.read_csv(
    "./assets/SSL_Jogos.csv", encoding="UTF-8", sep="\;", engine="python"
)

# Consolidar votos destaques
lista_jogos_df["Destaques"] = (lista_jogos_df["Destaques"] >= 3).astype(int)


# Estatísticas dos jogadores combinados - Dupla
times_df = (
    lista_jogos_df.groupby(["Rodada", "Time"])["Jogador"].apply(list).reset_index()
)

times_df["Combinações"] = times_df["Jogador"].apply(lambda x: list(combinations(x, 2)))

times_df = times_df.explode("Combinações")

# Dados únicos dos Jogos
num_jogos = lista_jogos_df["Rodada"].max()
num_gols = lista_jogos_df["Gols"].sum()


# Classificação ao longo do tempo
lista_jogos_completa_df = lista_jogos_df[["Rodada", "Jogador", "Pontos", "Gols"]]

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

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
)

# components

escudo = dbc.Card(
    dbc.CardImg(src="./assets/Escudo.jpg"),
    class_name="center mx-2 my-1 align-middle",
)

card_pj = (
    dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H6("Partidas Jogadas"),
                    html.H4(num_jogos),
                ],
            ),
        ],
        class_name="text-center mx-2 my-1",
    ),
)

card_ngols = (
    dbc.Card(
        dbc.CardBody(
            [
                html.H6("Número de Gols"),
                html.H4(num_gols),
            ],
        ),
        class_name="text-center mx-2 my-1",
    ),
)

card_mediagols = (
    dbc.Card(
        dbc.CardBody(
            [
                html.H6("Média de Gols/Partida"),
                html.H4(num_gols // num_jogos),
            ],
        ),
        class_name="text-center mx-2 my-1",
    ),
)

card_temporada = (
    dbc.Card(
        dbc.CardBody(
            [
                html.H6("Temporada"),
                dcc.Dropdown(
                    [
                        2011,
                        2012,
                        2013,
                        2014,
                        2015,
                        2016,
                        2017,
                        2018,
                        2019,
                        2020,
                        2021,
                        2022,
                        2023,
                    ],
                    2023,
                ),
            ],
        ),
        class_name="text-center mx-2 my-1",
    ),
)

card_titulo = dbc.Card(
    dbc.CardBody(html.H1("Sábado sem Lei")),
    class_name="text-center mx-2 my-1 align-middle",
)

card_pjmin = (
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
        class_name="mx-2 my-1",
    ),
)

card_selec_jog = (
    dbc.Card(
        dbc.CardBody(
            [
                html.H6("Escolha o Jogador Para Análisar"),
                dcc.Dropdown(
                    lista_jogos_df["Jogador"].unique(),
                    id="filtro_jogador",
                ),
            ],
        ),
        class_name="mx-2",
    ),
)

tabela_classificação = (
    html.Div(
        id="table1",
        children=[],
        style={"max-height": "70vh", "overflow": "auto"},
    ),
)

grafico_classificação = (
    html.Div(
        id="graph1",
        children=[],
    ),
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    escudo,
                    width=1,
                ),
                dbc.Col(
                    card_titulo,
                    width=3,
                ),
                dbc.Col(
                    card_temporada,
                    width=2,
                ),
                dbc.Col(
                    card_pj,
                    width=2,
                ),
                dbc.Col(
                    card_ngols,
                    width=2,
                ),
                dbc.Col(
                    card_mediagols,
                    width=2,
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
                                    card_pjmin,
                                    width=6,
                                ),
                                dbc.Col(
                                    card_selec_jog,
                                    width=6,
                                ),
                            ]
                        ),
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
        dcc.Store(id="memory-output"),
    ],
    fluid=True,
)


@callback(
    Output("table1", "children"),
    Output("memory-output", "data"),
    Input("filtro_jogador", "value"),
    Input("min_pj", "value"),
)
def create_table1(jogador, pj_min):
    t_df = times_df.copy()

    if jogador:
        t_df["Combinações"] = t_df["Combinações"].apply(lambda x: jogador in x)
    else:
        t_df["Combinações"] = t_df["Combinações"].apply(lambda x: True)

    t_df["Rodada-Time"] = t_df.Rodada.astype(str) + "-" + t_df.Time.astype(str)

    t_df = t_df[["Rodada-Time", "Combinações"]]

    t_df = t_df.loc[t_df["Combinações"] == True].drop_duplicates()

    lista_jogos_df["Rodada-Time"] = (
        lista_jogos_df.Rodada.astype(str) + "-" + lista_jogos_df.Time.astype(str)
    )

    lista_jogos_filtrada_df = lista_jogos_df.loc[
        lista_jogos_df["Rodada-Time"].isin(t_df["Rodada-Time"])
    ]
    jogadores_df = lista_jogos_filtrada_df.groupby("Jogador")[
        ["Pontos", "Gols", "Destaques"]
    ].sum()
    jogadores_df["Presença"] = (
        lista_jogos_filtrada_df.groupby("Jogador")["Rodada"].count().astype(int)
    )
    jogadores_df["Presença%"] = jogadores_df["Presença"] / num_jogos
    jogadores_df["Gols/Jogo"] = jogadores_df["Gols"] / jogadores_df["Presença"]
    jogadores_df["Aproveitamento%"] = jogadores_df["Pontos"] / (
        jogadores_df["Presença"] * 3
    )

    jogadores_df["Vitórias"] = (
        lista_jogos_filtrada_df.loc[lista_jogos_filtrada_df["Pontos"] == 3]
        .groupby("Jogador")["Pontos"]
        .size()
        .astype(int)
    )
    jogadores_df["Empates"] = (
        lista_jogos_filtrada_df.loc[lista_jogos_filtrada_df["Pontos"] == 1]
        .groupby("Jogador")["Pontos"]
        .size()
        .astype(int)
    )
    jogadores_df["Derrotas"] = (
        lista_jogos_filtrada_df.loc[lista_jogos_filtrada_df["Pontos"] == 0]
        .groupby("Jogador")["Pontos"]
        .size()
        .astype(int)
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

    return DataTable(
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
    ), jogadores_df.to_dict("records")


@callback(
    Output("graph1", "children"),
    Input("datatable-interactivity", "derived_virtual_selected_rows"),
    Input("memory-output", "data"),
)
def criar_graph1(selecionados, data):
    df = lista_jogos_completa_df

    dff = pd.DataFrame(data)

    jog_selecionados = [dff["JOGADOR"][x] for x in selecionados]

    if len(selecionados) == 0:
        pass
    else:
        df = df[df["Jogador"].isin(jog_selecionados)]

    line_classificação = px.line(
        df,
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
