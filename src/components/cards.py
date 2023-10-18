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
        class_name="mx-1 my-1",
    ),
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
