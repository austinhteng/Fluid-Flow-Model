from phi.flow import *

scene = Scene.at('./data', 0)

for i in view('scene,velocity,water', display='scene', play=False, namespace=globals()).range():
    water, velocity = scene.read(['water', 'velocity'], frame=i)