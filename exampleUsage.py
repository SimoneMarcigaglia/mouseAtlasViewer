from mouseAtlasViewer import load
from mouseAtlasViewer import view
import os.path
import pandas as pd
import pyvista as pv
import pyvistaqt as pvqt

# %% Define paths
atlasFolder = "ccf2017"
atlasResolution = 10  # available resolutions are 10,25,50 and 100 microns


# %% Load atlas
st = pd.read_csv(os.path.join(atlasFolder, 'structure_tree_safe_2017.csv'))
ann = load.loadAtlas(atlasFolder, atlasResolution)

# %% Create surfaces
brain = view.makeBrainContour(ann)

hip = view.makeRegionByID(ann, st, 1089)
pir = view.makeRegionByID(ann, st, 961)


# %% Plot

pInt = pvqt.BackgroundPlotter(off_screen=False, window_size=(800, 600))
# Alternatively use pv.Plotter but that is blocking (i.e. runs in the same thread)
pInt.set_background('white')
pInt.add_mesh(brain, color='black', opacity=.2, smooth_shading=True)

pInt.add_mesh(hip, color='red', smooth_shading=True)
pInt.add_mesh(pir, color='blue', smooth_shading=True)

pInt.add_bounding_box()

legend_entries = []
legend_entries.append(['Hippocampal formation', 'red'])
legend_entries.append(['Piriform cortex', 'blue'])
pInt.add_legend(legend_entries, bcolor=None)
pInt.show()


# %% Make video
pVid = pv.Plotter(off_screen=True, window_size=(800, 600))
pVid.set_background('white')
pVid.add_mesh(brain, color='black', opacity=.2, smooth_shading=True)

pVid.add_mesh(hip, color='red', smooth_shading=True)
pVid.add_mesh(pir, color='blue', smooth_shading=True)

pVid.add_bounding_box()
pVid.add_legend(legend_entries, bcolor=None)
pVid.show(auto_close=False)
viewup = [0, 0, 1]
path = pVid.generate_orbital_path(
    factor=2.0, n_points=360, viewup=viewup, shift=90)
pVid.open_gif("orbit.gif")
# pVid.open_movie("orbit.mp4", quality=5, framerate=15)
pVid.orbit_on_path(path, write_frames=True, viewup=viewup, step=0.05)
pVid.close()
