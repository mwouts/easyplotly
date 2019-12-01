"""Sankey plot"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


def source_target_series(links):
    """

    :param links: a dataframe with the value of the links (rows=source, columns=target), a series with a
        two-dimensional multiindex (source/target), or a list of such objects
    :return:
    """
    if isinstance(links, pd.DataFrame):
        links = links.copy().stack()
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

    :param links: a dataframe with the value of the links (rows=source, columns=target), a series with a
        two-dimensional multiindex (source/target), or a list of such objects
    :param node_labels: (optional) the labels for the nodes: a dict, series or callable: node id => label
    :param link_labels: (optional) the labels for the links: a series with an index similar to 'links',
    or a function source, target => label
    :return: a go.Sankey object
    """
    links = source_target_series(links)
    if node_labels is None:
        def node_id_to_label(i):
            return i
    elif callable(node_labels):
        node_id_to_label = node_labels
    else:
        def node_id_to_label(i):
            return node_labels[i]

    node_ids = list(set(links.index.get_level_values(0)).union(links.index.get_level_values(1)))
    node_ids.sort()
    node_nums = np.arange(len(node_ids))

    node_id_to_num_dict = dict(zip(node_ids, node_nums))

    def node_id_to_num(i):
        return node_id_to_num_dict[i]

    sankey_node = dict(label=[node_id_to_label(i) for i in node_ids])
    sankey_link = dict(
        source=[node_id_to_num(i) for i in links.index.get_level_values(0)],
        target=[node_id_to_num(i) for i in links.index.get_level_values(1)],
        value=links.values
    )

    if callable(link_labels):
        sankey_link['label'] = [link_labels(source, target) for (source, target) in links.index]
    elif link_labels is not None:
        link_labels = source_target_series(link_labels)
        sankey_link['label'] = link_labels.values

    return go.Sankey(node=sankey_node, link=sankey_link)
