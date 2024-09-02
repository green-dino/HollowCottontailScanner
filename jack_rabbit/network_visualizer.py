from bokeh.io import output_file, show
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool, LabelSet, ColumnDataSource
from bokeh.plotting import from_networkx
from bokeh.palettes import Spectral4

class NetworkVisualizer:
    @staticmethod
    def visualize_graph(G, pos):
        plot = Plot(width=1920, height=1080, x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
        plot.title.text = "Network Map"
        
        graph_renderer = from_networkx(G, pos, scale=1, center=(0, 0))
        graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
        graph_renderer.edge_renderer.glyph = MultiLine(line_alpha=0.8, line_width=1)
        plot.renderers.append(graph_renderer)
        
        plot.add_tools(HoverTool(tooltips=None), BoxZoomTool(), ResetTool())
        
        source = ColumnDataSource(data=dict(
            x=[pos[0] for pos in pos.values()],
            y=[pos[1] for pos in pos.values()],
            label=list(G.nodes())
        ))
        
        labels = LabelSet(x='x', y='y', text='label', source=source,
                           text_font_size='10pt', x_offset=5, y_offset=5)
        plot.add_layout(labels)
        
        return plot