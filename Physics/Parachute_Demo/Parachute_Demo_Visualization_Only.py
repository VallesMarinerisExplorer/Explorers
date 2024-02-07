"""This file shows how soft body cloths in PyBullet can be used to visualize materials like parachutes. This file does
not model the complex aerodynamics of a parachute, but forces have been applied to the bottom to make it appear to be
falling somewhat realistically."""

import pybullet as p
import pybullet_data
import math
def get_key_pressed(camerapitch, camerayaw, cameradist):
    pressed_keys = []
    events = p.getKeyboardEvents()
    key_codes = events.keys()

    for key in key_codes:
        pressed_keys.append(key)
    if len(pressed_keys)==0:
        return camerapitch, camerayaw, cameradist
    if pressed_keys[0] == 65297:
        camerapitch -= 0.01
    elif pressed_keys[0] == 65298:
        camerapitch += 0.01
    elif pressed_keys[0] == 65295:
        camerayaw -= 0.01
    elif pressed_keys[0] == 65296:
        camerayaw += 0.01
    elif pressed_keys[0] == 108:
        cameradist += 0.002
    elif pressed_keys[0] == 107:
        cameradist -= 0.002


    return camerapitch, camerayaw, cameradist
camerapitch = -40
camerayaw = 90
cameradist = 1
# camerax = 10
# cameray = 10
# cameraz = 10


# Connect to the physics server
p.connect(p.GUI, options='--background_color_red=0.2 --background_color_green=0.2 --background_color_blue=0.2')
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.resetSimulation(p.RESET_USE_DEFORMABLE_WORLD)
# p.setGravity(0, 0, -9.8)
useRealTimeSim = 1
p.setRealTimeSimulation(useRealTimeSim)

clothId = p.loadSoftBody("parachute3.obj", basePosition = [0,0,0], scale = 0.01, mass = 1., useNeoHookean = 1, useBendingSprings=1,useMassSpring=1, springElasticStiffness=1, springDampingStiffness=.1, springDampingAllDirections = 0, useSelfCollision = 1, frictionCoeff = .5, useFaceContact=1)
# texture = p.loadTexture("YourTexture.jpg")
p.changeVisualShape(clothId, -1, flags=p.VISUAL_SHAPE_DOUBLE_SIDED)#,textureUniqueId=texture)
# p.getMeshData(clothId)
basepos = []
boxes =[]
# print(p.getMeshData(clothId)[0])
numpoints = int(p.getMeshData(clothId)[0]/4)-19
for i in range(0, numpoints):
    basepos.append([p.getMeshData(clothId)[1][i][0],p.getMeshData(clothId)[1][i][1], p.getMeshData(clothId)[1][i][2]])

for i in range(0, numpoints):
    box = p.createMultiBody(baseMass=1, basePosition=basepos[i])
    boxes.append(box)  # Store the box object in the list
for i in range(0, numpoints):
    p.createSoftBodyAnchor(clothId, i, boxes[i], -1)
edgenums = [1,8,15,24,31,43,50,64,70,82,89,103]
theta = [210,240,270,300,330,360,30,60,90,120,150,180]
# for i in range(0,numpoints):
#     if ((i-1)/7)%1 == 0:
#         edgenums.append(i)
# print(edgenums)

while True:
    camerapitch, camerayaw, cameradist = get_key_pressed(camerapitch, camerayaw, cameradist)
    p.resetDebugVisualizerCamera(cameraDistance=cameradist, cameraYaw=camerayaw, cameraPitch=camerapitch,
                                 cameraTargetPosition=[0,0,0])
    thetaval = 0
    for i in range(0,numpoints-1):

        if i in edgenums:
            p.applyExternalForce(boxes[i], -1, [-math.cos(math.radians(theta[thetaval])), -math.sin(math.radians(theta[thetaval])), -2], [0, 0, 0], flags=1)
            thetaval+=1
        # else:
        #    p.applyExternalForce(boxes[i], -1, [0, 0, 1], [0, 0, 0], flags=1)
