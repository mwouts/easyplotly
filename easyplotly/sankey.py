"""Sankey plot"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def source_target_series(links):
    """

    :param links: a dataframe with the value of the link (rows=source, columns=target), a series with a
        two-dimensional multiindex (source/target), or a list of such objects
    :return:
    """
    if isinstance(links, pd.DataFrame):
        links = links.stack()
    elif isinstance(links, dict):
        links = pd.Series(links)
        
    if not isinstance(links, pd.Series):
        try:
            _ = (i for i in links)
        except TypeError:
            raise TypeError("'links' should be (an interable) of Pandas Series, not {}".format(type(links)))
        return pd.concat((source_target_series(i) for i in links))
    assert isinstance(links.index, pd.MultiIndex) and len(links.index.names) == 2, \
        "'links' should have source x target as its index"
    return links


def Sankey(links, node_labels=None, link_labels=None):
    """Sankey plots made easy

    :param links: a dataframe with the value of the link (rows=source, columns=target), a series with a
        two-dimensional multiindex (source/target), or a list of such objects
    :param node_labels: (optional) the labels for the nodes: a dict, series or callable: node id => label
    :param link_labels: (optional) the labels for the links: a series with an index similar to 'links'
    :return: a go.Sankey object
    """
    links = source_target_series(links)

    if node_labels is None:
        def node_id_to_label(i):
            return i
    elif isinstance(node_labels, dict):
        def node_id_to_label(i):
            return node_labels[i]
    elif isinstance(node_labels, pd.Series):
        assert len(node_labels.index.names) == 1, "'node_labels' should have a simple index"

        def node_id_to_label(i):
            return node_labels.loc[i]
    elif callable(link_labels):
        node_id_to_label = node_labels
    else:
        raise TypeError("'link_labels' should be either a series, a dict, or a callable")

    node_ids = list(set(links.index.get_level_values(0)).union(links.index.get_level_values(1)))
    node_ids.sort()
    node_nums = np.arange(len(node_ids))

    node_id_to_num_dict = dict(zip(node_ids, node_nums))

    def node_id_to_num(i):
        return node_id_to_num_dict[i]

    node = dict(label=list(map(node_id_to_label, node_ids)))
    link = dict(
        source=list(map(node_id_to_num, links.index.get_level_values(0))),
        target=list(map(node_id_to_num, links.index.get_level_values(1))),
        value=links.values
    )

    if link_labels is not None:
        link_labels = source_target_series(link_labels)
        link['label'] = link_labels.values

    return go.Sankey(node=node, link=link)
