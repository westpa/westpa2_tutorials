import mdtraj as md
import numpy as np

def calc_radius_of_gyration(traj):
    atom_indices = traj.top.select("resname LIG")
    ligtraj = traj.atom_slice(atom_indices)
    masses = np.array([atom.element.mass for atom in ligtraj.top.atoms])
    rg = md.compute_rg(ligtraj, masses=masses)

    return rg

if __name__ == "__main__":
    from sys import argv

    outfile = argv[1]
    trajfile = argv[2]
    topfile = argv[3] if len(argv) > 3 else None

    if topfile:
        traj = md.load(trajfile, top=topfile)
    else:
        traj = md.load(trajfile)

    dists = calc_radius_of_gyration(traj)
    np.savetxt(outfile, dists)
