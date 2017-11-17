# web_data_models_project [D&K2017]
**YAX Parser** (**Y**et **A**nother **X**ML Parser)
This project is about implementing an XML parser using a DTD file, both the XML and the DTD files are symplified.

# How to Run ?
there is no need to download additional libraries, you just need python 3 installed.  
To run the program run the command below:  
**`./python yax_parser_CLI.py <xml_file_path> <dtd_file_path>`**

# Analysis and experiment document
to display the jupyter notebook and see the analysis and all the tests we did you need to install [jupyter notebook](http://jupyter.org/).  
In order to execute the notebook, if you want to redo the tests, you will need these dependencies:
* [sklearn](http://scikit-learn.org/stable/index.html) (for machine learning)
* [matplotlib](https://matplotlib.org/) (for plotting)
* [numpy](http://www.numpy.org/)

either you download each of the dependencies or you just install [Anaconda3](https://www.anaconda.com/download/#linux) distribution that already includes them.  
**To run the tests on the memory consumption** you need to add [memory porfiler](https://pypi.python.org/pypi/memory_profiler) module.
## How to display the notebook ?
run the command below:  
**`jupyter notebook <path_to_notebook>`**.  if you are in the root of the project hierarchy, **`<path_to_notebook>`** should be replaced by **`jupyter_notebook/YAX_parser.ipynb`**

you can find a none executable version of the notebook [here in GitHub](https://github.com/MassyB/web_data_models_project/blob/master/jupyter_notebook/YAX_parser.ipynb), but it's not displaying the figure for Thompons' construction rules.
