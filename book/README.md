# EasyPlotly's Book

In this folder we have a series of notebooks that demo how to use EasyPlotly.
The notebooks are deployed as a Jupyter Book at [Netlify](https://www.netlify.com).

## Building the book locally

We assume that you have installed [Ruby](https://www.ruby-lang.org) and then [Bundler](https://bundler.io/) with e.g. `gem install bundler`.

You should also have a Python environment ready, with all the requirements for the EasyPlotly installed, e.g:
```
conda create -n easyplotly plotly numpy pandas jupyter ipykernel pytest
conda activate easyplotly
pip install -r requirements-dev.txt
pip install -e .
python -m ipykernel install --name easyplotly-kernel --user
```

Then we create our Jupyter Book with
```
jupyter-book create build/book --overwrite --content-folder book/content --config book/config.yml --toc book/toc.yml
```

Then we turn the Markdown files into Jupyter Notebooks by adding an explicit Kernel to them:
```
jupytext --set-kernel easyplotly-kernel build/book/content/*/*.md
```

Finally we build the book locally with
```
jupyter-book build build/book
```

Supposedly you can serve the book locally with
```
make serve
```

Now if we want to publish the book, we do:
```
cd build/book/_build
git init
git add .
git commit -m 'Add Book'
git remote add origin https://github.com/mwouts/easyplotly-book.git
git push -uf --set-upstream origin master
```

At this stage, the book is not working. GitHub says:

```
Your site is having problems building: The variable {{ x.observe(notebookContainer, {childList: true} on line 197 in 1_sunburst/1_simple_sunburst.html was not properly closed with }}. For more information, see https://help.github.com/en/github/working-with-github-pages/troubleshooting-jekyll-build-errors-for-github-pages-sites#tag-not-properly-terminated. 
```