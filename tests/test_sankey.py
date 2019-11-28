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
