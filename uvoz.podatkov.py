import re
import requests
import csv
import os


hoteli_url = "https://www.booking.com/searchresults.sl.html?aid=309654&label=hotels-slovenian-sl-aaFjqS2XX3ZQOPQP42zhGAS95119537132%3Apl%3Ata%3Ap1%3Ap21.577.000%3Aac%3Aap1t1%3Aneg%3Afi%3Atikwd-70520048%3Alp1007614%3Ali%3Adec%3Adm&sid=36e623017a248d4165fac0110a20f8e0&checkin_month=4&checkin_monthday=18&checkin_year=2018&checkout_month=4&checkout_monthday=19&checkout_year=2018&class_interval=1&dest_id=192&dest_type=country&dtdisc=0&from_sf=1&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&oos_flag=0&order=review_score_and_price&postcard=0&raw_dest_type=country&room1=A%2CA&sb_price_type=total&src=searchresults&src_elem=sb&ss=Slovenija&ss_all=0&ssb=empty&sshis=0&ssne=Slovenija&ssne_untouched=Slovenija&rows=15&offset="
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


        
