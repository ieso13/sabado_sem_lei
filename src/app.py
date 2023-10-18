from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

import dash


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    suppress_callback_exceptions=True,
    use_pages=True,
)

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
                                    dbc.NavLink(
                                        page["name"], href=page["path"], active="exact"
                                    )
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
    ),
    color="primary",
    dark=True,
)

app.layout = dbc.Container(
    [
        navbar,
        dash.page_container,
        dcc.Store(id="linhas_filtradas_tabela_classificação"),
        dcc.Store(id="df_filtrado_temporada_selecionada"),
        dcc.Store(id="linhas_selecionadas_temporada_classificação"),
    ],
    fluid=True,
    class_name="gx-0",
)


if __name__ == "__main__":
    app.run_server(debug=True)
