# mouseAtlasViewer
A python package which allows to plot any brain region annotated in the Allen brain Atlas in a 3D interactive way with pyVista.

## Setup
Preferentially install the mouseAtlasViewer package in a conda environment as follows: 
```
conda env create -f environment.yml
conda activate mav
```

## Usage

Check out *exampleUsage.py* for an example of how to create a plot or an animation.  Once the package is installed, the mainmodules can be imported with:
```Python
import mouseAtlasViewer as mav
```
and used with the following methods:

```Python
mav.downloadAtlas(atlasFolder)

ann = mav.loadAtlas(atlasFolder, atlasResolution)

brain = mav.makeBrainContour(ann)

region_data = mav.getRegionData("TH") # TH short fo thalamus

surf = mav.makeRegionByID(ann, region_data["id"])
```
The creation of each surface can take some time and be quite computationally expensive (on RAM usage especially).
This higly depends on the version of the atlas used, where the high-resolution(10um) version will take the most time 
but will be the best looking.

The spreadsheet *Annotated regions list.xlsx* can be used to quickly look up the id of the region(s) to be displayed.

## Example

![example animation](media/orbit_10.gif)

## Further info

Check out the documentation from [pyVista](https://docs.pyvista.org/) for further info on isosurface plotting. 

