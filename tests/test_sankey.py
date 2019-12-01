import pandas as pd
import pytest
import plotly.graph_objects as go
from easyplotly import Sankey


@pytest.fixture()
def sankey_a_b_target():
    return go.Sankey(
        node=dict(label=['Source A', 'Source B', 'Target']),
        link=dict(
            source=[0, 1],
            target=[2, 2],
            value=[1, 1]
        ))


def test_sankey_df(sankey_a_b_target, df=pd.DataFrame(1, index=['Source A', 'Source B'], columns=['Target'])):
    assert Sankey(df) == sankey_a_b_target


def test_sankey_dict(sankey_a_b_target, links={('Source A', 'Target'): 1, ('Source B', 'Target'): 1}):
    assert Sankey(links) == sankey_a_b_target


def test_sankey_two_series():
    x = pd.Series({('A', 'B'): 1})
    y = pd.Series({('B', 'C'): 1})
    node_label = {'A': 'a', 'B': 'b', 'C': 'c'}
    sankey_expected = go.Sankey(
        node=dict(label=['a', 'b', 'c']),
        link=dict(
            source=[0, 1],
            target=[1, 2],
            value=[1, 1]
        ))
    assert Sankey((x, y), node_label=node_label) == sankey_expected
    sankey_expected.link.label = ['ab', 'bc']

    def link_label(source, target):
        return ''.join([source, target]).lower()

    assert Sankey((x, y), node_label=node_label, link_label=link_label) == sankey_expected
