from ke_app.data import get_crime_data, get_life_data, get_happiness_data, get_poverty_data, get_merged
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


df_merged = get_merged(0.25, 0.25, 0.25, 0.25)
df_merged.to_csv("merged_final.csv")

df_continent = pd.read_csv("continents2.csv")
df_continent = df_continent[['alpha-3', 'sub-region', 'region']].rename(columns={'alpha-3': 'ISO'})
df_continent['global'] = "World"

df_merged = df_merged.merge(df_continent, how='left', on='ISO')

dct1 = dict(df_merged['sub-region'].value_counts())
dct2 = dict(df_merged['region'].value_counts())
dct3 = dict(df_merged['global'].value_counts())
dct4 = dict(df_merged['Country'].value_counts())

dct1.update(dct2)
dct1.update(dct3)
dct1.update(dct4)

kg_df = pd.DataFrame(columns={"source", "target", "edge"})[["source", "target", "edge"]]
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
         "target": str(val['Rank']),
         "edge": "QoL Rank"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

kg_df.drop_duplicates(inplace=True)

rem = ['index', 'Country', 'Rank', 'ISO']
crime = list(get_crime_data().columns)
for item in rem:
    crime.remove(item)

rem = ['Country', 'Year', 'ISO']
life = list(get_life_data().columns)
for item in rem:
    life.remove(item)

rem = ['Country Name', 'Country Code', 'Country', 'ISO']
pov = list(get_poverty_data().columns)
for item in rem:
    pov.remove(item)

rem = ['Health (Life Expectancy)', 'Country', 'Region', 'Happiness Rank', 'Happiness Score', 'Standard Error', 'Year', 'Lower Confidence Interval', 'Upper Confidence Interval', 'ISO']
hap = list(get_happiness_data().columns)
for item in rem:
#     print(item)
    hap.remove(item)
hap.append('Life expectancy ')

# kg_df = pd.DataFrame(columns={"source", "target", "edge"})[["source", "target", "edge"]]
entry = pd.DataFrame(
    {"source": "Quality of Life",
     "target": "Crime",
     "edge": "weight w1"}, index=[0])
kg_df = pd.concat([kg_df, entry])

entry = pd.DataFrame(
    {"source": "Quality of Life",
     "target": "Life",
     "edge": "weight w2"}, index=[0])
kg_df = pd.concat([kg_df, entry])

entry = pd.DataFrame(
    {"source": "Quality of Life",
     "target": "Happiness",
     "edge": "weight w3"}, index=[0])
kg_df = pd.concat([kg_df, entry])

entry = pd.DataFrame(
    {"source": "Quality of Life",
     "target": "Poverty",
     "edge": "weight w4"}, index=[0])
kg_df = pd.concat([kg_df, entry])

for elem in crime:
    entry = pd.DataFrame(
        {"source": "Crime",
         "target": elem,
         "edge": "co"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

for elem in life:
    entry = pd.DataFrame(
        {"source": "Life",
         "target": elem,
         "edge": "co"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

for elem in hap:
    entry = pd.DataFrame(
        {"source": "Happiness",
         "target": elem,
         "edge": "co"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

for elem in pov:
    entry = pd.DataFrame(
        {"source": "Poverty",
         "target": elem,
         "edge": "co"}, index=[0])
    kg_df = pd.concat([kg_df, entry])

G = nx.from_pandas_edgelist(kg_df, "source", "target",
                          edge_attr=True, create_using=nx.DiGraph())

ll = ['Crime', 'Life', 'Happiness', 'Poverty']

from pyvis.network import Network

nt = Network('1920px', '1080px', directed=True, notebook=False, select_menu=False,
             filter_menu=False, )
# nt.barnes_hut()
for node in G:
    if node == "Quality of Life":
        color = "blue"
        size = 20
    elif node in ll:
        color = "purple"
        size = 15
    elif node == "World":
        color = "yellow"
        size = 20
    elif node in df_merged['region'].unique():
        color = "orange"
        size = 15
    elif node in df_merged['sub-region'].unique():
        color = "green"
        size = 10

    elif node in df_merged['Country'].unique():
        color = "lightgray"
        size = 10
    else:
        color = "black"
        size = 10
    nt.add_node(node, label=node, color=color, size=size)

for edge in G.edges:
    #     print(edge)
    nt.add_edge(edge[0], edge[1], color="gray", width=1, \
                label=kg_df[(kg_df['source'] == edge[0]) & (kg_df['target'] == edge[1])]['edge'][0])

nt.show_buttons(filter_=['nodes'])

nt.show('kg.html')