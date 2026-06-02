from bs4 import BeautifulSoup
import pandas as pd
import requests

url="https://en.wikipedia.org/wiki/Main_Page"
soup = BeautifulSoup(requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text, "html.parser")


#  #   recuperation de tout les balises uniques de la page et les stocker dans une liste trié pas ordre alphabetique 
balise= soup.find_all() #pour trouver les balises uniques
vus = set()
for ui in balise:
    
        vus.add(ui.name)
        
liste_of_tages_h=[]
for i in vus:
        if i.startswith("h") and i[1].isnumeric():
            liste_of_tages_h.append(i)
# print(sorted(vus))

hearders= soup.find_all(liste_of_tages_h)
for i in hearders:
    print(i.text.strip()) #strip() pour enlever les espaces avant et après le texte