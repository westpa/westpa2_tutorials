import logging
import mdtraj as md
import numpy as np

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])
log = logging.getLogger("msm_we")

def processCoordinates(self, coords):
    log.debug("Processing coordinates")

    if self.dimReduceMethod == "none":
        nC = np.shape(coords)
        nC = nC[0]
        data = coords.reshape(nC, 3 * self.nAtoms)
        return data

    if self.dimReduceMethod == "pca" or self.dimReduceMethod == "vamp":

        # Dimensionality reduction 

        xt = md.Trajectory(xyz=coords, topology=None)
        indCA = self.reference_structure.topology.select("name CA")
        pair1, pair2 = np.meshgrid(indCA, indCA, indexing="xy")
        indUT = np.where(np.triu(pair1, k=1) > 0)
        pairs = np.transpose(np.array([pair1[indUT], pair2[indUT]])).astype(int)
        dist = md.compute_distances(xt, pairs, periodic=True, opt=True)
        
        return dist

def reduceCoordinates(self, coords):
    """
    Defines the coordinate reduction strategy used.
    The reduced corodinates are stored in /auxdata for each iteration.

    Parameters
    ----------
    coords: array-like
        Array of coordinates to reduce.

    Returns
    -------
    Reduced data

    """

    log.debug("Reducing coordinates")

    if self.dimReduceMethod == "none":
        nC = np.shape(coords)
        nC = nC[0]
        data = coords.reshape(nC, 3 * self.nAtoms)
        return data

    if self.dimReduceMethod == "pca" or self.dimReduceMethod == "vamp":
        coords = self.processCoordinates(coords)
        coords = self.coordinates.transform(coords)
        return coords

    raise Exception


log.info("Loading user-override functions for modelWE")
