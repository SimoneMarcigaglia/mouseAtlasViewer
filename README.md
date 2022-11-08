# mouseAtlasViewer
A python package which allows to plot any brain region annotated in the Allen brain Atlas in a 3D interactive way with pyVista.

## Setup
Install the mouseAtlasViewer package by navigating to the cloned folder and running: 
```
pip install .
```
either machine-wide or in a local environment. For older versions of Python, *setuptools* might need to be installed separately  (and before the command above) with:
```
pip install setuptools
```

## Usage

Check out *exampleUsage.py* for an example of how to create a plot or an animation.  Once the package is installed, the mainmodules can be imported with:
```Python
from mouseAtlasViewer import load
from mouseAtlasViewer import view
```
The creation of each surface can take some time and be quite computationally expensive (on RAM usage especially).
This higly depends on the version of the atlas used, where the high-resolution(10um) version will take the most time 
but will be the best looking.

The spreadsheet *Annotated regions list.xlsx* can be used to quickly look up the id of the region(s) to be displayed.

## Example

![example animation](orbit.gif)

## Further info

Check out the documentation from [pyVista](https://docs.pyvista.org/) for further info on isosurface plotting. 

