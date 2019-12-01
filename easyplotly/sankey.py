"""Sankey plot"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def _source_target_series(links):
    """Transform the input, if possible, in a pandas Series with a multiindex of dimension two: source x target"""
    if isinstance(links, pd.DataFrame):
        links = links.copy().stack()
    elif isinstance(links, dict):
        links = pd.Series(links)

    if not isinstance(links, pd.Series):
        try:
            _ = (i for i in links)
        except TypeError:
            raise TypeError("'links' should be (an interable) of Pandas Series, not {}".format(type(links)))
        return pd.concat((_source_target_series(i) for i in links))
    assert isinstance(links.index, pd.MultiIndex) and len(links.index.names) == 2, \
        "'links' should have source x target as its index"
    return links


def Sankey(link_value, **kwargs):
    """Sankey diagrams

    :param link_value: a dataframe with the value of the links (rows=source, columns=target), a series with a
        two-dimensional multiindex (source/target), or a list of such objects
    :param kwargs: additional arguments like 'node_label': a dict, series or callable: node id => label, or
    'link_label': a series with an index similar to 'link_value', or a function source, target => label
    :return: a go.Sankey object
    """
    link_value = _source_target_series(link_value)
    node_ids = list(set(link_value.index.get_level_values(0)).union(link_value.index.get_level_values(1)))
    node_ids.sort()
    node_nums = np.arange(len(node_ids))

    node_id_to_num_dict = dict(zip(node_ids, node_nums))

    def node_id_to_num(i):
        return node_id_to_num_dict[i]

    trace = dict(
        node=dict(label=node_ids),
        link=dict(
            source=[node_id_to_num(i) for i in link_value.index.get_level_values(0)],
            target=[node_id_to_num(i) for i in link_value.index.get_level_values(1)],
            value=link_value.values
        ))

    for arg in kwargs:
        value = kwargs[arg]
        if isinstance(value, (str, int, float, list)):
            trace[arg] = value
        elif arg.startswith('link_'):
            if callable(value):
                trace[arg] = [value(source, target) for (source, target) in link_value.index]
            else:
                value = _source_target_series(value)
                trace[arg] = [value.loc[link] for link in link_value.index]
        else:
            if callable(value):
                fun = value
            else:
                def fun(i):
                    return value[i]
            trace[arg] = [fun(i) for i in node_ids]

    return go.Sankey(**trace)
