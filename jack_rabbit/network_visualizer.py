from bokeh.io import output_file, show
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool, LabelSet, ColumnDataSource
from bokeh.plotting import from_networkx
from bokeh.palettes import Spectral4
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class NetworkVisualizer:
    @staticmethod
    def create_plot():
        """Create and return a Bokeh plot with the desired dimensions and title."""
        plot = Plot(width=1920, height=1080, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
        plot.title.text = "Network Map"
        return plot

    @staticmethod
    def create_graph_renderer(G, pos):
        """Create and return a graph renderer from the networkx graph and positions."""
        graph_renderer = from_networkx(G, pos, scale=1, center=(0, 0))
        graph_renderer.node_renderer.glyph = Circle(radius=0.05, fill_color=Spectral4[0])
        graph_renderer.edge_renderer.glyph = MultiLine(line_alpha=0.8, line_width=1)
        return graph_renderer

    @staticmethod
    def create_labels(G, pos):
        """Create and return labels for the nodes."""
        data = {'x': [], 'y': [], 'ip': [], 'packet_count': [], 'label': []}

        for node in G.nodes():
            if node not in pos:
                logging.warning(f"Node {node} does not have a position.")
                continue

            if 'ip' not in G.nodes[node] or 'packet_count' not in G.nodes[node]:
                logging.warning(f"Node {node} does not have required attributes.")
                continue

            try:
                data['x'].append(pos[node][0])
                data['y'].append(pos[node][1])
                data['ip'].append(G.nodes[node]['ip'])
                data['packet_count'].append(G.nodes[node]['packet_count'])
                data['label'].append(f"{G.nodes[node]['ip']} ({G.nodes[node]['packet_count']} packets)")
            except KeyError as e:
                logging.error(f"KeyError for node {node}: {e}")

        source = ColumnDataSource(data=data)
        labels = LabelSet(x='x', y='y', text='label', source=source,
                          text_font_size='10pt', x_offset=5, y_offset=5)
        return labels

    @staticmethod
    def visualize_graph(G, pos):
        """Visualize the network graph using Bokeh."""
        plot = NetworkVisualizer.create_plot()
        graph_renderer = NetworkVisualizer.create_graph_renderer(G, pos)
        plot.renderers.append(graph_renderer)

        plot.add_tools(HoverTool(tooltips=[("IP", "@ip"), ("Packet Count", "@packet_count")]), BoxZoomTool(), ResetTool())

        labels = NetworkVisualizer.create_labels(G, pos)
        plot.add_layout(labels)

        # Log the total number of nodes
        logging.info(f"Total number of nodes in the graph: {len(G.nodes())}")

        return plot