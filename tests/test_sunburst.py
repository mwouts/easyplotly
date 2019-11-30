import numpy as np
import pytest
import plotly.graph_objects as go
from easyplotly import Sunburst


@pytest.fixture()
def sunburst_expected():
    return go.Sunburst(
        ids=np.arange(6),
        labels=['', 'OK', 'OK', 'Not OK', 'A', 'B'],
        parents=[None, 4, 5, 5, 0, 0],
        values=[0, 1, 2, 1, 0, 0]
    )


@pytest.fixture()
def sunburst_input():
    return {('A', 'OK'): 1, ('B', 'OK'): 2, ('B', 'Not OK'): 1}


def test_sunburst_series(sunburst_expected, sunburst_input):
    assert Sunburst(sunburst_input) == sunburst_expected
