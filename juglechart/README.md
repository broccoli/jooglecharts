

# What is JugleChart?
JugleChart is Python/jupyter api for creating a Google Chart using generated javascript and html that calls the Google Charts library.  JugleChart generates the javascript and html for you.  You don't have to worry about loading the chart library, creating valid javascript or html, or creating unique id's for your chart containers.

*** Note: JugleChart is a thin wrapper for Google Charts.  You must consult Google Charts documenation for all types and options to pass to JugleChart.  It does not replace the Google Charts documentation.***

JugleChart is designed to be simple, so it has some limitations over coding your own Google Chart.
* JugleChart accepts only one set of data.
* JugleChart can create only one chart from the data.
* JugleChart does not support javascript event handling.
* Data Views are not (yet) supported.
* Loading data from an external source is not (yet) supported.

JugleChart will allow you to do with a chart whatever the most generic Google Chart javascript structure permits.  It will plug your configurations into a basic javascript template.  In other words, any charts and options that do not require specially coded javascript should work in JugleChart.  What JugleChart will let you do:
* Use most (if not all) Google Chart types.
* Use most (if not all) Google Chart configuration options.
* Use most Formatters for customizing data display (currently excepting only ColorFormat).
* Create one or more dashboard controls that can bind to the data or to other controls.


# Dependencies

## Python 2.7
The following following packages must be installed.  Specific versions not tested.
* gviz_api
* pandas
* ipython
* jupyter
* juglechart
* jinja2

You can install gviz_api from git at https://github.com/google/google-visualization-python
`````
pip install git+https://github.com/google/google-visualization-python
`````

## Javascript
* jquery (already part of the jupyter environment)

## CSS
* bootstrap (already part of the jupyter environment)


