import sys
import pytest

try:
    import unittest.mock as mock
except ImportError:
    import mock
import pandas as pd
import plotly.graph_objects as go
from easyplotly import Sunburst

if sys.version_info < (3, 6):
    pytest.skip(msg="dict is not ordered", allow_module_level=True)


@pytest.fixture()
def sunburst_expected():
    return go.Sunburst(
        ids=['/A/OK', '/B/OK', '/B/Not OK', '/A', '/B'],
        labels=['OK', 'OK', 'Not OK', 'A', 'B'],
        parents=['/A', '/B', '/B', None, None],
        values=[1, 2, 1, 1, 3],
        branchvalues='total'
    )


@pytest.fixture()
def sunburst_with_root():
    return go.Sunburst(
        ids=['/A/OK', '/B/OK', '/B/Not OK', '/', '/A', '/B'],
        labels=['OK', 'OK', 'Not OK', '', 'A', 'B'],
        parents=['/A', '/B', '/B', None, '/', '/'],
        values=[1, 2, 1, 4, 1, 3],
        branchvalues='total'
    )


@pytest.fixture()
def sunburst_input():
    return {('A', 'OK'): 1, ('B', 'OK'): 2, ('B', 'Not OK'): 1}


def test_sunburst(sunburst_expected, sunburst_input):
    assert Sunburst(sunburst_input) == sunburst_expected


def test_sunburst_with_root(sunburst_with_root, sunburst_input):
    assert Sunburst(sunburst_input, root_label='') == sunburst_with_root


def test_sunburst_simple_index():
    sunburst_input = {'A': 2, 'B': 3}
    sunburst_expected = go.Sunburst(
        ids=['/A', '/B'],
        labels=['A', 'B'],
        parents=[None, None],
        values=[2, 3],
        branchvalues='total'
    )
    assert Sunburst(sunburst_input) == sunburst_expected


def test_sunburst_remainder(sunburst_expected, sunburst_input):
    sunburst_expected.branchvalues = 'remainder'
    sunburst_expected.values = [1, 2, 1, 0, 0]
    assert Sunburst(sunburst_input, branchvalues='remainder') == sunburst_expected


def test_sunburst_maxdepth(sunburst_expected, sunburst_input):
    sunburst_expected.maxdepth = 1
    assert Sunburst(sunburst_input, maxdepth=1) == sunburst_expected


def test_sunburst_text(sunburst_expected, sunburst_input, text={'A': 'a', ('A', 'OK'): 'a ok'}):
    sunburst_expected.text = ['a ok', '', '', 'a', '']
    assert Sunburst(sunburst_input, text=text) == sunburst_expected


def test_sunburst_text_fun(sunburst_expected, sunburst_input):
    def text(i):
        return ' '.join(i).lower() if i else ''

    sunburst_expected.text = ['a ok', 'b ok', 'b not ok', 'a', 'b']
    assert Sunburst(sunburst_input, text=text) == sunburst_expected


def test_sunburst_index_none_is_removed():
    sunburst_input = pd.Series({('I', '1', 'a'): 1, ('I', '1', 'b'): 1, ('I', '2', None): 1})
    sunburst_expected = go.Sunburst(
        ids=['/I/1/a', '/I/1/b', '/I/1', '/I', '/I/2'],
        labels=['a', 'b', '1', 'I', '2'],
        parents=['/I/1', '/I/1', '/I', None, '/I'],
        values=[1, 1, 2, 3, 1],
        branchvalues='total')
    assert Sunburst(sunburst_input) == sunburst_expected


def test_negative_raise_error():
    with pytest.raises(ValueError, match='Negative'):
        Sunburst({('A', 'a'): -5})


def test_parent_value_strictly_larger():
    with mock.patch('easyplotly.internals.EPS', 0.01):
        sunburst_input = {('A', 'a', '1', 'i'): 1.0}
        sunburst_expected = go.Sunburst(
            ids=['/A/a/1/i', '/A/a/1', '/A/a', '/A'],
            labels=['i', '1', 'a', 'A'],
            parents=['/A/a/1', '/A/a', '/A', None],
            values=[1., 1.01, 1.02, 1.03],
            branchvalues='total'
        )
        assert Sunburst(sunburst_input) == sunburst_expected
