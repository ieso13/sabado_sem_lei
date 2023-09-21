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
