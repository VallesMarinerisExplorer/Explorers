import wget
import PySimpleGUI as sg
from PIL import Image
#https://alasky.cds.unistra.fr/hips-image-services/hips2fits#projection=SIN&hips=CDS%2FP%2F2MASS%2Fcolor&ra=266.404995&dec=-28.936174&fov=58.6323
# fov = 3
# ra = 5.633083
# dec = 22.0145
sg.theme('black')
layout = [[sg.Text('Field of View (degrees)'), sg.InputText(size=(10, 8))],
 [sg.Text('Right Ascension (degrees) -180 to 180'), sg.InputText(size=(10, 8))],
 [sg.Text('Declination (degrees -90 to 90)'), sg.InputText(size=(10, 8))],
          [sg.Submit()]]

window = sg.Window('Virtual Telescope', layout, finalize=True)
while True:
    event, values = window.read()

    if event in (None,):
        window.close()
        break
    elif event == 'Submit':
        fov = float(values[0])
        ra = float(values[1])
        dec = float(values[2])
        url = "https://alasky.u-strasbg.fr/hips-image-services/hips2fits?hips=CDS%2FP%2F2MASS%2Fcolor&width=2400&height=2400&fov=" + str(fov) + "&projection=SIN&coordsys=icrs&rotation_angle=0.0&ra=" + str(ra) + "&dec=" + str(dec) + "&format=jpg"
        filename = wget.download(url)
        image = Image.open(filename)
        image.show()
        window.close()

