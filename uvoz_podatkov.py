import requests
import os


nba_url = "http://www.espn.com/nba/statistics/player/_/stat/scoring-per-game/sort/avgPoints/count/"
nba_directory = "podatki"

def shrani_text(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    pot = os.path.join(directory, filename)
    with open(pot, 'w', encoding = 'utf-8') as mapa:
        mapa.write(text)
    return None



def download_url(url):
    s=1
    for i in range(0,8):
        a= i*40 + 1
        datoteka  = requests.get(url + str(a))
        datoteka_text = datoteka.text
        datoteka_ime = "statistika{}.html".format(str(s))
        shrani_text(datoteka_text, nba_directory, datoteka_ime )
        s+=1
    return None
