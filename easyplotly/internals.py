"""Functions internal to the easyplotly package"""

import pandas as pd
import numpy as np


def tree_like_structure_to_dict(values):
    """Transform a series, a dict, or a collection of such objects, into a dictionary index by tuples"""
    if isinstance(values, dict):
        return {item if isinstance(item, tuple) else (item,): values[item]
                for item in values}
    if isinstance(values, pd.Series):
        return tree_like_structure_to_dict(values.to_dict())
    raise TypeError('Expected a dict, or a pandas Series, but got {}'.format(type(values)))


def dict_to_function(fun_or_dict, default=''):
    """Transform a series, dict, etc into a function"""
    if callable(fun_or_dict):
        return fun_or_dict

    tree = tree_like_structure_to_dict(fun_or_dict)

    def dict_fun(i):
        return tree[i] if i in tree else default

    return dict_fun


def sunburst_or_treemap(values, root_label=None, branchvalues='total', **kwargs):
    """Return a dict compatible with either a sunburst or a treemap"""
    # Turn the input values into a dict (tuple) => value
    org_tree = tree_like_structure_to_dict(values)
    tree = org_tree.copy()

    for item in org_tree:
        if isinstance(item, tuple):
            value = values[item]
            if value < 0:
                raise ValueError('Negative value {} for {}'.format(value, item))

            for depth in range(len(item)):
                parent = item[:-depth]

                # Create the missing intermediate nodes in the dict, and give them a weight 0
                # (Unless the parent is the root and we don't have the root in the tree)
                if not parent and root_label is None:
                    continue

                tree.setdefault(parent, 0)

                if branchvalues == 'total' and not np.isnan(value):
                    # Sum the descendent weights onto the parents (skip nans)
                    tree[parent] += value

    all_nodes = list(tree.keys())

    def node_id(item):
        if root_label is None and not item:
            return None
        return '/' + '/'.join(item)

    if 'labels' in kwargs:
        label_function = dict_to_function(kwargs.pop('labels'))
    else:
        def label_function(i):
            return i[-1] if i else root_label

    trace = dict(
        ids=[node_id(i) for i in all_nodes],
        labels=[label_function(i) for i in all_nodes],
        parents=[node_id(i[:-1]) if i else None for i in all_nodes],
        values=[tree[i] for i in all_nodes],
        branchvalues=branchvalues
    )

    for arg in kwargs:
        text_function = dict_to_function(kwargs[arg])
        trace[arg] = [text_function(i) for i in all_nodes]

    return trace
