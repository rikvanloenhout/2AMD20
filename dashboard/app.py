from ke_app.main import app
from ke_app.views.menu import make_menu_layout
from ke_app.views.world_cl import CloroMap
from ke_app.views.frequencyplot import FrequencyPlot
from ke_app.data import get_crime_data, get_life_data, get_happiness_data, get_poverty_data, get_merged

from dash import html, dcc, dash_table
import plotly.express as px
from dash.dependencies import Input, Output


from ke_app.data import get_crime_data, get_life_data, get_happiness_data, get_poverty_data, get_merged
import pandas as pd
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

df_combined = pd.read_csv("../datasets/all_data.csv")
df = get_merged(df_combined, 100, 100, 100, 100)
df_continent = pd.read_csv("../datasets/continents2.csv")
df_continent = df_continent[['alpha-3', 'sub-region', 'region']].rename(columns={'alpha-3': 'ISO'})
df_continent['global'] = "World"

df_merged = df.merge(df_continent, how='left', on='ISO')

dct1 = dict(df_merged['sub-region'].value_counts())
dct2 = dict(df_merged['region'].value_counts())
dct3 = dict(df_merged['global'].value_counts())
dct4 = dict(df_merged['Country'].value_counts())

dct1.update(dct2)
dct1.update(dct3)
dct1.update(dct4)

kg_df = pd.DataFrame(columns=["source", "target", "edge"])[["source", "target", "edge"]]
for idx, val in df_merged.iterrows():
    entry = pd.DataFrame(
        {"source": "World",
         "target": val['region'],
         "edge": "part of"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

for idx, val in df_merged.iterrows():
    entry = pd.DataFrame(
        {"source": val['region'],
         "target": val['sub-region'],
         "edge": "part of"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

for idx, val in df_merged.iterrows():
    entry = pd.DataFrame(
        {"source": val['sub-region'],
         "target": val['Country'],
         "edge": "contains"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

for idx, val in df_merged.iterrows():
    entry = pd.DataFrame(
        {"source": val['Country'],
         "target": str(round(val['Mean Crime Index'], 3)),
         "edge": "Crime"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

for idx, val in df_merged.iterrows():
    entry = pd.DataFrame(
        {"source": val['Country'],
         "target": str(round(val['Happiness Score'], 3)),
         "edge": "Happiness"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

for idx, val in df_merged.iterrows():
    entry = pd.DataFrame(
        {"source": val['Country'],
         "target": str(round(val['Life expectancy'], 3)),
         "edge": "Life"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

for idx, val in df_merged.iterrows():
    entry = pd.DataFrame(
        {"source": val['Country'],
         "target": str(round(val['MeanGini'], 3)),
         "edge": "Poverty"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

kg_df.drop_duplicates(inplace=True)

G = nx.from_pandas_edgelist(kg_df, "source", "target",
                            edge_attr=True, create_using=nx.DiGraph())

ll = ['Crime', 'Life', 'Happiness', 'Poverty']

nt = Network('1920px', '1080px', directed=True, notebook=False, select_menu=False,
             filter_menu=False, )

for node in G:
    if node == "World":
        color = "yellow"
        size = 20
    elif node in df_merged['region'].unique():
        color = "orange"
        size = 15
    elif node in df_merged['sub-region'].unique():
        color = "red"
        size = 10

    elif node in df_merged['Country'].unique():
        color = "darkred"
        size = 10
    else:
        color = "black"
        size = 10
    nt.add_node(node, label=node, color=color, size=size)

for edge in G.edges:
    #     print(edge)
    label = kg_df[(kg_df['source'] == edge[0]) & (kg_df['target'] == edge[1])]['edge'][0]
    if label == "Life":
        color = 'green'
    elif label == "Happiness":
        color = 'violet'
    elif label == "Crime":
        color = 'blue'
    elif label == "Poverty":
        color = 'indigo'
    else:
        color = 'gray'
    nt.add_edge(edge[0], edge[1], color=color, width=1,  label=label)

# nt.show_buttons(filter_=['nodes'])

nt.show('kg.html')



if __name__ == '__main__':
    # Create data
    df_crime = get_crime_data()
    df_life = get_life_data()
    df_happ = get_happiness_data()
    df_pov = get_poverty_data()

    # Instantiate custom views
    cloroMap1 = CloroMap("cloromap1")
    frequencyPlot1 = FrequencyPlot("frequencyplot1")

    ALLOWED_TYPES = (
        "text", "number", "password", "email", "search",
        "tel", "url", "range", "hidden",
    )

    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    cloroMap1,
                    frequencyPlot1,
                    html.Div(
                        className="graph_card",
                        children=[
                            html.H6("Knowledge graph equal importance"),
                            html.Iframe(srcDoc=nt.html,
                                        style={"height": "1067px", "width": "100%"}),
                        ]),
                ],
            ),
            # dash_table.DataTable(df_merged[['Country', 'Rank']].head(5).to_dict('records'))
        ],
    )

    # Define interactions
    @app.callback(
        [Output(cloroMap1.html_id, "figure"),
         Output(f"CloroMap_{cloroMap1.html_id}", "children"),
         Output(frequencyPlot1.html_id, "figure"),
         Output(f"FrequencyPlot_{frequencyPlot1.html_id}", "children")],
        [Input("select-data-cloro-1", "value"),
         Input("input1", "value"),
         Input("input2", "value"),
         Input("input3", "value"),
         Input("input4", "value")])

    def update_cloromap_1(selected_data, *vals):
        if selected_data == "Crime":
            return cloroMap1.update(df_crime, 'Mean Crime Index', on_hover=['Min Crime Index', 'Max Crime Index']), \
                "Mean Crime Index, 2022", \
                frequencyPlot1.update(df_crime, "Mean Crime Index", "freq"), \
                "Distribution Mean Crime Index, 2022"
        elif selected_data == "Life":
            return cloroMap1.update(df_life, "Life expectancy ", animation_frame=['Year']), \
                "Life Expectancy, 2000-2015", \
                frequencyPlot1.update(df_life, "Life expectancy ", "freq"), \
                "Distribution Life Expectancy, 2015"
        elif selected_data == "Happiness":
            return cloroMap1.update(df_happ, "Happiness Score", on_hover=["Happiness Rank"], animation_frame=['Year']), \
                "Happiness Score, 2015-2019", \
                frequencyPlot1.update(df_happ, "Happiness Score", "freq"), \
                "Distribution Happiness Score, 2015"
        elif selected_data == "Poverty":
            return cloroMap1.update(df_pov, "Gini"), \
                "Gini Index, 2019", \
                frequencyPlot1.update(df_pov, "Gini", "freq"), \
                "Distribution Gini Index, 2019"
        elif selected_data == "Custom Scores":
            if all(map(lambda x: x is not None, vals)):
                # print(vals)
                df_merged = get_merged(df_combined, vals[0], vals[1], vals[2], vals[3])
                df_merged['outlier'] = df_combined['outliers']
            else:
                df_merged = get_merged(df_combined, 0.25, 0.25, 0.25, 0.25)
                df_merged['outlier'] = df_combined['outliers']
            return cloroMap1.update(df_merged, "Aggregate Scores", on_hover=["Rank", 'outlier']), \
                "Aggregate Scores", \
                frequencyPlot1.update(df_merged, "Aggregate Scores", "bar"), \
                "Aggregate Scores"



    app.run_server(debug=True, dev_tools_ui=True)
