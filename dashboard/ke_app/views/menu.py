from dash import dcc, html
from ..config import data_list
from dash.dependencies import Input, Output


def generate_description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Quality of Life Dataset"),
            html.Div(
                id="intro",
                children="This is a dashboard to inform and recommended users about the quality of life of countries all over the world",
            ),
        ],
    )


def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.Label("Dataset choropleth"),
            dcc.Dropdown(
                id="select-data-cloro-1",
                options=[{"label": i, "value": i} for i in data_list],
                value=data_list[0],
            ),
        ], style={"textAlign": "float-left"}
    )

def generate_description_card2():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card2",
        children=[
            html.H6("Weights Initialization (0-100)")
        ],
        style={"textAlign": "float-left"}
    )



def generate_numeric_input1():
    return html.Div(children=
                    [dcc.Input(
                        id="input1",
                        type="number",
                        min=0,
                        max=100,
                        placeholder="Weight of Crime",
                    ),
                    dcc.Input(
                        id="input2",
                        type="number",
                        min=0,
                        max=100,
                        placeholder="Weight of Life",
                    ),
                    dcc.Input(
                        id="input3",
                        type="number",
                        min=0,
                        max=100,
                        placeholder="Weight of Happiness",
                    ),
                    dcc.Input(
                        id="input4",
                        type="number",
                        min=0,
                        max=100,
                        placeholder="Weight of Poverty",
                    )]
                    + [html.Div(id="out-all-inputs")]
    )

def make_menu_layout():
    return [generate_description_card(), generate_control_card(),generate_description_card2(), generate_numeric_input1()]
