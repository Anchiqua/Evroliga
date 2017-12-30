
import re
import requests
import os


vzorec = re.compile(
    'href="\/competition\/players\/showplayer\?pcode='
    '(?P<ID>\d+|[A-Z]+)'  #ID
    '&amp;seasoncode=E2016">\n\s+<span class="hidden-xs">'
    '(?P<Ime>[A-Z]+\s*[A-Z]*, [A-Z]+)'  #Priimek, Ime
    '.*\n+\s+.+<span class="visible-sm-inline">'
    '(?P<Klub>\w+ \w+)'  #Klub
    )

igralec_vzorec = re.compile(
        r' <div class="summary-second">\n\s+<span>.*'
        r'(?P<Visina>\d\.\d+)'  #Visina
        r'.+\n\s+.+'
        r'(?P<Letnica_rojstva>\d\d\d\d)' #Letnica
        r'.+\n\s+<span>Nationality: '
        r'(?P<Nacionalnost>.+)'  #Nacionalnost
        r'</span>'
        r'.*'
        r'<td class="PlayerTitleColumn">Averages</td>\n\s+<td>'
        r'(?P<G>\d+)'  #G
        r'</td>\n\s+<td>'
        r'(?P<GS>\d+)'  #GS
        r'</td>\n\s+<td>'
        r'(?P<Min>\d+:\d+)'  #Min
        r'</td>\n\s+<td>'
        r'(?P<Tocke>\d+\.?\d*)'  #Tocke
        r'</td>\n\s+<td>'
        r'(?P<DvaFG>\d+\.?\d*%)'  #2FG
        r'</td>\n\s+<td>'
        r'(?P<TriFG>\d*\.?\d+%)'  #3FG
        r'</td>\n\s+<td>'
        r'(?P<FT>\d*\.?\d+%)'  #FT
        r'</td>',
        
        flags = re.DOTALL
        )
 
    
#imenik = 'statistika'
def seznam_iz_podatkov(imenik):
    sez=[]
    s=0
    for ime_datoteke in os.listdir(imenik):
        pot = os.path.join(imenik, ime_datoteke)
        with open(pot) as datoteka:
            vsebina = datoteka.read()
        for ujemanje in vzorec.finditer(vsebina):
            podatki = ujemanje.groupdict()
        #podatki['ID'] = int(podatki['ID'])
        #podatki['Ime'] = podatki['Ime'].strip()
            s+=1
            sez.append(podatki)
    
            if s>99:
                break
    return sez

seznam = seznam_iz_podatkov('statistika')

def igralci_seznam(podatki):
    a=0
    igralci_seznam = []
    dolzina= len(podatki)
    for i in range(0, dolzina+1):
            if a>1:
                break
            else:
                igralec_url = 'http://www.euroleague.net/competition/players/showplayer?pcode={}&seasoncode=E2016'.format(podatki[i]['ID'])
                stran = requests.get(igralec_url)
                text = stran.text
                najdi = igralec_vzorec.search(text)
                igralec = najdi.groupdict()
                igralci_seznam.append(igralec)
                a+=1    
    return igralci_seznam
