import dash

dash.register_page(__name__, name="Gráfico de Classificação")

import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


grafico_classificação = html.Div(
    dcc.Graph(
        figure={},
        style={"height": "90vh"},
        id="gráfico_classificação",
    ),
)

slicer_rodadas_selecionadas = dcc.RangeSlider(
    id="rodadas_selecionadas",
    min=0,
    max=1,
    value=[0, 1],
    step=1,
)

layout = dbc.Container(
    [
        dbc.Row(dbc.Col(slicer_rodadas_selecionadas)),
        dbc.Row(dbc.Col(grafico_classificação, width=12)),
    ],
    fluid=True,
)


@callback(
    Output("rodadas_selecionadas", "min"),
    Output("rodadas_selecionadas", "max"),
    Output("rodadas_selecionadas", "value"),
    Input("df_filtrado_temporada_selecionada", "data"),
)
def slicer_rodadas(df_filtrado_temporada_selecionada):
    df = pd.DataFrame(df_filtrado_temporada_selecionada)
    min_value = df["Rodada"].unique().min()
    max_value = df["Rodada"].unique().max()
    value = [df["Rodada"].unique().min(), df["Rodada"].unique().max()]

    return min_value, max_value, value


@callback(
    Output("gráfico_classificação", "figure"),
    Input("linhas_selecionadas_temporada_classificação", "data"),
    Input("linhas_filtradas_tabela_classificação", "data"),
    Input("df_filtrado_temporada_selecionada", "data"),
    Input("rodadas_selecionadas", "value"),
)
def criar_gráfico_classificação(
    jogadores_selecionados, linhas_tabela, jogos_filtrados, rodadas
):
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

    dff = pd.DataFrame(linhas_tabela)
    jog_filtrados_df = dff["JOGADOR"].unique()
    if not jogadores_selecionados:
        df = df[df["Jogador"].isin(jog_filtrados_df)]
    else:
        jog_selecionados = [s["JOGADOR"] for s in jogadores_selecionados]
        df = df[df["Jogador"].isin(jog_selecionados)]

    line_classificação = px.line(
        df,
        x="Rodada",
        y="Pontos Acc",
        range_y=[0, 70],
        range_x=[0, df["Rodada"].max() + 5],
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
