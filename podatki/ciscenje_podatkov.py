import re
import requests

with open('statistika1.html') as datoteka:
    vsebina = datoteka.read()


vzorec = re.compile(
    'href="\/competition\/players\/showplayer\?pcode='
    '(?P<ID>\d+|[A-Z]+)'  #ID
    '&amp;seasoncode=E2016">\n\s+<span class="hidden-xs">'
    '(?P<Ime>[A-Z]+\s*[A-Z]*, [A-Z]+)'  #Priimek, Ime
    '.*\n+\s+.+<span class="visible-sm-inline">'
    '(?P<Klub>\w+ \w+)'  #Klub
    )

s=0
for ujemanje in vzorec.finditer(vsebina):
    podatki = ujemanje.groupdict()
    s+=1
    dodatni_podatki = requests.get('http://www.euroleague.net/competition/players/showplayer?pcode={}&seasoncode=E2016'.format(podatki['ID']))

    print(podatki['Ime'], dodatni_podatki.status_code)
    if s>10:
        break

    
