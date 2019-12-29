# EasyPlotly's Book

In this folder we have a series of notebooks that demo how to use EasyPlotly.
The notebooks are deployed as a Jupyter Book at [Netlify](https://www.netlify.com).

## Building the book locally

We assume that you are using Ubuntu 19.10, that you created a conda environment named `easyplotly` with
```bash
conda env create --file environment.yml
```

That environment already condains [Ruby](https://www.ruby-lang.org) abd [Bundler](https://bundler.io/).

We activate the environment with
```
conda activate easyplotly
```

and then we run 
```
bundle install
```

You should also have a Python environment ready, with all the requirements for the EasyPlotly installed, e.g:
```bash
pip install -e .
python -m ipykernel install --name easyplotly-kernel --user
```

Then we create our Jupyter Book with
```bash
jupyter-book create build/book --overwrite --content-folder book/content --config book/config.yml --toc book/toc.yml
```

Then we turn the Markdown files into Jupyter Notebooks by adding an explicit Kernel to them:
```bash
jupytext --set-kernel easyplotly-kernel build/book/content/*/*.md
```

Finally we build the book locally with
```
jupyter-book build build/book
```

You can also serve the book locally with
```
cd build/book/
make serve
```

Now if we want to publish the book, we do:
```
cd _build
git init
git add .
git commit -m 'Add Book'
git remote add origin https://github.com/mwouts/easyplotly-book.git
git push -uf --set-upstream origin master
```

At this stage, the book is not working. Both `make serve` and GitHub say:

```
The variable {{ x.observe(notebookContainer, {childList: true} on line 197 in 1_sunburst/1_simple_sunburst.html was not properly closed with }}. For more information, see https://help.github.com/en/github/working-with-github-pages/troubleshooting-jekyll-build-errors-for-github-pages-sites#tag-not-properly-terminated. 
```