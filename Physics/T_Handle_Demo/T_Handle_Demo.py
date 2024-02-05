"""This file demonstrates how PyBullet is capable of simulating attitude mechanics, which is particularly 
important to spacecraft attitude control and stability. An unstable shape (T-shaped handle) is spun, 
illustrating the unstable yet periodic behavior that is predicted by the intermediate-axis theorem."""

import pybullet as p
import time

p.connect(p.GUI, options='--background_color_red=0 --background_color_green=0 --background_color_blue=0')
urdfloc = "T_handle.urdf"
Thandle = p.loadURDF(urdfloc,globalScaling=0.1)
p.setRealTimeSimulation(1)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.changeDynamics(Thandle, -1, angularDamping=0.0)
p.resetBaseVelocity(Thandle,[0,0,0],[5,0.1,0])
while True:
    time.sleep(1 / 240)
