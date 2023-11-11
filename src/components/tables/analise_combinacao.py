from itertools import combinations

# Estatísticas dos jogadores combinados - Dupla
times_df = (
    lista_jogos_df.groupby(["Rodada", "Time"])["Jogador"].apply(list).reset_index()
)

times_df["Combinações"] = times_df["Jogador"].apply(lambda x: list(combinations(x, 2)))

times_df = times_df.explode("Combinações")


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
