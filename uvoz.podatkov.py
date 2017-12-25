import re
import requests
import csv
import os


hoteli_url = "https://www.booking.com/searchresults.sl.html?country=si;offset="
hoteli_directory = "podatki"

def shrani_text(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    pot = os.path.join(directory, filename)
    with open(pot, 'w', encoding = 'utf-8') as mapa:
        mapa.write(text)
    return None



def download_url(url):
    s=1
    for i in range(0,2):
        a = i*15
        datoteka  = requests.get(url + str(a))
        datoteka_text = datoteka.text
        datoteka_ime = "hoteli{}.html".format(str(s))
        shrani_text(datoteka_text, hoteli_directory, datoteka_ime )
        s+=1
    return None


        
