import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

lista_jogos_df = pd.read_csv(
    "./SSL_Jogos.csv", encoding="UTF-8", sep="\;", engine="python"
)

# Consolidar votos destaques
lista_jogos_df["Destaques"] = (lista_jogos_df["Destaques"] >= 3).astype(int)

# Dados únicos dos Jogos
num_jogos = lista_jogos_df["Rodada"].max()

# Dados individuais dos jogadores
jogadores_df = lista_jogos_df.groupby("Jogador")[["Pontos", "Gols", "Destaques"]].sum()

jogadores_df["Presença"] = (
    lista_jogos_df.groupby("Jogador")["Rodada"].count().astype(int)
)
jogadores_df["Presença%"] = ((jogadores_df["Presença"] / num_jogos) * 100).map(
    "{:,.1f}%".format
)
jogadores_df["Gols/Jogo"] = (jogadores_df["Gols"] / jogadores_df["Presença"]).map(
    "{:,.1f}".format
)
jogadores_df["Aproveitamento%"] = (
    jogadores_df["Pontos"] / (jogadores_df["Presença"] * 3) * 100
).map("{:,.1f}%".format)
jogadores_df["Vitórias"] = (
    lista_jogos_df.loc[lista_jogos_df["Pontos"] == 3]
    .groupby("Jogador")["Pontos"]
    .size()
    .astype(int)
)
jogadores_df["Empates"] = (
    lista_jogos_df.loc[lista_jogos_df["Pontos"] == 1]
    .groupby("Jogador")["Pontos"]
    .size()
    .astype(int)
)


jogadores_df["Derrotas"] = (
    lista_jogos_df.loc[lista_jogos_df["Pontos"] == 0]
    .groupby("Jogador")["Pontos"]
    .size()
    .astype(int)
)

jogadores_df = jogadores_df.replace(np.nan, 0)

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

tabela_escaladores["Aproveitamento%"] = (
    tabela_escaladores["Pontos"] / (tabela_escaladores["Presença"] * 3) * 100
).map("{:,.1f}%".format)

tabela_escaladores = tabela_escaladores.reset_index().sort_values(
    by=["Presença"], ascending=False
)

tabela_escaladores = tabela_escaladores.rename(
    columns={
        "Jogador": "JOGADOR",
        "Pontos": "PTS",
        "Aproveitamento%": "APRV",
        "Gols": "GOLS",
        "Presença": "PJ",
        "Destaques": "S+",
    }
)

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

# Tabela de classificação final
tabela = jogadores_df.copy().reset_index()
tabela = tabela.sort_values(by=["Pontos"], ascending=False)
tabela = tabela[
    [
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
tabela = tabela.rename(
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


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H1(
                        "Sábado Sem Lei - 2022",
                        style={"textAlign": "center"},
                    ),
                    width=3,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.P("Presença Mínima"),
                            dbc.Input(
                                id="filtro_presença",
                                type="number",
                                min=1,
                                max=num_jogos,
                                step=1,
                                value=num_jogos // 2,
                            ),
                        ]
                    ),
                    width=1,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        id="table1",
                        children=[],
                        style={"max-height": "90vh", "overflow": "auto"},
                    ),
                    width=4,
                ),
                dbc.Col(
                    html.Div(id="graph1", children=[]),
                    width=8,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        id="table2",
                        children=[
                            dbc.Table.from_dataframe(
                                tabela_escaladores,
                                size="sm",
                                hover=True,
                                style={"width": "100%"},
                            )
                        ],
                        style={"max-height": "100vh", "overflow": "auto"},
                    ),
                    width=4,
                ),
                dbc.Col(
                    html.Div(id="graph2", children=[]),
                    width=4,
                ),
                dbc.Col(
                    html.Div(id="graph3", children=[]),
                    width=4,
                ),
            ]
        ),
        dcc.Store(id="store-data", data=[], storage_type="memory"),
    ],
    fluid=True,
)


@callback(Output("store-data", "data"), Input("filtro_presença", "value"))
def store_data(value):
    linha_de_corte = jogadores_df.loc[jogadores_df["Presença"] >= value].index
    lista_filtrada = lista_jogos_completa_df[
        lista_jogos_completa_df["Jogador"].isin(linha_de_corte)
    ].reset_index()
    data = lista_filtrada.to_dict("records")
    return data


@callback(Output("graph1", "children"), Input("store-data", "data"))
def create_graph1(data):
    dff = pd.DataFrame(data)
    line_classificação = px.line(
        dff,
        x="Rodada",
        y="Posição",
        range_x=[1, num_jogos + 10],
        color="Jogador",
        template="none",
    )

    line_classificação.update_yaxes(autorange="reversed")
    line_classificação.update_layout(
        showlegend=False, template="none", yaxis={"title": ""}
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

    return dcc.Graph(figure=line_classificação, style={"height": "100vh"})


@callback(Output("table1", "children"), Input("filtro_presença", "value"))
def create_table1(value):
    dff = tabela.loc[tabela["PJ"] >= value]
    return dbc.Table.from_dataframe(
        dff,
        size="sm",
        hover=True,
        style={
            "width": "100%",
        },
    )


@callback(Output("graph2", "children"), Input("store-data", "data"))
def create_graph2(data):
    dff = pd.DataFrame(data)
    bar_pontos = px.bar(
        dff,
        x="Pontos Acc",
        y="Jogador",
        color="Jogador",
        animation_frame="Rodada",
        orientation="h",
        text="Posição",
        template="none",
        title="Classificação",
    )
    bar_pontos.update_layout(
        showlegend=False,
        yaxis={
            "categoryorder": "total ascending",
            "title": "",
            "side": "right",
            "automargin": "width",
        },
        xaxis={"title": ""},
    )
    bar_pontos.update_yaxes(ticklabelposition="inside")
    bar_pontos.add_vline(x=0)

    return dcc.Graph(figure=bar_pontos, style={"height": "100vh"})


@callback(Output("graph3", "children"), Input("store-data", "data"))
def create_graph3(data):
    dff = pd.DataFrame(data)
    bar_gols = px.bar(
        dff,
        x="Gols Acc",
        y="Jogador",
        color="Jogador",
        animation_frame="Rodada",
        orientation="h",
        text="Gols Acc",
        template="none",
        title="Gols Acumudalos",
    )
    bar_gols.update_layout(
        showlegend=False,
        yaxis={"categoryorder": "total ascending", "side": "right", "title": ""},
        xaxis={"title": ""},
    )

    bar_gols.update_yaxes(ticklabelposition="inside")
    bar_gols.add_vline(x=0)

    return dcc.Graph(figure=bar_gols, style={"height": "100vh"})


if __name__ == "__main__":
    app.run_server(debug=True)
