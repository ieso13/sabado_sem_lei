import pandas as pd
import numpy as np


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
