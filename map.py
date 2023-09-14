import json
import plotly.graph_objects as go
from dash import dash, dcc, html


class InfraMap:
    nodes_path = "json_data/nodes_orb.json"
    lines_path = "json_data/lines_orb.json"
    broken_lines = []

    def __init__(self):
        self.__load_data(self.nodes_path, self.lines_path)
        self.__build_lines()
        self.__build_points()
        self.__build_clusters()
        self.__build_cps()
        self.__build_measuring_unit()
        self.__build_gas_system()
        self.__build_map()
        self.__run_dash()

    def __load_data(self, nodes_path: str, lines_path: str):
        with open(nodes_path, 'r', encoding='utf-8-sig') as f:
            self.nodes = json.loads(f.read())
        with open(lines_path, 'r', encoding='utf-8-sig') as f:
            self.lines = json.loads(f.read())

    def __build_lines(self):
        x_coords = []
        y_coords = []
        names = []
        x_coords, y_coords = self.__make_line_coords(x_coords, y_coords, names)
        self.map_lines = go.Scatter(
            x=x_coords, y=y_coords, text=names,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

    def __make_line_coords(self, x_coords: list, y_coords: list, names: list):
        for line in self.lines:
            node_from = [node for node in self.nodes if node["routeId"] == line["routeFrom"]]
            node_to = [node for node in self.nodes if node["routeId"] == line["routeTo"]]
            if node_from and node_to:
                line_from_coord_x = node_from[0]["coordX"]
                line_from_coord_y = node_from[0]["coordY"]
                line_to_coord_x = node_to[0]["coordX"]
                line_to_coord_y = node_to[0]["coordY"]
                x_coords.append(line_from_coord_x)
                x_coords.append(line_to_coord_x)
                x_coords.append(None)
                y_coords.append(line_from_coord_y)
                y_coords.append(line_to_coord_y)
                y_coords.append(None)
                names.append(line["id"])
            else:
                self.broken_lines.append(line)

        return x_coords, y_coords

    def __build_points(self):
        nodes = [node for node in self.nodes if node["typeId"] == 0]
        x_coords = [node["coordX"] for node in nodes]
        y_coords = [node["coordY"] for node in nodes]
        names = [node["name"] for node in nodes]
        self.map_points = go.Scatter(
            x=x_coords, y=y_coords, text=names,
            mode='markers+text',
            textposition='bottom center',
            hoverinfo='text',
            marker=dict(
                reversescale=True,
                color=[],
                size=5,
                line_width=2))

    def __build_clusters(self):
        nodes = [node for node in self.nodes if node["typeId"] == 1]
        x_coords = [node["coordX"] for node in nodes]
        y_coords = [node["coordY"] for node in nodes]
        names = [point["name"] for point in nodes]
        self.map_clusters = go.Scatter(
            x=x_coords, y=y_coords, text=names,
            mode='markers+text',
            textposition='bottom center',
            hoverinfo='text',
            marker=dict(
                reversescale=True,
                color="green",
                size=10,
                line_width=2))

    def __build_measuring_unit(self):
        nodes = [node for node in self.nodes if node["typeId"] == 2]
        x_coords = [node["coordX"] for node in nodes]
        y_coords = [node["coordY"] for node in nodes]
        names = [point["name"] for point in nodes]
        self.map_measuring_units = go.Scatter(
            x=x_coords, y=y_coords, text=names,
            mode='markers+text',
            textposition='bottom center',
            hoverinfo='text',
            marker=dict(
                reversescale=True,
                color="yellow",
                size=10,
                line_width=2))

    def __build_gas_system(self):
        nodes = [node for node in self.nodes if node["typeId"] == 3]
        x_coords = [node["coordX"] for node in nodes]
        y_coords = [node["coordY"] for node in nodes]
        names = [point["name"] for point in nodes]
        self.map_gas_system = go.Scatter(
            x=x_coords, y=y_coords, text=names,
            mode='markers+text',
            textposition='bottom center',
            hoverinfo='text',
            marker=dict(
                reversescale=True,
                color="orange",
                size=10,
                line_width=2))

    def __build_cps(self):
        nodes = [node for node in self.nodes if node["typeId"] == 6]
        x_coords = [node["coordX"] for node in nodes]
        y_coords = [node["coordY"] for node in nodes]
        names = [point["name"] for point in nodes]
        self.map_cps = go.Scatter(
            x=x_coords, y=y_coords, text=names,
            mode='markers+text',
            textposition='bottom center',
            hoverinfo='text',
            marker=dict(
                reversescale=True,
                color="blue",
                size=15,
                line_width=2))

    def __build_map(self):
        self.fig = go.Figure(data=[self.map_points, self.map_clusters, self.map_measuring_units,
                                   self.map_gas_system,
                                   self.map_cps, self.map_lines],
                             layout=go.Layout(
                                 title='Infra',
                                 showlegend=False,
                                 hovermode='closest',
                                 margin=dict(b=20, l=5, r=5, t=40),
                                 xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                 yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                             )
        self.fig.update_layout(
            font=dict(
                size=5,
                color="Black"
            )
        )

    def __run_dash(self):
        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        app = dash.Dash(external_stylesheets=external_stylesheets)

        app.layout = html.Div([
            dcc.Graph(figure=self.fig, style={'width': '95%', 'height': '95%'})
        ])

        app.run_server(debug=False)
