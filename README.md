# mouseAtlasViewer
A python package which allows to plot any brain region annotated in the Allen brain Atlas in a 3D interactive way with pyVista.

## Setup
Install the required packages by running 
```
pip install -r requirements.txt
```
either machine-wide or in a local environment.

## Usage

Check out *exampleUsage.py* for an example of how to create a plot or an animation. The creation 
of each surface can take some time and be quite computationally expensive (on RAM usage especially).
This higly depends on the version of the atlas used, where the high-resolution(10um) version will take the most time 
but will be the best looking.

The spreadsheet *Annotated regions list.xlsx* can be used to quickly look up the id of the region(s) to be displayed.

## Example

![example animation](orbit.gif)

## Further info

Check out the documentation from [pyVista](https://docs.pyvista.org/) for further info on isosurface plotting. 

