from app import lista_jogos_df as df


# Estatísticas dos escaladores
escaladores_df = df.loc[df["Escalador"] == df["Jogador"]]

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
