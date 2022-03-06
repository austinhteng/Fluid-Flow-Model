from phi.flow import *

scene = Scene.create('./data/')

bounds=Box[0:32, 0:40]
GRAVITY = math.tensor([0, -9.81])
DT = 1

water_ref = CenteredGrid(Noise(), extrapolation.BOUNDARY, x=32, y=40, bounds=bounds)
velocity_ref = StaggeredGrid(0, extrapolation.ZERO, x=32, y=40, bounds=bounds)
#velocity_ref = StaggeredGrid(Noise(), extrapolation.ZERO, x=32, y=40, bounds=bounds) * 10

water_ref = water_ref.with_values(math.maximum(water_ref.values, 0))

vis.plot([water_ref, velocity_ref])

water = water_ref
velocity = velocity_ref

#add gravity
gravity_force = GRAVITY * DT
#gravity_force = 0
velocity += gravity_force
velocity, _ = fluid.make_incompressible(velocity)

for i in range(20):
  water = advect.mac_cormack(water, velocity, dt=DT)
  gravity_force = water * GRAVITY * DT @ velocity
  velocity = advect.semi_lagrangian(velocity, velocity, dt=DT) + gravity_force
  velocity, _ = fluid.make_incompressible(velocity)

  scene.write({'water' : water, 'velocity' : velocity}, fames=i)