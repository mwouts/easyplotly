"""Treemaps"""

import plotly.graph_objects as go
from .internals import sunburst_or_treemap


def Treemap(values, root_label=None, **kwargs):
    """
    Return a go.Treemap object with the given values
    :param values: a Pandas Series with a simple or a multiindex, a dict indexed by tuples, or a collection of such
    objects. All observations should be non-negatives.
    :param root_label: label for the root
    :param **kwargs: additional arguments like 'labels' or 'text' or 'marker_colors', 'branchvalues' or 'maxdepth'.
    Can be a Pandas Series, or a dict indexed by tuples, or a function that associates to each tuple its value
    """
    return go.Treemap(**sunburst_or_treemap(values, root_label, **kwargs))
