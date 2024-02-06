import pybullet as p
import time
import pybullet_data
import numpy as np
from scipy.integrate import odeint

"""This script demonstrates simple orbit propagation. You can move the camera using the arrow keys, O and P and also by
pressing ctrl + mouse click to pan around. It uses odeint from scipy for the integrator. Kep_2_cart converts keplerian
elements to cartesian so you can easily define and initialize your orbit using gravitational parameter, semi-major axis,
eccentricity, inclination, arguement of Periapsis, longitude of the ascending node and mean anomaly. You can adjust the
time scaling using the scalefactor parameter, i.e. increasing this makes time go faster"""

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

def model_2BP(state, t, Fx, Fy, Fz):
    # mu = 1.32712440018e20 # Sun's grav parameter
    mu = 10000000   # The value for the Earth is probably much bigger than this
    x = state[0]
    y = state[1]
    z = state[2]

    x_dot = state[3]
    y_dot = state[4]
    z_dot = state[5]
    m = 1000   # Spacecraft Mass (kg)

    rocketaccelx = Fx/m
    rocketaccely = Fy/m
    rocketaccelz = Fz/m

    x_ddot = -mu * x / (x ** 2 + y ** 2 + z ** 2) ** (3 / 2) + rocketaccelx
    y_ddot = -mu * y / (x ** 2 + y ** 2 + z ** 2) ** (3 / 2) + rocketaccely
    z_ddot = -mu * z / (x ** 2 + y ** 2 + z ** 2) ** (3 / 2) + rocketaccelz
    dstate_dt = [x_dot, y_dot, z_dot, x_ddot, y_ddot, z_ddot]
    return dstate_dt

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
radius = 0.5
ballVisualShapeId = p.createVisualShape(shapeType=p.GEOM_SPHERE, radius=radius)
ballMass = 1.0
ballCollisionShapeId = p.createCollisionShape(shapeType=p.GEOM_SPHERE, radius=radius)
ballId = p.createMultiBody(baseMass=ballMass, baseCollisionShapeIndex=ballCollisionShapeId,
                           baseVisualShapeIndex=ballVisualShapeId, basePosition=ballPosition,
                           baseOrientation=ballOrientation)
p.changeVisualShape(ballId,linkIndex=-1, rgbaColor=[0.3,0,1,1])


scaleFact = 0.0005
initialized = 0
while True:
    getKeysPressed2()
    # Draw a debug line in PyBullet between consecutive trajectory points
    # p.resetBasePositionAndOrientation(spacecraft_id, line_to, [0, 0, 0, 1])
    if initialized == 0:
        x,y,z = kep_2_cart(398600,100,0.5,45,0,0,0)[0]
        vx, vy, vz = kep_2_cart(398600,100,0.5,45,0,0,0)[1]
        thetax = 0
        thetay = 0
        thetaz = 0
        wx = 0
        wy = 0
        wz = 0

        state_vec1 = np.array([[x, y, z], [vx, vy, vz], [thetax, thetay, thetaz], [wx, wy, wz]])
        initialized = 1
        sol = odeint(model_2BP, np.array([x, y, z, vx, vy, vz]), [tic, toc + scaleFact],
                     (0,0,0))
        line_from = [x,y,z]
    else:

        sol = odeint(model_2BP, np.array([x[-1],y[-1],z[-1],vx[-1],vy[-1],vz[-1]]), [tic,toc+ scaleFact],(0,0,0))
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
                                       lifeTime = 4, # Seconds
                                       physicsClientId=physicsClient)
    time.sleep(0.1)
