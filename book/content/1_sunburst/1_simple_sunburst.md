# A simple Sunburst plot

## The World Population as a Pandas Series

To begin with we download the World Population indicator from the [World Bank](https://data.worldbank.org/). 
We organize the data as a series indexed by World Region and Country.

```python
import world_bank_data as wb
import pandas as pd


# Displaying a few rows only is enough
pd.set_option('display.max_rows', 6)

# Collect countries
countries = wb.get_countries()
countries = countries[['region', 'name']].rename(columns={'name': 'country'})

# Population
countries['population'] = wb.get_series('SP.POP.TOTL', mrv=1, id_or_value='id', simplify_index=True)

# Remove aggregate (regions and world)
countries = countries.loc[countries.region != 'Aggregates'].set_index(['region', 'country']).sort_index()

# The result is a Pandas series with a multiindex
population = countries.population
population
```

## Our first sunburst plot

EasyPlotly's `Sunburst` will automatically aggregate the values of the population at higher levels:

```python
import easyplotly as ep
sunburst = ep.Sunburst(population)
```

The result is a `go.Sunburst` object, so you can plot it as usual with

```python
import plotly.graph_objects as go
go.Figure(sunburst, layout=dict(title='World Population<br>Data from the World Bank'))
```
