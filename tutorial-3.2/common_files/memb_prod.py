from simtk.openmm import (
    XmlSerializer,
    LangevinIntegrator,
    Platform,
)
from simtk.unit import kelvin, picosecond
from simtk.openmm import LangevinIntegrator, Platform
from simtk.openmm.app import (
    StateDataReporter,
    Simulation,
    PDBFile
)
from mdtraj.reporters import HDF5Reporter


with open('system.xml', 'rt') as f:
    xml_str = f.read()

system = system = XmlSerializer.deserialize(xml_str)
pdb = PDBFile('bstate.pdb')
integrator = LangevinIntegrator(300*kelvin, 1/picosecond, 0.002*picosecond)

platform = Platform.getPlatformByName('CUDA')

simulation = Simulation(pdb.topology, system, integrator, platform)
simulation.context.setPositions(pdb.positions)

simulation.loadState('parent.xml')
simulation.reporters.append(StateDataReporter('seg.nfo', 5000, step=True, potentialEnergy=True, kineticEnergy=True, temperature=True))
simulation.reporters.append(HDF5Reporter('seg.h5', 10000))
simulation.step(50000)
simulation.saveState('seg.xml')
