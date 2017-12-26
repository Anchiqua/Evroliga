import re
import requests

with open('statistika1.html') as datoteka:
    vsebina = datoteka.read()


vzorec = re.compile(
    '<a href="http:\/\/www.espn.com\/nba\/player\/_\/id\/'
    '(?P<ID>\d+)'  #ID
    '\/\w*.?\w*.?\w*">'
    '(?P<Ime>\w*.?\w*\s\w*)'  #Ime
    '<\/a>,\s'
    '(?P<Pozicija>[A-Z]+)'  #Pozicija
    '<\/td><td align="left">'
    '(?P<Klub>[A-Z]+.?[A-Z*])'  #Klub
    '<\/td><td >'
    '(?P<GP>\d*)'  #GP
    '<\/td><td >'
    '(?P<MPG>\d*\.\d)'  #MPG
    '<\/td><td\s+class="sortcell">'
    '(?P<PTS>\d+\.\d)'  #PTS
    '<\/td><td >'
    '(?P<FGM>\d+\.\d)'  #FGM
    '-'
    '(?P<FGA>\d+\.\d)'  #FGA
    '<\/td><td >'
    '(?P<FG>\.\d+)'  #FG%
    '<\/td><td >'
    '(?P<triPM>\d+\.\d)'  #3PM
    '-'
    '(?P<triPA>\d+\.\d)'  #3PA
    '<\/td><td >'
    '(?P<triP>\.\d+)'  #triP%
    '<\/td><td >'
    '(?P<FTM>\d+\.\d)'  #FTM
    '-'
    '(?P<FTA>\d+\.\d)'  #FTA
    '<\/td><td >'
    '(?P<FT>\.\d+)'  #FT%
    )

s=0
for ujemanje in vzorec.finditer(vsebina):
    podatki = ujemanje.groupdict()
    s+=1
    dodatni_podatki = requests.get('http://www.espn.com/nba/player/_/id/{}/{}'.format(podatki['ID'], podatki['Ime']))

    print(podatki['Ime'], dodatni_podatki.status_code)
    if s>10:
        break

    
