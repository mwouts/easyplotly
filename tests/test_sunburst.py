import pytest
import plotly.graph_objects as go
from easyplotly import Sunburst


@pytest.fixture()
def sunburst_expected():
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


def test_sunburst_relative(sunburst_expected, sunburst_input):
    sunburst_expected.branchvalues = 'remainder'
    sunburst_expected.values = [1, 2, 1, 0, 0, 0]
    assert Sunburst(sunburst_input, branchvalues='remainder') == sunburst_expected


def test_sunburst_text(sunburst_expected, sunburst_input, text={'A': 'a', ('A', 'OK'): 'a ok'}):
    sunburst_expected.text = ['a ok', '', '', '', 'a', '']
    assert Sunburst(sunburst_input, text=text) == sunburst_expected


def test_sunburst_text_fun(sunburst_expected, sunburst_input):
    def text(i):
        return ' '.join(i).lower() if i else ''

    sunburst_expected.text = ['a ok', 'b ok', 'b not ok', '', 'a', 'b']
    assert Sunburst(sunburst_input, text=text) == sunburst_expected


def test_negative_raise_error():
    with pytest.raises(ValueError, match='Negative'):
        Sunburst({('A', 'a'): -5})
