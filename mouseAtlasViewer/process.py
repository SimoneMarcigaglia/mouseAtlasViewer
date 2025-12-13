import importlib.resources as pkg_resources
import numpy as np
import pandas as pd
import pyvista as pv
import collections

def _load_st_data(): #Read in region list CSV as a pandas DataFrame
    file_path = pkg_resources.files('mouseAtlasViewer') / 'structure_tree_safe_2017.csv'
    
    return pd.read_csv(str(file_path))

def _matriciseTree(st):

    paths = st['structure_id_path'].astype('string')
    slashes = paths.apply(lambda x: x.count('/'))

    for i in range(len(paths)):
        for k in range(12-slashes[i]):
            paths[i] = paths[i] + '0/'

    matrixTree = paths.str.split('/', expand=True)
    matrixTree = matrixTree.iloc[:, 1:11]
    matrixTree = matrixTree.astype('int')
    matrixTree = matrixTree.to_numpy()

    return matrixTree

def _matriciseTree_optimized(st):
    # 1. Split the path string directly into columns
    # Example path: '/1/8/997/...'
    # Split: ['','1','8','997',...]
    matrixTree = st['structure_id_path'].str.split('/', expand=True)

    # 2. Select columns (assuming the first two columns are '' and '1')
    # Use iloc to select only the columns containing the actual IDs (up to the max depth needed)
    # The max depth of the mouse atlas is often around 10-12 levels.
    # Selecting columns 1:12 covers 11 levels, which is safer than 1:11.
    matrixTree = matrixTree.iloc[:, 1:12] # Up to 11 levels of depth

    # 3. Fill NaN/empty strings with 0 (where the path ends)
    # This replaces your custom '0/' padding logic but is much faster and cleaner.
    matrixTree = matrixTree.fillna('0')

    # 4. Replace any remaining empty strings (from splitting / at end) with '0'
    # This prevents the ValueError
    matrixTree = matrixTree.replace('', '0')

    # 5. Convert all columns to integers
    matrixTree = matrixTree.astype(int)

    # 6. Convert to a NumPy array for fast lookups later
    return matrixTree.to_numpy()



# 2. Calculate the matrix tree once at module load
# This runs the first time 'from mouseatlasviewer import view' is executed.
ST_DATA = _load_st_data()
MATRIX_TREE = _matriciseTree_optimized(ST_DATA)



def _hasChildren(targetId):

    repetitions = (MATRIX_TREE == targetId).sum()

    if repetitions == 1:
        hasChildren = False
    elif repetitions > 1:
        hasChildren = True
    else:
        print("Invalid index!")
        hasChildren = -1

    return hasChildren


def _findChildren(targetId):
    
    if not _hasChildren(targetId):
        indices = [targetId]
    else:
        # Remove rows that do not have the index from tree
        indices = np.empty([0, 0])
        mask = (MATRIX_TREE == targetId)
        mask = mask.sum(axis=1)
        mask = np.array(mask, dtype=bool)

        filteredTree = MATRIX_TREE[mask, :]
        nRows, nCols = filteredTree.shape
        for row in range(nRows):
            for col in range(nCols):
                if filteredTree[row, col] == 0:
                    indexToCheck = filteredTree[row, col-1]
                    if indexToCheck not in indices:
                        indices = np.append(indices, indexToCheck)
                        break
                elif col == nCols-1:
                    indices = np.append(indices, filteredTree[row, col])

    return indices

def _findChildren_optimized(targetId):
    
    # 1. Handle case where the ID does not exist
    if not (MATRIX_TREE == targetId).any():
        return np.array([targetId], dtype=int)

    # 2. Filter Rows: Create a boolean mask of rows that contain the target ID
    # (Same as before)
    mask = (MATRIX_TREE == targetId).any(axis=1)
    filteredTree = MATRIX_TREE[mask, :]

    # 3. Find Column Index (Depth) of the Target ID
    # np.argmax finds the index of the FIRST TRUE value in each row.
    # This efficiently finds the column index where the targetId first appears in each path.
    # We use a temp mask to only search in the filtered rows.
    col_indices = np.argmax(filteredTree == targetId, axis=1)

    # 4. Extract the Child IDs using the Calculated Indices
    # We create a simple array representing the row index (0, 1, 2, 3...)
    row_indices = np.arange(filteredTree.shape[0])
    
    # The child is ALWAYS in the column immediately following the target ID's column.
    child_cols = col_indices + 1
    
    # Use advanced indexing to pull the value at [row_indices, child_cols]
    # This selects the (N+1)th element for every row where N is the targetId's position.
    child_ids = filteredTree[row_indices, child_cols]

    # 5. Final Cleanup and Uniqueness
    
    # Filter out the '0' padding entries (which means the end of a branch)
    unique_indices = child_ids[child_ids != 0]

    # Add the targetId itself (required for the final contour mask)
    unique_indices = np.append(unique_indices, targetId)

    # Return only the unique IDs, ensuring no duplicates.
    return np.unique(unique_indices)


def getRegionData(abbreviation):
    """
    Looks up structure data (ID and name) using the region abbreviation.
    
    Args:
        abbreviation (str): The acronym/abbreviation of the region (e.g., "MOB").
        
    Returns:
        dict: A dictionary containing 'id' (int) and 'name' (str), or None if not found.
    """
    # Assuming ST_DATA is the globally loaded pandas DataFrame for the structure tree
    # If using the Option 2 Lazy Loading, you'd use _load_st_data() here.
    global ST_DATA 
    
    # 1. Find the row where the acronym matches the abbreviation
    match = ST_DATA[ST_DATA['acronym'] == abbreviation]
    
    if match.empty:
        print(f"Warning: Abbreviation '{abbreviation}' not found in structure tree.")
        return None
    
    # 2. Extract the ID and name from the first (and only) match
    region_id = match['id'].iloc[0]
    region_name = match['name'].iloc[0]
    
    return {
        'id': region_id,
        'name': region_name,
        'abbreviation': abbreviation # Include the abbreviation for completeness
    }


def makeRegionByID(av,targetId):

    indices = _findChildren_optimized(targetId)

    region = np.full(av.shape, False)

    for index in indices:
        region = np.logical_or(region, av == index)

    # Create the spatial reference
    grid = pv.ImageData()
    grid.dimensions = av.shape
    grid.spacing = (1, 1, 1)
    #region = 1.0*region  # bool to float
    region = region.astype(np.float32)
    grid.point_data['values'] = region.ravel(order='F')

    surface = grid.contour(isosurfaces=2, progress_bar=True)

    return surface


def makeBrainContour(av, gaussianSmoothingstd=0):

    # Create the spatial reference
    grid = pv.ImageData()
    grid.dimensions = av.shape
    grid.spacing = (1, 1, 1)
    brain = (av > 1).astype(np.float32)
    grid.point_data['values'] = brain.ravel(order='F')

    if not gaussianSmoothingstd == 0:
        grid = grid.gaussian_smooth(std_dev=gaussianSmoothingstd)

    surface = grid.contour(isosurfaces=2, progress_bar=True)

    return surface
