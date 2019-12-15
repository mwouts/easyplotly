# Easy Plotly

[![Build Status](https://travis-ci.com/mwouts/easyplotly.svg?branch=master)](https://travis-ci.com/mwouts/easyplotly)
[![codecov.io](https://codecov.io/github/mwouts/easyplotly/coverage.svg?branch=master)](https://codecov.io/github/mwouts/easyplotly?branch=master)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/mwouts/easyplotly.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/mwouts/easyplotly/context:python)
[![Pypi](https://img.shields.io/pypi/v/easyplotly.svg)](https://pypi.python.org/pypi/easyplotly)
[![pyversions](https://img.shields.io/pypi/pyversions/easyplotly.svg)](https://pypi.python.org/pypi/easyplotly)
[![Jupyter Notebook](https://img.shields.io/badge/Binder-Notebook-blue.svg)](
    https://mybinder.org/v2/gh/mwouts/easyplotly/master?filepath=README.md)
[![GitHub.io](https://img.shields.io/badge/GitHub-HTML-blue.svg)](https://mwouts.github.io/easyplotly)
<a class="github-button" href="https://github.com/mwouts/easyplotly" data-icon="octicon-star" data-show-count="true" aria-label="Star mwouts/easyplotly on GitHub">Star</a>

This is on-going research on how ploting with [Plotly.py](https://github.com/plotly/plotly.py), 
especially ploting of hierarchical data, could be made easier.

See the outputs of the commands below - tables and plots - 
in the [HTML export](https://mwouts.github.io/easyplotly/) of this notebook.
Or even, open this `README.md` as a notebook and run it interactively on 
[Binder](https://mybinder.org/v2/gh/mwouts/easyplotly/master?filepath=README.md)!

## Installation

Install the `easyplotly` python package with

```
pip install easyplotly
```

## Sample data

Our sample data is the population and life expectancy, per country and region:

```python
import world_bank_data as wb
import itables.interactive

# Collect countries
countries = wb.get_countries()
region_country = countries[['region', 'name']].rename(columns={'name': 'country'})

# Population & life expectancy
region_country['population'] = wb.get_series('SP.POP.TOTL', mrv=1, id_or_value='id', simplify_index=True)
region_country['life_expectancy'] = wb.get_series('SP.DYN.LE00.IN', mrv=1, id_or_value='id', simplify_index=True)

# Observations restricted to the countries
pop_and_exp = region_country.loc[countries.region != 'Aggregates'].set_index(['region', 'country']).sort_index()
pop_and_exp
```

## Sunburst Charts

```python
import plotly.graph_objects as go
import plotly.io as pio
import easyplotly as ep

pio.renderers.default = 'notebook_connected'
layout = go.Layout(title='World Population and Life Expectancy<br>Data from the World Bank', height=800)
```

Our `Sunburst` function accepts inputs of many types: pandas Series, dictionaries, and list of such objects.
If you want, you can redefine `labels`, or add other arguments like `text` - use either a Series with an index
identical to that of `values`, or a function that to any tuple `(level0, level1, ... leveln)`
associates the corresponding label or value.

```python
sunburst = ep.Sunburst(pop_and_exp.population, text=pop_and_exp.life_expectancy)
go.Figure(sunburst, layout)
```

## Treemaps

The `Treemap` function works like the `Sunburst` one:

```python
treemap = ep.Treemap(pop_and_exp.population, text=pop_and_exp.life_expectancy)
go.Figure(treemap, layout)
```

Just like the `Sunburst` function, it also accepts all the arguments supported by the original
`go.Sunburst` object. You're even welcome to use the
[magic underscore notation](https://plot.ly/python/creating-and-updating-figures/#magic-underscore-notation),
as we do below when we set `marker.colors` with `marker_colors`:

```python
import numpy as np


def average(values, weights):
    """Same as np.average, but remove nans"""
    total_obs = 0.
    total_weight = 0.
    if isinstance(values, np.float):
        values = [values]
        weights = [weights]
    for x, w in zip(values, weights):
        xw = x * w
        if np.isnan(xw):
            continue
        total_obs += xw
        total_weight += w
    return total_obs / total_weight if total_weight != 0 else np.NaN


def life_expectancy(item):
    """Life expectancy associated to a tuple like (), ('Europe & Central Asia') or ('East Asia & Pacific', 'China')"""
    sub = pop_and_exp.loc[item] if item else pop_and_exp
    return average(sub.life_expectancy, weights=sub.population)


def text(item):
    """Return the text associated to a tuple like (), ('Europe & Central Asia') or ('East Asia & Pacific', 'China')"""
    life_exp = life_expectancy(item)
    if life_exp > 0:
        pop = pop_and_exp.population.loc[item].sum() if item else pop_and_exp.population.sum()  
        return 'Population: {:,}<br>Life expectancy: {:.2f}'.format(int(pop), life_exp)


treemap = ep.Treemap(pop_and_exp.population,
                     hoverinfo='label+text',
                     text=text,
                     root_label='World',
                     # magic underscore notation
                     marker_colors=life_expectancy,
                     marker_colorscale='RdBu')

go.Figure(treemap, layout)
```

Treemaps and Sunburst also accept trees with a non-constant depth - use a dictionary indexed with tuples of varying size. For instance, here is a tree that represents the files in this project:

```python
import os
from plotly.colors import DEFAULT_PLOTLY_COLORS

project_files = os.popen('git ls-tree --name-only -r master').read().split()

size = {tuple(path.split('/')):os.stat(path).st_size for path in project_files}
log_size = {i: np.log(size[i]) for i in size}
extensions = set(os.path.splitext(path)[1] for path in project_files)
color_map = dict(zip(extensions, DEFAULT_PLOTLY_COLORS))

def node_color(node):
    if not node:
        return
    node_extension = os.path.splitext(node[-1])[1]
    return color_map[node_extension]
```

```python
treemap = ep.Treemap(log_size,
                     text=size,
                     hoverinfo='label+text',
                     marker_colors=node_color,
                     root_label='https://github.com/mwouts/easyplotly')

go.Figure(treemap)
```

## Sankey Plot

Plot links from a dict, or a series with a source/target multiindex:

```python
links = {('A', 'B'): 3, ('B', 'C'): 1, ('B', 'D'): 2, ('C', 'A'): 1, ('D', 'A'): 1, ('A', 'D'): 1}
go.Figure(ep.Sankey(links))
```

Plot links from a DataFrame (sources as the index, targets as the columns):

```python
import pandas as pd
```

```python
links = pd.DataFrame(1, index=['Source A', 'Source B'], columns=['Target'])
go.Figure(ep.Sankey(links))
```

We conclude the examples with a plot in which the links are a list of pandas Series:

```python
region_income = wb.get_countries().query("region != 'Aggregates'").copy()
region_income['population'] = wb.get_series('SP.POP.TOTL', mrv=1, id_or_value='id', simplify_index=True)
income_lending = region_income.copy()
region_income.set_index(['region', 'incomeLevel'], inplace=True)
income_lending.set_index(['incomeLevel', 'lendingType'], inplace=True)

layout = go.Layout(title='Regions income and lending type<br>Data from the World Bank')

sankey = ep.Sankey(
    link_value=[region_income['population'], income_lending['population']],
    link_label=[region_income['name'], income_lending['name']])

go.Figure(sankey, layout)
```

<script async defer src="https://buttons.github.io/buttons.js"></script>
