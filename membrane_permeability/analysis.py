from westpa.analysis import Run, HDF5MDTrajectory

with Run.open('west.h5') as run:
    topweight = None
    topwalker = None

    for walker in run.recycled_walkers:
        if topweight is None or topweight < walker.weight:
            topweight = walker.weight
            topwalker = walker

    walker = topwalker
    trace = walker.trace()

    trajectory = HDF5MDTrajectory()
    traj = trajectory(trace)

    traj.save('trace-%d-%d.h5' % (walker.iteration.number, walker.index))
