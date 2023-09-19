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
