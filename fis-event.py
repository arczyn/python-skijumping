import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
sprawdzany_link = "https://www.fis-ski.com/DB/general/results.html?sectorcode=JP&raceid=6453" #strona z wynikami konkursu

sprawdzana_odpowiedz = requests.get(sprawdzany_link)
sprawdzany_html = sprawdzana_odpowiedz.text
sprawdzana_soup = BeautifulSoup(sprawdzany_html, 'html.parser')
konkurs_data = sprawdzana_soup.find("span", class_ = "date__full").string
konkurs_data = datetime.strptime(konkurs_data, "%B %d, %Y")
konkurs_name = sprawdzana_soup.find("div", class_ = "event-header__subtitle").string
konkurs_skocznia = sprawdzana_soup.find("h1", class_ = "heading heading_l2 heading_white heading_off-sm-style").string
konkurs_typ = sprawdzana_soup.find("div", class_ = "event-header__kind").string.strip()
konkurs_typ = re.sub("\W{2,}", " ", konkurs_typ)

konkurs_tabela = []
konkurs_wyniki = sprawdzana_soup.find("div", id="events-info-results")
skoczkowie_wyniki = konkurs_wyniki.find_all("div", class_="g-row justify-sb")
for skoczek in range(len(skoczkowie_wyniki)):
    skoczek_miejsce = int(skoczkowie_wyniki[skoczek].find("div", class_ = "g-lg-1 g-md-1 g-sm-1 g-xs-2 justify-right pr-1 bold").string)
    skoczek_numer = int(skoczkowie_wyniki[skoczek].find("div", class_ = "g-lg-1 g-md-1 g-sm-1 justify-right hidden-xs pr-1 gray").string)
    skoczek_fiscode = int(skoczkowie_wyniki[skoczek].find("div", class_ = "g-lg-2 g-md-2 g-sm-2 hidden-xs justify-right gray pr-1").string)
    skoczek_athlete = skoczkowie_wyniki[skoczek].find("div", class_ = "g-lg g-md g-sm g-xs justify-left bold").string.strip()
    skoczek_totalnota = float(skoczkowie_wyniki[skoczek].find("div", class_ = "g-lg-2 g-md-2 g-sm-3 g-xs-5 justify-right blue bold hidden-sm hidden-xs").string)
    skoczek_kompletny_wpis = []
    skoczek_kompletny_wpis.append(skoczek_miejsce)
    skoczek_kompletny_wpis.append(skoczek_numer)
    skoczek_kompletny_wpis.append(skoczek_fiscode)
    skoczek_kompletny_wpis.append(skoczek_athlete)
    skoczek_kompletny_wpis.append(skoczek_totalnota)
    konkurs_tabela.append(skoczek_kompletny_wpis)

konkurs_filename = konkurs_name + " " + konkurs_data.strftime("%Y-%m-%d") + " " + konkurs_skocznia + " " + konkurs_typ + ".csv"

df = pd.DataFrame(konkurs_tabela, columns =['Miejsce', 'Numer startowy', "FIS Code", "Zawodnik", "Nota"])
df.to_csv(konkurs_filename, index=False, sep=';')
