import mouseAtlasViewer as mav
import os.path
import pandas as pd
import pyvista as pv
import pyvistaqt as pvqt
import numpy as np

# %% Define paths
# Join current path with new folder  name ccf2017
atlasFolder = os.path.join(os.path.curdir,"ccf2017")
atlasResolution = 10  # available resolutions are 10,25,50 and 100 microns


# %% Download atlas (if not already present)
mav.downloadAtlas(atlasFolder)

# %% Load atlas
ann = mav.loadAtlas(atlasFolder, atlasResolution)


# %% Create brain surface
brain = mav.makeBrainContour(ann)


# %% Set up 3d plotter

# Use pvqt.BackgroundPlotter for an interactive display or pv.Plotter to create
# the animation under the %%Make video section

pInt = pv.Plotter(off_screen=True, window_size=(1600, 1200))

pInt.set_background('white')
pInt.add_mesh(brain, color='black', opacity=.15, smooth_shading=True)


# %% Add region meshes
regionsToPlot = ["MOB", "V4", "CEA", "TH", "SUB"]

colours = ["4BC6B9", "73C1C6", "96C3CE", "A79AB2", "B57BA6"]

# Initialize lists to collect data for the legend
abbreviations = []
annotations = []
shortLegend = []
longLegend = []

for r, abbr in enumerate(regionsToPlot):

    region_data = mav.getRegionData(abbr)
    if region_data is None:
        continue

    regionId = region_data['id']
    regionName = region_data['name']
    print(f"Adding region: {regionName} (ID: {regionId}, Abbreviation: {abbr})")

    surf = mav.makeRegionByID(ann, regionId)
    pInt.add_mesh(surf, color=colours[r])

    # 4. Store the data for the legend
    abbreviations.append(abbr)
    annotations.append(regionName)
    shortLegend.append((abbr, colours[r]))
    longLegend.append((regionName, colours[r]))


# Uncomment one of the following two lines depending on what you want to appear in the legend
legend_entries = list(zip(abbreviations, colours))
#legend_entries = list(zip(annotations, colours))

pInt.add_legend(legend_entries, bcolor=None)
pInt.add_bounding_box()
pInt.enable_anti_aliasing()

#pInt.show()                     # for interactive display with BackgroundPlotter
#pause = input("Press Enter to continue...")  # keep window open
#pInt.show(auto_close=False)   # for video making

# %% Make video
output_dir = "media/"

viewup = [0, 0, 1]
path = pInt.generate_orbital_path(
        factor=2.0, n_points=360, viewup=viewup, shift=np.size(ann, 2)*2)
filename = os.path.join(output_dir, "orbit_"+str(atlasResolution)+".gif")
pInt.open_gif(filename)
# pInt.open_movie("orbit.mp4", quality=5, framerate=15)
pInt.orbit_on_path(path, write_frames=True, viewup=viewup, step=0.05)
#pInt.close()


# %% Take scrennshots from different angles

os.makedirs(output_dir, exist_ok=True) # Ensure the output directory exists

# List of views and their corresponding file suffixes
views = {
    "top": pInt.view_xy,
    "front": pInt.view_yz,
    "right": pInt.view_xz,
    "iso": pInt.view_isometric, # Bonus 3/4 view
}

print("Capturing high-resolution screenshots...")

for name, view_func in views.items():
    # 1. Set the camera view
    view_func()
    
    # 2. Reset the camera to fit the data perfectly in the new orientation
    # pInt.camera_position = pInt.show() 
    pInt.reset_camera()

    # 3. Save the screenshot
    filename = os.path.join(output_dir, f"atlas_{atlasResolution}_{name}.png")
    
    # Take the screenshot. 
    # The `window_size` (set when initializing Plotter) controls the base resolution.
    pInt.screenshot(filename)
    
    # You can also use the scale argument to double/triple the resolution:
    # pInt.screenshot(filename, scale=2) 
    
    print(f"Saved: {filename}")