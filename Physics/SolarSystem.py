"""This simulation plots the position of the planets for you to see. It queries directly from Horizons and plots each
planetary position. There is a somewhat higher CPU load due to the update rate, which could be improved possibly with
using orbital elements instead or by decreasing the update rate. This is just meant as a proof of concept script."""

import time
import pybullet as p
import pybullet_data
from astroquery.jplhorizons import Horizons
import numpy as np

# Planets to track
planets = [199, 299, 399, 499, 599, 699, 799, 899, 999]

# Dictionary to store planet positions
planet_positions = {planet: [] for planet in planets}

# Time range
start_date = '2010-01-01'
end_date = '2010-06-01'
time_step = '1d'

# Query Horizons for each planet over the specified time range
for planet in planets:
    obj = Horizons(id=str(planet), epochs={'start': start_date, 'stop': end_date, 'step': time_step})
    planet_positions[planet] = list(zip(obj.vectors()["x"], obj.vectors()["y"], obj.vectors()["z"]))

physicsClient = p.connect(p.GUI, options='--background_color_red=0.0 --background_color_green=0.0 --background_color_blue=0.0')
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

# Generate random colors for each planet
planet_colors = {planet: np.random.rand(3) for planet in planets}
i = 0
while True:
    # Draw debug lines for each planet's orbit with assigned colors
    for planet in planets:
        positions = planet_positions[planet]
        color = planet_colors[planet]
        # for i in range(len(positions) - 1):
        line_from = positions[i]
        line_to = positions[i + 1]
        debug_line_id = p.addUserDebugLine(lineFromXYZ=line_from,
                                           lineToXYZ=line_to,
                                           lineColorRGB=color,
                                           lineWidth=2.0,
                                           lifeTime=0,  # Permanent lines
                                           physicsClientId=physicsClient)
    i+=1
    time.sleep(0.1)

