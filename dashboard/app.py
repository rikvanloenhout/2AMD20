from ke_app.main import app
from ke_app.views.menu import make_menu_layout
from ke_app.views.world_cl import CloroMap
from ke_app.views.frequencyplot import FrequencyPlot
from ke_app.data import get_crime_data, get_life_data, get_happiness_data, get_poverty_data, get_merged

from dash import html, dcc, dash_table
import plotly.express as px
from dash.dependencies import Input, Output




if __name__ == '__main__':
    # Create data
    df_crime = get_crime_data()
    df_life = get_life_data()
    df_happ = get_happiness_data()
    df_pov = get_poverty_data()
    # print(df_merged)

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
                "Mean Crime Index, 2015", \
                frequencyPlot1.update(df_crime, "Mean Crime Index", "freq"), \
                "Distribution Mean Crime Index, 2015"
        elif selected_data == "Life":
            return cloroMap1.update(df_life, "Life expectancy "), \
                "Life Expectancy, 2015", \
                frequencyPlot1.update(df_life, "Life expectancy ", "freq"), \
                "Distribution Life Expectancy, 2015"
        elif selected_data == "Happiness":
            return cloroMap1.update(df_happ, "Happiness Score", on_hover=["Happiness Rank"]), \
                "Happiness Score, 2015", \
                frequencyPlot1.update(df_happ, "Happiness Score", "freq"), \
                "Distribution Happiness Score, 2015"
        elif selected_data == "Poverty":
            return cloroMap1.update(df_pov, "Gini"), \
                "Gini Index, 2015", \
                frequencyPlot1.update(df_pov, "Gini", "freq"), \
                "Distribution Gini Index, 2015"
        elif selected_data == "Custom Scores":
            if all(map(lambda x: x is not None, vals)):
                # print(vals)
                df_merged = get_merged(vals[0], vals[1], vals[2], vals[3])
            else:
                df_merged = get_merged(0.25, 0.25, 0.25, 0.25)
            return cloroMap1.update(df_merged, "Aggregate Scores", on_hover=["Rank"]), \
                "Aggregate Scores, 2015", \
                frequencyPlot1.update(df_merged, "Aggregate Scores", "bar"), \
                "Aggregate Scores, 2015"



    app.run_server(debug=True, dev_tools_ui=True)
