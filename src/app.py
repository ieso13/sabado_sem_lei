from dash import Dash, dcc, html, callback, Input, Output, State
import dash_bootstrap_components as dbc
import dash
from dfs.lista_jogos import lista_jogos_df
import pandas as pd
from tools.criar_df_classificação import criar_df_classificação

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    use_pages=True,
)

app.config.suppress_callback_exceptions = True

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    [
                        html.Img(
                            src=app.get_asset_url("SSL.png"),
                            height="40px",
                            className="ms-2",
                        ),
                        dbc.NavbarBrand("Sábado Sem Lei", className="ms-2"),
                    ],
                    width={"size": "auto"},
                    class_name="d-flex align-items-center",
                ),
                align="center",
                class_name="g-0",
            ),
            dbc.Row(
                dbc.Col(
                    [
                        dbc.Nav(
                            [
                                dbc.NavItem(
                                    dbc.NavLink(page["name"], href=page["path"])
                                )
                                for page in dash.page_registry.values()
                            ],
                            className="w-100",
                            navbar=True,
                        )
                    ],
                    width={"size": "auto"},
                    class_name="d-flex align-items-center",
                ),
                align="center",
                # className="flex-grow-1",
            ),
        ],
        fluid=True,
        class_name="g-0",
    ),
    color="primary",
    dark=True,
    className="py-1",
)


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 48,
    "left": 0,
    "bottom": 0,
    "padding": "2rem 1rem",
    "background-color": "Gainsboro",
}

sidebar = html.Div(
    [
        html.H2("Filtros", className="display-5"),
        html.Hr(),
        html.H6("Temporada"),
        dcc.Dropdown(
            [{"label": c, "value": c} for c in lista_jogos_df["Ano"].unique()],
            value=lista_jogos_df["Ano"].unique().max(),
            id="temporada_dpdn",
            persistence=True,
            persistence_type="memory",
        ),
        html.Hr(),
        html.H6("Presença Mínima"),
        dcc.Input(
            id="min_pj",
            type="number",
            placeholder="Número Mínimo de Rodadas",
            value=0,
            persistence=True,
            persistence_type="memory",
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = dbc.Container(
    [
        navbar,
        dbc.Row([dbc.Col(sidebar, width=2), dbc.Col(dash.page_container, width=10)]),
        dcc.Store(id="linhas_filtradas_tabela_classificação", storage_type="session"),
        dcc.Store(id="df_filtrado_temporada_selecionada", storage_type="session"),
        dcc.Store(
            id="linhas_selecionadas_temporada_classificação", storage_type="session"
        ),
        dcc.Store(id="frequencia_minima", storage_type="session"),
        dcc.Store(id="filtro_tabela_classificação", storage_type="session"),
    ],
    fluid=True,
    class_name="gx-0",
)


@callback(
    Output("df_filtrado_temporada_selecionada", "data"),
    Input("temporada_dpdn", "value"),
)
def filtrar_lista_jogos(temporada):
    df = lista_jogos_df
    df = df.loc[df["Ano"] == temporada]
    return df.to_dict("records")


@callback(
    Output("frequencia_minima", "data"),
    Input("min_pj", "value"),
)
def filtro_frequencia(frequencia_minima):
    return frequencia_minima


@callback(
    [
        Output("filtro_tabela_classificação", "data"),
        Output("linhas_filtradas_tabela_classificação", "data"),
        Input("frequencia_minima", "data"),
        Input("df_filtrado_temporada_selecionada", "data"),
    ],
)
def filtrar_dados_tabela_classificação(pj_min, linhas_temporada_selecionada):
    df = pd.DataFrame(linhas_temporada_selecionada)
    tabela_df = criar_df_classificação(df)
    tabela_df = tabela_df.loc[tabela_df["PJ"] >= pj_min]
    rowData = tabela_df.to_dict("records")

    return (rowData, rowData)


@callback(
    Output("tabela_classificação", "rowData"),
    Input("filtro_tabela_classificação", "data"),
)
def filtro_frequencia(data):
    return data


@callback(
    Output("linhas_selecionadas_temporada_classificação", "data"),
    Input("tabela_classificação", "selectedRows"),
)
def selecionar_linhas_tabela(selectedRows):
    return selectedRows


if __name__ == "__main__":
    app.run_server(debug=False)
