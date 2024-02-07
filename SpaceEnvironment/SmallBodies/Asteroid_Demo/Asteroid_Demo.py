#************* This demo Asteroid is scaled with 1 being maximum value I believe ***************************************
# ********************** so it is not to scale, just for demonstration *************************************************

import time
import pandas as pd

import sqlite3
import os
import aiosqlite
import asyncio
from lxml import html
import cloudscraper
import PySimpleGUI as sg
import pybullet as p


# Credit for asteroid models goes to Greg Frieger
# 3d asteroids
# https://3d-asteroids.space/asteroids/

# In order to run this code you will need to get NASA's Small Bodies Database. It is big. It has 1.3M+ entries, so you
# will have to go to this website and download it based on what you want https://ssd.jpl.nasa.gov/tools/sbdb_query.html.
# For this program to display asteroids and run quickly each time, this "sbdb_query_results.csv" is turned into a
# sqlite database so that the lookup function can run faster. It will initialize the first time you run it but after
# that should run much faster each time.

# Download all columns or you can also edit the code below to remove the parameters you don't want.

print("Loading database")

df = pd.read_csv('sbdb_query_results.csv', delimiter=',')
pd.set_option('display.max_columns', None)

choices =df['name'].apply(str)
input_width = 20
num_items_to_show = 4

layout = [
    [sg.Text('Select Asteroid:')],
    [sg.Input(size=(input_width, 1), enable_events=True, key='-IN-')],
    [sg.pin(sg.Col(
        [[sg.Listbox(values=[], size=(input_width, num_items_to_show), enable_events=True, key='-BOX-',
                     select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, no_scrollbar=True)]],
        key='-BOX-CONTAINER-', pad=(0, 0), visible=False))],
    [sg.Submit(tooltip='Submit'), sg.Cancel()]
]

window2 = sg.Window('AutoComplete', layout, return_keyboard_events=True, finalize=True,
                    font=('Helvetica', 16))

list_element: sg.Listbox = window2.Element(
    '-BOX-')  # store listbox element for easier access and to get to docstrings
prediction_list, input_text, sel_item = [], "", 0

while True:  # Event Loop
    event2, values = window2.read()
    if event2 == sg.WINDOW_CLOSED:
        break
    # pressing down arrow will trigger event -IN- then aftewards event Down:40
    elif event2.startswith('Escape'):
        window2['-IN-'].update('')
        window2['-BOX-CONTAINER-'].update(visible=False)
    elif event2.startswith('Down') and len(prediction_list):
        sel_item = (sel_item + 1) % len(prediction_list)
        list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
    elif event2.startswith('Up') and len(prediction_list):
        sel_item = (sel_item + (len(prediction_list) - 1)) % len(prediction_list)
        list_element.update(set_to_index=sel_item, scroll_to_index=sel_item)
    elif event2 == '\r':
        if len(values['-BOX-']) > 0:
            window2['-IN-'].update(value=values['-BOX-'])
            window2['-BOX-CONTAINER-'].update(visible=False)
    elif event2 == '-IN-':
        text = values['-IN-'].lower()
        if text == input_text:
            continue
        else:
            input_text = text
        prediction_list = []
        if text:
            prediction_list = [item for item in choices if item.lower().startswith(text)]

        list_element.update(values=prediction_list)
        sel_item = 0

        list_element.update(set_to_index=sel_item)

        if len(prediction_list) > 0:
            window2['-BOX-CONTAINER-'].update(visible=True)
        else:
            window2['-BOX-CONTAINER-'].update(visible=False)
    elif event2 == '-BOX-':
        window2['-IN-'].update(value=values['-BOX-'])
        window2['-BOX-CONTAINER-'].update(visible=False)
    elif event2 == "Submit":
        Asteroid = values["-BOX-"][0]

        window2.close()
    elif event2 == "Cancel":
        window2.close()
window2.close()


if os.path.isfile("latest_fulldb.db") is False:
    print("Initializing the small-body database. This may take 10+ minutes for the first time.")
    db_conn = sqlite3.connect("latest_fulldb.db")
    latest_fulldb = pd.read_csv('sbdb_query_results.csv', header=0)

    c = db_conn.cursor()
    c.execute("""CREATE TABLE latest_fulldb(
                    id TEXT,
                    spkid INTEGER,
                    full_name TEXT,
                    pdes INTEGER,
                    name TEXT,
                    prefix TEXT,
                    neo TEXT,
                    pha TEXT,
                    H REAL,
                    G REAL,
                    M1 REAL,
                    M2 REAL,
                    K1 INTEGER,
                    K2 INTEGER,
                    PC REAL,
                    diameter REAL,
                    extent TEXT,
                    albedo REAL,
                    rot_per REAL,
                    GM REAL,
                    BV REAL,
                    UB REAL,
                    IR TEXT,
                    spec_B TEXT,
                    spec_T TEXT,
                    H_sigma REAL,
                    diameter_sigma REAL,
                    orbit_id INTEGER,
                    epoch INTEGER,
                    epoch_mjd INTEGER,
                    epoch_cal INTEGER,
                    equinox TEXT,
                    e REAL,
                    a REAL,
                    q REAL,
                    i REAL,
                    om REAL,
                    w REAL,
                    ma REAL,
                    ad REAL,
                    n REAL,
                    tp REAL,
                    tp_cal REAL,
                    per REAL,
                    per_y REAL,
                    moid REAL,
                    moid_ld REAL,
                    moid_jup REAL,
                    t_jup REAL,
                    sigma_e REAL,
                    sigma_a REAL,
                    sigma_q REAL,
                    sigma_i REAL,
                    sigma_om REAL,
                    sigma_w REAL,
                    sigma_ma REAL,
                    sigma_ad REAL,
                    sigma_n REAL,
                    sigma_tp REAL,
                    sigma_per REAL,
                    class TEXT,
                    producer TEXT,
                    data_arc INTEGER,
                    first_obs TEXT,
                    last_obs TEXT,
                    n_obs_used INTEGER,
                    n_del_obs_used INTEGER,
                    n_dop_obs_used INTEGER,
                    condition_code INTEGER,
                    rms REAL,
                    two_body TEXT,
                    A1 REAL,
                    A2 REAL,
                    A3 REAL,
                    DT TEXT);""")
    latest_fulldb.to_sql('latest_fulldb', db_conn, if_exists='append', index=False)

async def print_devices(query):
    async with aiosqlite.connect("latest_fulldb.db") as db:
        async with db.execute("SELECT * FROM latest_fulldb WHERE name=?", (query,)) as cursor:
            async for row in cursor:
                return row

print("Loading asteroid")

loop = asyncio.get_event_loop()
row = loop.run_until_complete(print_devices(Asteroid))
loop.close()

id = row[0]
spkid = row[1]
full_name = row[2]
pdes = row[3]
name = row[4]
prefix = row[5]
neo = row[6]
pha = row[7]
H = row[8]
G = row[9]
M1 = row[10]
M2 = row[11]
K1 = row[12]
K2 = row[13]
PC = row[14]
diameter = row[15]
extent = row[16]
albedo = row[17]
rot_per = row[18]
GM = row[19]
BV = row[20]
UB = row[21]
IR = row[22]
spec_B = row[23]
spec_T = row[24]
H_sigma = row[25]
diameter_sigma = row[26]

orbit_id = row[27]
epoch = row[28]
epoch_mjd = row[29]
epoch_cal = row[30]
equinox = row[31]
e = row[32]
a = row[33]
q = row[34]
i = row[35]
om = row[36]
w = row[37]
ma = row[38]
ad = row[39]
n = row[40]
tp = row[41]
tp_cal = row[42]
per = row[43]
per_y = row[44]
moid = row[45]
moid_ld = row[46]
moid_jup = row[47]
t_jup = row[48]
sigma_e = row[49]
sigma_a = row[50]
sigma_q = row[51]
sigma_i = row[52]
sigma_om = row[53]
sigma_w = row[54]
sigma_ma = row[55]
sigma_ad = row[56]
sigma_n = row[57]
sigma_tp = row[58]
sigma_per = row[59]
class1 = row[60]
producer = row[61]
data_arc = row[62]
first_obs = row[63]
last_obs = row[64]
n_obs_used = row[65]
n_del_obs_used = row[66]
n_dop_obs_used = row[67]
condition_code = row[68]
rms = row[69]
two_body = row[70]
A1 = row[71]
A2 = row[72]
A3 = row[73]
DT = row[74]

target_url = "https://3d-asteroids.space/asteroids/" + str(pdes) + "-" + str(name)
scraper = cloudscraper.create_scraper()
r = scraper.get(target_url).text
webpage = html.fromstring(r)
links = webpage.xpath('//a/@href')
for link in links:
    if link.find(".obj") > -1:
        objlink = link

r = scraper.get(objlink).text
text_file = open("Asteroid.obj", "wt")
n = text_file.write(r)
text_file.close()

urdfloc = "Asteroid.urdf"

gravity = 0
Atmosphere = 0

p.connect(p.GUI, options='--background_color_red=0 --background_color_green=0 --background_color_blue=0')

p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)
p.setRealTimeSimulation(1)
p.resetSimulation()

p.setGravity(0, 0, -gravity)

asteroid = p.loadURDF(urdfloc)

camerapitch = -40
camerayaw = 90


cameradist = 1
# cameradist = diameter*3 # If you did not download diameter data with the database you may get an error here
p.resetDebugVisualizerCamera(cameraDistance=cameradist, cameraYaw=camerayaw, cameraPitch=camerapitch,
                             cameraTargetPosition=[0,0,0])

while True:
    time.sleep(0.1)

