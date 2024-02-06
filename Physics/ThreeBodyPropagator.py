import pybullet as p
import time
import pybullet_data
import numpy as np
from scipy.integrate import odeint

"""This script demonstrates 3 body orbit propagation. You can move the camera using the arrow keys, O and P and also by
pressing ctrl + mouse click to pan around. It uses odeint from scipy for the integrator. You can adjust the
time scaling using the scalefactor parameter, i.e. increasing this makes time go faster. This script does not use real
distance values but is merely a demonstration of how you might model lagrange points, Near-Rectilinear Halo Orbits and 
other unique orbits with more than 1 gravitational well."""

def getKeysPressed2():
    # Credit Inwernos for inspiration
    keys = p.getKeyboardEvents()
    cam = p.getDebugVisualizerCamera()

    # Keys to change camera
    if keys.get(65297):  # Up Arrow
        xyz = cam[11]
        x = float(xyz[0]) + 0.125
        y = xyz[1]
        z = xyz[2]
        p.resetDebugVisualizerCamera(cameraYaw=cam[8], cameraPitch=cam[9], cameraDistance=cam[10],
                                     cameraTargetPosition=[x, y, z])
    if keys.get(65298):  # Down Arrow
        xyz = cam[11]
        x = float(xyz[0]) - 0.125
        y = xyz[1]
        z = xyz[2]
        p.resetDebugVisualizerCamera(cameraYaw=cam[8], cameraPitch=cam[9], cameraDistance=cam[10],
                                     cameraTargetPosition=[x, y, z])
    if keys.get(65295):  # Left Arrow
        xyz = cam[11]
        x = xyz[0]
        y = float(xyz[1]) + 0.125
        z = xyz[2]
        p.resetDebugVisualizerCamera(cameraYaw=cam[8], cameraPitch=cam[9], cameraDistance=cam[10],
                                     cameraTargetPosition=[x, y, z])
    if keys.get(65296):  # Right arrow
        xyz = cam[11]
        x = xyz[0]
        y = float(xyz[1]) - 0.125
        z = xyz[2]
        p.resetDebugVisualizerCamera(cameraYaw=cam[8], cameraPitch=cam[9], cameraDistance=cam[10],
                                     cameraTargetPosition=[x, y, z])

    if keys.get(112): # O
        xyz = cam[11]
        x = xyz[0]
        y = float(xyz[1])
        z = xyz[2]+ 0.125
        p.resetDebugVisualizerCamera(cameraYaw=cam[8], cameraPitch=cam[9], cameraDistance=cam[10],
                                     cameraTargetPosition=[x, y, z])

    if keys.get(111):  # P
        xyz = cam[11]
        x = xyz[0]
        y = float(xyz[1])
        z = xyz[2]- 0.125
        p.resetDebugVisualizerCamera(cameraYaw=cam[8], cameraPitch=cam[9], cameraDistance=cam[10],
                                     cameraTargetPosition=[x, y, z])

def model_3BP(state, t):
    # Gravitational parameters
    mu_earth = 398600.0  # Earth's gravitational parameter in km^3/s^2
    mu_moon = 398600.0  # Moon's gravitational parameter in km^3/s^2

    x, y, z, vx, vy, vz = state
    r_earth = np.sqrt(x**2 + y**2 + z**2)
    r_moon = np.sqrt((x - 384)**2 + y**2 + z**2)  # Assuming Moon is at (384400, 0, 0)

    # Gravitational forces
    F_earth = -mu_earth / r_earth**3 * np.array([x, y, z])
    F_moon = -mu_moon / r_moon**3 * np.array([x - 384, y, z])  # Adjust for Moon's position

    # Equations of motion
    x_dot = vx
    y_dot = vy
    z_dot = vz
    vx_dot = F_earth[0] + F_moon[0]
    vy_dot = F_earth[1] + F_moon[1]
    vz_dot = F_earth[2] + F_moon[2]

    return [x_dot, y_dot, z_dot, vx_dot, vy_dot, vz_dot]

def kep_2_cart(mu, a,e,i,omega_AP,omega_LAN, MA):
    import math
    from scipy import optimize
    # n = np.sqrt(mu/(a**3))
    # T = 2*math.pi*math.sqrt((a**3)/132712440018000000000)
    def f(x):
        EA_rad = x - (e * math.sin(x)) - math.radians(MA)
        return EA_rad
    EA = math.degrees(optimize.newton(f, 1))

    nu = 2*np.arctan(np.sqrt((1+e)/(1-e)) * np.tan(math.radians(EA)/2))
    r = a*(1 - e*np.cos(math.radians(EA)))

    h = np.sqrt(mu*a * (1 - e**2))

    X = r*(np.cos(math.radians(omega_LAN))*np.cos(math.radians(omega_AP)+nu) - np.sin(math.radians(omega_LAN))*np.sin(math.radians(omega_AP)+nu)*np.cos(math.radians(i)))
    Y = r*(np.sin(math.radians(omega_LAN))*np.cos(math.radians(omega_AP)+nu) + np.cos(math.radians(omega_LAN))*np.sin(math.radians(omega_AP)+nu)*np.cos(math.radians(i)))
    Z = r*(np.sin(math.radians(i))*np.sin(math.radians(omega_AP)+nu))

    p = a*(1-e**2)

    V_X = (X*h*e/(r*p))*np.sin(nu) - (h/r)*(np.cos(omega_LAN)*np.sin(omega_AP+nu) + \
    np.sin(omega_LAN)*np.cos(omega_AP+nu)*np.cos(i))
    V_Y = (Y*h*e/(r*p))*np.sin(nu) - (h/r)*(np.sin(omega_LAN)*np.sin(omega_AP+nu) - \
    np.cos(omega_LAN)*np.cos(omega_AP+nu)*np.cos(i))
    V_Z = (Z*h*e/(r*p))*np.sin(nu) + (h/r)*(np.cos(omega_AP+nu)*np.sin(i))

    return [X,Y,Z],[V_X,V_Y,V_Z]

physicsClient = p.connect(p.GUI, options='--background_color_red=0.0 --background_color_green=0.0 --background_color_blue=0.0')
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

toc = 0         # Initialize timers
tic = 0

ballPosition = [0, 0, 0]  # [x, y, z]
ballOrientation = p.getQuaternionFromEuler([0, 0, 0])  # No rotation
radius = 25
ballVisualShapeId = p.createVisualShape(shapeType=p.GEOM_SPHERE, radius=radius)
ballMass = 1.0
ballCollisionShapeId = p.createCollisionShape(shapeType=p.GEOM_SPHERE, radius=radius)
ballId = p.createMultiBody(baseMass=ballMass, baseCollisionShapeIndex=ballCollisionShapeId,
                           baseVisualShapeIndex=ballVisualShapeId, basePosition=ballPosition,
                           baseOrientation=ballOrientation)
p.changeVisualShape(ballId,linkIndex=-1, rgbaColor=[0.3,0,1,1])

ball2Position = [384, 0, 0]  # [x, y, z]
ball2Orientation = p.getQuaternionFromEuler([0, 0, 0])  # No rotation
radius = 25
ball2VisualShapeId = p.createVisualShape(shapeType=p.GEOM_SPHERE, radius=radius)
ball2Mass = 1.0
ball2CollisionShapeId = p.createCollisionShape(shapeType=p.GEOM_SPHERE, radius=radius)
ball2Id = p.createMultiBody(baseMass=ball2Mass, baseCollisionShapeIndex=ball2CollisionShapeId,
                           baseVisualShapeIndex=ball2VisualShapeId, basePosition=ball2Position,
                           baseOrientation=ball2Orientation)
p.changeVisualShape(ball2Id,linkIndex=-1, rgbaColor=[1,0,0,1])

p.resetDebugVisualizerCamera(cameraYaw=0, cameraPitch=0, cameraDistance=600,
                             cameraTargetPosition=[384/2, 0, 0])
scaleFact = 0.051
initialized = 0
while True:
    getKeysPressed2()
    # Draw a debug line in PyBullet between consecutive trajectory points
    # p.resetBasePositionAndOrientation(spacecraft_id, line_to, [0, 0, 0, 1])
    if initialized == 0:
        # x,y,z = kep_2_cart(398600,384,0.5,45,0,0,0)[0]
        # vx, vy, vz = kep_2_cart(398600,384,0.5,45,0,0,0)[1]
        x,y,z = 384,90,0
        vx,vy,vz = 0,0,90
        thetax = 0
        thetay = 0
        thetaz = 0
        wx = 0
        wy = 0
        wz = 0

        state_vec1 = np.array([[x, y, z], [vx, vy, vz], [thetax, thetay, thetaz], [wx, wy, wz]])
        initialized = 1
        sol = odeint(model_3BP, np.array([x, y, z, vx, vy, vz]), [tic, toc + scaleFact])
        line_from = [x,y,z]
    else:

        sol = odeint(model_3BP, np.array([x[-1], y[-1], z[-1], vx[-1], vy[-1], vz[-1]]), [tic, toc + scaleFact])
        line_from = [x[-1],y[-1],z[-1]]

    x = sol[:, 0]  # X-coord [m] of satellite over time interval
    y = sol[:, 1]  # Y-coord [m] of satellite over time interval
    z = sol[:, 2]  # Z-coord [m] of satellite over time interval
    vx = sol[:, 3]
    vy = sol[:, 4]
    vz = sol[:, 5]

    line_to = [x[-1],y[-1],z[-1]]
    line_color = [1, 0, 0]  # Red color (Red, Green, Blue)/1
    line_width = 2.0
    debug_line_id = p.addUserDebugLine(lineFromXYZ=line_from,
                                       lineToXYZ=line_to,
                                       lineColorRGB=line_color,
                                       lineWidth=line_width,
                                       lifeTime = 0, # Seconds
                                       physicsClientId=physicsClient)
    time.sleep(0.1)
