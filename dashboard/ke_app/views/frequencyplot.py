from dash import dcc, html
import plotly.figure_factory as ff
import plotly.express as px


class FrequencyPlot(html.Div):
    def __init__(self, name):
        self.html_id = name.lower().replace(" ", "-")

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(name, id=f"FrequencyPlot_{name}"),
                dcc.Graph(id=self.html_id)
            ],
        )

    def update(self, df, col_name, ty):
        if ty == "freq":
            self.fig = ff.create_distplot([df[col_name]], group_labels=[col_name])
        elif ty == "bar":
            self.fig = px.bar(df, x='Country', y=col_name)
            self.fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
        return self.fig
