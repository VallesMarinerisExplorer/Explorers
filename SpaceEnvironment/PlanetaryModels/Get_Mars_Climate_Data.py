from bs4 import BeautifulSoup
import warnings
import requests

# This file uses the web interface of the Mars Climate Database to get temperature, pressure, density and wind (and also can get dust info probably) for Mars based
# on the Mars Climate Model used/created by Laboratoire de Météorologie Dynamique.

# Credit Laboratoire de Météorologie Dynamique
# See https://www-mars.lmd.jussieu.fr/mars/mcd_training/  for more details on this model

year = 2020
month = 2
day = 10
hrs = 1
mins = 1
sec = 1
warnings.filterwarnings("ignore")
url ="http://www-alternate-mars.lmd.jussieu.fr/mcd_python/cgi-bin/mcdcgi.py?var1=t&var2=p&var3=rho&var4=wind&datekeyhtml=1&ls=10.6&localtime=9.&latitude=all&longitude=all&altitude=10.&zkey=3&spacecraft=none&isfixedlt=off&dust=1&hrkey=1&averaging=off&dpi=80&islog=off&colorm=jet&minval=&maxval=&proj=cyl&palt=&plon=&plat=&trans=&iswind=off&latpoint=&lonpoint="
r = requests.get(url)
soup = BeautifulSoup(r.text)

for a in soup.find_all('a', href=True):
    link = "http://www-alternate-mars.lmd.jussieu.fr/mcd_python" + a['href'][2:]
print(link)
response = requests.get(link)
name = str(year) +"_" + str(month) + "_" + str(day) + str(hrs) + "_" + str(mins) + "_" + str(sec) + ".txt"
if response.status_code == 200:
    with open(name + ".txt", "w") as file:
        file.write(response.text)
        print("File downloaded successfully.")
else:
    print("Failed to download the file.")
