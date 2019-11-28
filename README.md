# Easy Plotly

[![Build Status](https://travis-ci.com/mwouts/easyplotly.svg?branch=master)](https://travis-ci.com/mwouts/easyplotly)
[![codecov.io](https://codecov.io/github/mwouts/easyplotly/coverage.svg?branch=master)](https://codecov.io/github/mwouts/easyplotly?branch=master)
[![Language grade: Python](https://img.shields.io/badge/lgtm-A+-brightgreen.svg)](https://lgtm.com/projects/g/mwouts/easyplotly/context:python)
[![Pypi](https://img.shields.io/pypi/v/easyplotly.svg)](https://pypi.python.org/pypi/easyplotly)
[![pyversions](https://img.shields.io/pypi/pyversions/easyplotly.svg)](https://pypi.python.org/pypi/easyplotly)
[![Jupyter Notebook](https://img.shields.io/badge/Binder-Notebook-blue.svg)](
    https://mybinder.org/v2/gh/mwouts/easyplotly/master?filepath=README.md)
[![GitHub.io](https://img.shields.io/badge/GitHub-HTML-blue.svg)](https://mwouts.github.io/easyplotly)
<a class="github-button" href="https://github.com/mwouts/easyplotly" data-icon="octicon-star" data-show-count="true" aria-label="Star mwouts/easyplotly on GitHub">Star</a>

This package collects a few functions that hopefully make Plotly plotting easier

## Installation

Install or update the `easyplotly` python package with

```
git clone https://github.com/mwouts/easyplotly.git
pip install -e easyplotly
```

## Sankey Plot

See the outputs of the commands below on [GitHub](https://mwouts.github.io/easyplotly/). Or even, open this `README.md` as a notebook and run it interactively on [Binder](https://mybinder.org/v2/gh/mwouts/easyplotly/master?filepath=README.md)!

```python
import plotly.graph_objects as go
import pandas as pd
import easyplotly as ep
```

Plot links from a dict, or a series with a source/target multiindex:
```python
links={('A', 'B'): 3, ('B', 'C'): 1, ('B', 'D'): 2, ('C', 'A'): 1, ('D', 'A'): 1, ('A', 'D'):1}
go.Figure(ep.Sankey(links))
```

Plot links from a DataFrame (sources as the index, targets as the columns):
```python
links = pd.DataFrame(1, index=['Source A', 'Source B'], columns=['Target'])
go.Figure(ep.Sankey(links))
```

```python

```
