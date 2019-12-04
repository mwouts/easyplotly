0.1.3 (2019-12-04)
==================

Fixed
-----
- Fix the epsilons added to values of Sunburst and Treemap when the graph has a root (#3)


0.1.2 (2019-12-04)
==================

Fixed
-----
- Sunburst and Treemap charts also work with dictionaries and pandas Series with a one-dimensional index (#4)
- Add epsilon when summing floats to fix the issue of Sunburst and Treemap not shown (#3)

0.1.1 (2019-12-02)
==================

Added
-----
- `Sunburst`, `Treemap` and `Sankey` accept the same arguments as the corresponding Plotly object.
- Nested arguments like `marker_colors` are also supported (this is Plotly's _magic underscore notation_).

0.1.0 (2019-12-01)
==================

Initial release with `Sunburst`, `Treemap` and `Sankey` plots.