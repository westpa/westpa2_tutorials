import enum
import mdtraj as md
import numpy as np


def compute_com(traj, atom_indices=None):
    """Compute the center of mass for each frame.
    Parameters
    ----------
    traj : Trajectory
        Trajectory to compute center of mass for
    atom_indices : list of int
        Atoms to compute center of mass for. If None,
        will compute over all atoms
    Returns
    -------
    com : np.ndarray, shape=(n_frames, 3)
         Coordinates of the center of mass for each frame
    """

    if atom_indices is None:
        atoms = traj.top.atoms
        coords = traj.xyz
    else:
        if not len(atom_indices):
            raise ValueError("empty atom_indices")
        atoms = [traj.top.atom(i) for i in atom_indices]
        coords = np.take(traj.xyz, atom_indices, axis=1)

    com = np.zeros((traj.n_frames, 3))
    masses = np.array([a.element.mass for a in atoms])
    masses /= masses.sum()

    for i, x in enumerate(coords):
        com[i, :] = x.astype("float64").T.dot(masses)
    return com


def compute_drug_to_memb_distance(traj):
    top = traj.topology

    com_z_drug = [
        z
        for _, _, z in compute_com(traj, atom_indices=top.select("resname 'LIG'"))
    ]
    com_z_memb_e = [
        z
        for _, _, z in compute_com(traj, atom_indices=top.select("resname 'POP' and chainid 4"))
    ]
    com_z_memb_f = [
        z
        for _, _, z in compute_com(traj, atom_indices=top.select("resname 'POP' and chainid 5"))
    ]

    dist_e = np.subtract(com_z_memb_e, com_z_drug) * 10.0
    dist_f = np.subtract(com_z_drug, com_z_memb_f) * 10.0

    dist = np.max((dist_e, dist_f), axis=0)

    return dist


if __name__ == "__main__":
    from sys import argv

    outfile = argv[1]
    trajfile = argv[2]
    topfile = argv[3] if len(argv) > 3 else None

    if topfile:
        traj = md.load(trajfile, top=topfile)
    else:
        traj = md.load(trajfile)

    dists = compute_drug_to_memb_distance(traj)
    np.savetxt(outfile, dists)
