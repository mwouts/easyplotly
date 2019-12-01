"""Easy Plotly"""

import plotly.graph_objects as go
from .sankey import Sankey
from .sunburst import Sunburst
from .treemap import Treemap

__all__ = ['go', 'Sankey', 'Sunburst', 'Treemap']
