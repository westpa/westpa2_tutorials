from simtk.openmm import app, XmlSerializer, MonteCarloMembraneBarostat
from simtk.unit import kelvin, bar, nanometer
from openmmforcefields.generators import SystemGenerator
from openff.toolkit.topology import Molecule


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
omm_sys_serialized = XmlSerializer.serialize(system)

with open('system.xml', 'wt') as f:
    f.write(omm_sys_serialized)
