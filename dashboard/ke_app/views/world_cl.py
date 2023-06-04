from dash import dcc, html
import plotly.express as px


class CloroMap(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name, id=f"CloroMap_{name}"),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, df, colorby, on_hover=None):
        if on_hover is None:
            self.fig = px.choropleth(df,
                                     locations="ISO",
                                     color=colorby,
                                     hover_name="Country",
                                     color_continuous_scale=px.colors.sequential.Plasma)
        else:
            self.fig = px.choropleth(df,
                                     locations="ISO",
                                     color=colorby,
                                     hover_name="Country",
                                     color_continuous_scale=px.colors.sequential.Plasma,
                                     hover_data=on_hover)
        self.fig.update_layout(height=700)
        return self.fig
