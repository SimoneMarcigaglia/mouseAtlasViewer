import pyvista as pv
import numpy as np


def hasChildren(targetId, tree):

    repetitions = (tree == targetId).sum()

    if repetitions == 1:
        hasChildren = False
    elif repetitions > 1:
        hasChildren = True
    else:
        print("Invalid index!")
        hasChildren = -1

    return hasChildren


def matriciseTree(st):

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


def findChildren(targetId, st):
    tree = matriciseTree(st)

    if not hasChildren(targetId, tree):
        indices = [targetId]
    else:
        # Remove rows that do not have the index from tree
        indices = np.empty([0, 0])
        mask = (tree == targetId)
        mask = mask.sum(axis=1)
        mask = np.array(mask, dtype=bool)

        filteredTree = tree[mask, :]
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


def makeRegionByID(av, st, targetId):

    indices = findChildren(targetId, st)

    region = np.full(av.shape, False)

    for index in indices:
        region = np.logical_or(region, av == index)

    # Create the spatial reference
    grid = pv.UniformGrid()
    grid.dimensions = av.shape
    region = 1.0*region  # bool to float
    grid.point_data['values'] = region.ravel(order='F')

    surface = grid.contour(isosurfaces=2, progress_bar=True)

    return surface


def makeBrainContour(av, gaussianSmoothingstd=0):

    # Create the spatial reference
    grid = pv.UniformGrid()
    grid.dimensions = av.shape
    brain = 1.0*(av > 1)  # bool to float
    grid.point_data['values'] = brain.ravel(order='F')

    if not gaussianSmoothingstd == 0:
        grid = grid.gaussian_smooth(std_dev=gaussianSmoothingstd)

    surface = grid.contour(isosurfaces=2, progress_bar=True)

    return surface
