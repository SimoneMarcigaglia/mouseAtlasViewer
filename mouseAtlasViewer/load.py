from os.path import exists
import wget
import os.path
import nrrd
import numpy as np


def downloadAtlas(destinationFolder):

    url = "http://download.alleninstitute.org/informatics-archive/current-release/mouse_ccf/annotation/ccf_2017/"

    resolutions = [10, 25, 50, 100]

    for res in resolutions:
        filename = "annotation_" + str(res) + ".nrrd"
        filepath = os.path.join(destinationFolder, filename)

        if exists(filepath):
            print(filename + " already present.")
        else:
            fileURL = url + filename
            wget.download(fileURL, out=filepath)

            print("\r Downloaded " + filename)

    url = 'http://data.cortexlab.net/allenCCF/'
    filename = 'structure_tree_safe_2017.csv'
    filepath = os.path.join(destinationFolder, filename)
    if exists(filepath):
        print(filename + " already present.")
    else:
        fileURL = url + filename
        wget.download(fileURL, out=filepath)

        print("\r Downloaded " + filename)


def loadAtlas(atlasFolder, atlasResolution=100):

    atlasFilename = "annotation_" + str(atlasResolution) + ".nrrd"
    atlasPath = os.path.join(atlasFolder, atlasFilename)

    if not exists(atlasPath):
        downloadAtlas(atlasFolder)

    data, header = nrrd.read(atlasPath)

    data = np.transpose(data, (0, 2, 1))
    data = data[::-1, :, ::-1]

    return data
