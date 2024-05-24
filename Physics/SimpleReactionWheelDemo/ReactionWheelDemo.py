import pybullet as p
import time
# This script demonstrates how a spinning reaction wheel can change the orientation of a spacecraft (box) with conservation of angular momentum. The 
# script has the wheel speed up, slow down and reverse, and the surrounding spacecraft body eventually changes its spin direction as well.

# LET IT BE NOTED TO ANYONE WHO READS THIS IN THE FUTURE. ROLL PITCH AND YAW ARE ALWAYS DEFINED IN RADIANS IN THE URDF, NOT DEGREES
p.connect(p.GUI, options='--background_color_red=0 --background_color_green=0 --background_color_blue=0')
p.setGravity(0, 0, 0)

p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

# Load the cube with two wheels attached
cubeStartPos = [0, 0, 0]
cubeStartOrientation = p.getQuaternionFromEuler([0, 0, 0])
cubeId = p.loadURDF("ReactionWheelSpacecraft.urdf", cubeStartPos, cubeStartOrientation, globalScaling=0.01)

# Enable motors for the wheels (assuming they are specified in your URDF file)
motorIds = [0]  # Adjust these IDs based on your URDF file
p.setJointMotorControlArray(cubeId, jointIndices=motorIds, controlMode=p.VELOCITY_CONTROL, forces=[0])

# Set initial velocities for reaction wheels
initial_wheel_velocities = [0.0, 0.0]

# Set pybullet realtime simulation to false (timestepped manually each while loop iteration)
p.setRealTimeSimulation(0)

i = 0
p.changeDynamics(cubeId, -1, linearDamping=0, angularDamping=0, rollingFriction=0.001, spinningFriction=0.001, maxJointVelocity=100000000000)
while True:
    # cube_orientation = p.getQuaternionFromEuler(p.getEulerFromQuaternion(p.getBasePositionAndOrientation(cubeId)[1]))

    if i < 500 or i> 800:
        forcearray = [0.00001]
    else:
        forcearray = [-0.0001]
    p.setJointMotorControlArray(cubeId, jointIndices=motorIds, controlMode=p.TORQUE_CONTROL, forces=forcearray)
    p.stepSimulation()
    i+=1
    wheel_states = p.getJointState(cubeId, motorIds[0])
    angular_velocity = wheel_states[1]
    print(angular_velocity)
    time.sleep(1/240)
