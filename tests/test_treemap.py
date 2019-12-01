import pytest
import pandas as pd
import plotly.graph_objects as go
from easyplotly import Treemap


@pytest.fixture()
def treemap_expected():
    return go.Treemap(
        ids=['/A/OK', '/B/OK', '/B/Not OK', '/A', '/B'],
        labels=['OK', 'OK', 'Not OK', 'A', 'B'],
        parents=['/A', '/B', '/B', None, None],
        values=[1, 2, 1, 1, 3],
        branchvalues='total'
    )


@pytest.fixture()
def treemap_input():
    return pd.Series({('A', 'OK'): 1, ('B', 'OK'): 2, ('B', 'Not OK'): 1})


def test_treemap(treemap_expected, treemap_input):
    assert Treemap(treemap_input) == treemap_expected


def test_treemap_relative(treemap_expected, treemap_input):
    treemap_expected.branchvalues = 'remainder'
    treemap_expected.values = [1, 2, 1, 0, 0]
    assert Treemap(treemap_input, branchvalues='remainder') == treemap_expected


def test_treemap_labels_fun(treemap_expected, treemap_input):
    def labels(item):
        return item[-1].lower()

    treemap_expected.labels = ['ok', 'ok', 'not ok', 'a', 'b']
    assert Treemap(treemap_input, labels=labels) == treemap_expected


def test_negative_raise_error():
    with pytest.raises(ValueError, match='Negative'):
        Treemap({('A', 'a'): -5})
