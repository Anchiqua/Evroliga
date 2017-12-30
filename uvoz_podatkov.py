import requests
import os


euroliga_url = "http://www.euroleague.net/main/statistics?mode=Leaders&entity=Players&seasonmode=Single&seasoncode=E2016&cat=Valuation&agg=Accumulated&page="
euroliga_directory = "statistika"

def shrani_text(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    pot = os.path.join(directory, filename)
    with open(pot, 'w', encoding = 'utf-8') as mapa:
        mapa.write(text)
    return None



def download_url(url):
    s=1
    for i in range(1,6):
        datoteka  = requests.get(url + str(i))
        datoteka_text = datoteka.text
        datoteka_ime = "statistika{}.html".format(str(s))
        shrani_text(datoteka_text, euroliga_directory, datoteka_ime )
        s+=1
    return None
