"""Easy Plotly"""

import plotly.graph_objects as go
from .sankey import Sankey
from .sunburst import Sunburst
from .treemap import Treemap
from .version import __version__

__all__ = ['go', 'Sankey', 'Sunburst', 'Treemap', '__version__']
