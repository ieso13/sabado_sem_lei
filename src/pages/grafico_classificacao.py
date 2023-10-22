import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import dash


dash.register_page(__name__, name="Gráfico de Classificação", order=3)

grafico_classificação = html.Div(
    dcc.Graph(
        figure={},
        style={"height": "85vh"},
        id="gráfico_classificação",
    ),
)

slicer_rodadas_selecionadas = dcc.RangeSlider(
    id="rodadas_selecionadas", min=0, max=1, value=[0, 1], step=1, marks=None
)

dropdown_tipo_gráfico = html.Div(
    [
        dcc.Dropdown(
            options=["Rodadas x Pontuação", "Rodadas x Posição"],
            value="Rodadas x Pontuação",
            id="tipo_gráfico",
            persistence=True,
            persistence_type="memory",
        ),
    ]
)

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [html.H3("Classificação ao Longo do Tempo")],
                    width={"size": "auto"},
                ),
                dbc.Col(
                    [dropdown_tipo_gráfico],
                    width=2,
                ),
            ],
            class_name="d-flex align-items-center g*-1",
        ),
        dbc.Row(grafico_classificação),
        dbc.Row(slicer_rodadas_selecionadas),
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
    value = [0, 1]

    return min_value, max_value, value


@callback(
    Output("gráfico_classificação", "figure"),
    Input("linhas_selecionadas_temporada_classificação", "data"),
    Input("linhas_filtradas_tabela_classificação", "data"),
    Input("df_filtrado_temporada_selecionada", "data"),
    Input("rodadas_selecionadas", "value"),
    Input("tipo_gráfico", "value"),
)
def criar_gráfico_classificação(
    jogadores_selecionados, linhas_tabela, jogos_filtrados, rodadas, tipo_gráfico
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

    if "Pontuação" in tipo_gráfico:
        df = df.sort_values(by=["Rodada", "Pontos Acc"], ascending=False)
        line_classificação = px.line(
            df,
            x="Rodada",
            y="Pontos Acc",
            range_y=[0, 66],
            range_x=[1, 50],
            color="Jogador",
            template="none",
        )
        line_classificação.update_traces(line_width=5, opacity=0.3)
        for i, d in enumerate(line_classificação.data):
            line_classificação.add_scatter(
                x=[d.x[0]],
                y=[d.y[0]],
                mode="markers+text",
                text=str(d.y[0]),
                textfont=dict(color=d.line.color, size=11),
                textposition="middle right",
                marker=dict(color=d.line.color, size=8),
                legendgroup=d.name,
                showlegend=False,
            )

    else:
        df = df.sort_values(by=["Rodada", "Posição"], ascending=[False, True])
        line_classificação = px.line(
            df,
            x="Rodada",
            y="Posição",
            range_y=[20, 0],
            range_x=[0, 47],
            color="Jogador",
            template="none",
        )
        line_classificação.update_traces(line_width=5, opacity=0.3)
        for i, d in enumerate(line_classificação.data):
            line_classificação.add_scatter(
                x=[d.x[0]],
                y=[d.y[0]],
                mode="markers+text",
                text=str(d.y[0]),
                textfont=dict(color=d.line.color, size=11),
                textposition="middle right",
                marker=dict(color=d.line.color, size=8),
                legendgroup=d.name,
                showlegend=False,
            )

    line_classificação.update_layout(
        template="none", yaxis={"title": ""}, xaxis={"title": ""}
    )

    return line_classificação
