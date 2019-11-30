import numpy as np
import plotly.graph_objects as go


def Sunburst(tree, root_label=''):
    assert isinstance(tree, dict)

    # Create the missing intermediate nodes in the dict,
    # and give them a weight 0 (or the total weight)
    complete_tree = tree.copy()
    for item in tree:
        if isinstance(item, tuple):
            for depth in range(1, len(item)):
                parent = item[:-depth]
                if parent not in tree:
                    complete_tree.setdefault(parent, 0)

    all_nodes = list(complete_tree.keys())
    nodes_ids = dict(zip(all_nodes, range(1, 1 + len(all_nodes))))

    return go.Sunburst(
        ids=np.arange(0, 1 + len(all_nodes)),
        labels=[root_label] + [i[-1] if isinstance(i, tuple) else i for i in all_nodes],
        parents=[None] + [nodes_ids[i[:-1]] if isinstance(i, tuple) and len(i)>1 else 0 for i in all_nodes],
        values=[0] + [complete_tree[i] for i in all_nodes],
    )
