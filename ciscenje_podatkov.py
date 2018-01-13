import re
import requests
import os
import json
import csv

euroliga_url = "http://www.euroleague.net/main/statistics?mode=Leaders&entity=Players&seasonmode=Single&seasoncode=E2016&cat=Valuation&agg=Accumulated&page="
euroliga_directory = "statistika"


#program, ki shrani text v datoteko                
def shrani_text(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    pot = os.path.join(directory, filename)
    with open(pot, 'w', encoding = 'utf-8') as mapa:
        mapa.write(text)
    return None


#osnovni podatki
def download_url(url):
    s=1
    for i in range(1,6):
        datoteka  = requests.get(url + str(i))
        datoteka_text = datoteka.text
        datoteka_ime = "statistika{}.html".format(str(s))
        shrani_text(datoteka_text, euroliga_directory, datoteka_ime )
        s+=1
    return None

#vzorec osnovnih podatkov
osnovni_vzorec = re.compile(
    'href="\/competition\/players\/showplayer\?pcode='
    '(?P<ID>.+)'  #ID
    '&amp;seasoncode=E2016">\n\s+<span class="hidden-xs">'
    '(?P<Ime>.+, .+)'  #Priimek, Ime
    '<\/span><span class="visible-xs">.*\n\s+.*\n*\s*.*visible-lg-inline">'
    '(?P<Klub>.*)'
    '(visible-sm-inline">)?'
    '.*?'
    '<\/span><\/a>'
    )


#vzorec za igralca
igralec_vzorec = re.compile(
        '<div class="name">'
        '(?P<Ime>.+, .+)'  #Ime
        '<\/div>\n\s+.+\n\s+.+\n\s+.+\n\s+.+\n\s+.+\n\s+.+'
        '\n\s+.+\n\s+.+\n\s+.+\n\s+.+\n\s+.+\n\s+.+\n\s+.+\n\s+.+\n\s+'
        '<div class="summary-second">\s+(<span>Height:\s)?'
        '(?P<Visina>\d\.\d+)?'  #Visina
        '.+\s+.+'
        '(?P<Letnica_rojstva>\d\d\d\d)' #Letnica
        '.+\n\s+<span>Nationality:\s'
        '(?P<Nacionalnost>.+)'  #Nacionalnost
        '<\/span>'
        )


 #vzorec za statistiko igralca
statistika_vzorec = re.compile(
        '<td class="PlayerTitleColumn">Averages<\/td>\n\s+<td>'
        '(?P<G>\d+)'  #G
        '<\/td>\n\s+<td>'
        '(?P<GS>\d+)'  #GS
        '<\/td>\n\s+<td>'
        '(?P<Min>\d+):\d+'  #Min
        '<\/td>\n\s+<td>'
        '(?P<Tocke>\d+\.?\d*)'  #Tocke
        '<\/td>\n\s+<td>'
        '(?P<DvaFG>\d+\.?\d*)%'  #2FG
        '<\/td>\n\s+<td>'
        '(?P<TriFG>\d*\.?\d+)%'  #3FG
        '<\/td>\n\s+<td>'
        '(?P<FT>\d*\.?\d+)%'  #FT
        '<\/td>'
    )
    
#imenik = 'statistika'
def seznam_iz_podatkov(imenik, vzorec):
    a=0
    sez=[]
    for ime_datoteke in os.listdir(imenik):
        pot = os.path.join(imenik, ime_datoteke)
        with open(pot, encoding = 'utf-8') as datoteka:
            vsebina = datoteka.read()
        for ujemanje in vzorec.finditer(vsebina):
            podatki = ujemanje.groupdict()
            sez.append(podatki)
            a+=1
        print(a)
    return sez

seznam_podatkov = seznam_iz_podatkov('statistika', osnovni_vzorec)

def download_igralci(podatki):
    dolzina = len(podatki)
    for i in range(0, dolzina):
        ID=podatki[i]['ID']
        igralec_url = 'http://www.euroleague.net/competition/players/showplayer?pcode={}&seasoncode=E2016'.format(str(ID))
        stran = requests.get(igralec_url)
        text = stran.text
        datoteka_ime = 'igralec{}.html'.format(str(ID))
        shrani_text(text, 'igralci', datoteka_ime)
        

    return None

seznam_igralci = seznam_iz_podatkov('igralci', igralec_vzorec)
seznam_statistika = seznam_iz_podatkov('igralci', statistika_vzorec)

def sestavi_slovarje(seznam1, seznam2):
    dolzina = len(seznam1)
    for i in range(0, dolzina):
        seznam1[i].update(seznam2[i])
    return seznam1


#ker je pri seznamih seznam_igralcev in seznam_statistika enako zaporedje slovarjev,
#lahko uporabimo funkcijo setavi_slovarje
slovar = sestavi_slovarje(seznam_igralci, seznam_statistika)


#funkcija, ki bo spojila skupaj dva seznama slovarjev, ki imata enak ključ
def merge_lists(slovar1, slovar2, key):
    merged = {}
    for item in slovar1+slovar2:
        if item[key] in merged:
            merged[item[key]].update(item)
        else:
            merged[item[key]] = item
    return [val for (_, val) in merged.items()]


seznam = merge_lists(seznam_podatkov, slovar, 'Ime')
for i in range(0, 242):
    seznam[i]['Ime'] = seznam[i]['Ime'].replace(',', '')

def zapisi_json(podatki, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        json.dump(podatki, datoteka, indent=2)


imena = [
    'ID',
    'Ime',
    'Nacionalnost',
    'Letnica_rojstva',
    'Visina',
    'Klub',
    'G',
    'GS',
    'Min',
    'Tocke',
    'DvaFG',
    'TriFG',
    'FT'
    ]

def zapisi_csv(podatki, polja, ime_datoteke):
    with open(ime_datoteke, 'w') as datoteka:
        pisalec = csv.DictWriter(datoteka, polja, extrasaction='ignore')
        pisalec.writeheader()
        for podatek in podatki:
            pisalec.writerow(podatek)
    


