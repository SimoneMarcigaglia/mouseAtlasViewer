import mouseAtlasViewer as mav
import os.path
import pandas as pd
import pyvista as pv
import pyvistaqt as pvqt
import numpy as np

# %% Define paths
atlasFolder = "ccf2017"
atlasResolution = 100  # available resolutions are 10,25,50 and 100 microns


# %% Load atlas
mav.downloadAtlas(atlasFolder)
st = pd.read_csv(os.path.join(atlasFolder, 'structure_tree_safe_2017.csv'))
ann = mav.loadAtlas(atlasFolder, atlasResolution)


# %% Create brain surface
brain = mav.makeBrainContour(ann)


# %% Set up 3d plotter

# Use pvqt.BackgroundPlotter for an interactive display or pv.Plotter to create
# the animation under the %%Make video section

pInt = pvqt.BackgroundPlotter(off_screen=False, window_size=(800, 600))
# pInt = pv.Plotter(off_screen=True, window_size=(800, 600))


pInt.set_background('black')
pInt.add_mesh(brain, color='white', opacity=.15, smooth_shading=True)


# %% Add region meshes
regionIndices = [507, 145, 536, 549, 502]
colours = ["4BC6B9", "73C1C6", "96C3CE", "A79AB2", "B57BA6"]
annotations = ["Main olfactory bulb", "Fourth ventricle",
               "Central amygdalar nucleus", "Thalamus", "Subiculum"]
abbreviations = ["MOB", "V4", "CEA", "TH", "SUB"]

for r, regionId in enumerate(regionIndices):
    surf = mav.makeRegionByID(ann, st, regionId)
    pInt.add_mesh(surf, color=colours[r])


# Uncomment one of the following two lines depending on what you want to appear in the legend
legend_entries = list(zip(abbreviations, colours))
#legend_entries = list(zip(annotations, colours))


pInt.add_legend(legend_entries, bcolor=None)
pInt.add_bounding_box()

pInt.show()                     # for interactive display
# pInt.show(auto_close=False)   # for video making

# %% Make video

# viewup = [0, 0, 1]
# path = pInt.generate_orbital_path(
#     factor=2.0, n_points=360, viewup=viewup, shift=np.size(ann, 2)*2)
# pInt.open_gif("orbit_10.gif")
# # pInt.open_movie("orbit.mp4", quality=5, framerate=15)
# pInt.orbit_on_path(path, write_frames=True, viewup=viewup, step=0.05)
# pInt.close()
