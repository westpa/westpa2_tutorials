from simtk.openmm import app
from simtk.unit import nanometer, kelvin, bar, nanometer, picosecond
from simtk.openmm import MonteCarloMembraneBarostat, LangevinIntegrator, Platform
from openmmforcefields.generators import SystemGenerator
from openff.toolkit.topology import Molecule

from simtk.openmm.app import StateDataReporter
from mdtraj.reporters import HDF5Reporter


pdb = app.PDBFile('bstate.pdb')
molecule = Molecule.from_smiles('CCCCO')

forcefield_kwargs = {'constraints': app.HBonds,
                     'removeCMMotion': False}
periodic_forcefield_kwargs = {'nonbondedMethod': app.LJPME,
                              'nonbondedCutoff': 1*nanometer}
membrane_barostat = MonteCarloMembraneBarostat(1*bar, 0.0*bar*nanometer, 308*kelvin,
                                               MonteCarloMembraneBarostat.XYIsotropic,
                                               MonteCarloMembraneBarostat.ZFree,
                                               15)
system_generator = SystemGenerator(forcefields=['amber/lipid17.xml', 'amber/tip3p_standard.xml'],
                                   small_molecule_forcefield='gaff-2.11',
                                   barostat=membrane_barostat,
                                   forcefield_kwargs=forcefield_kwargs,
                                   periodic_forcefield_kwargs=periodic_forcefield_kwargs)

system = system_generator.create_system(pdb.topology, molecules=molecule)
integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 0.002*picosecond)

platform = Platform.getPlatformByName('CUDA')

simulation = app.Simulation(pdb.topology, system, integrator, platform)
simulation.context.setPositions(pdb.positions)

simulation.loadState('parent.xml')
simulation.reporters.append(StateDataReporter('seg.nfo', 5000, step=True, potentialEnergy=True, kineticEnergy=True, temperature=True))
simulation.reporters.append(HDF5Reporter('seg.h5', 10000))
simulation.step(50000)
simulation.saveState('seg.xml')
