from bs4 import BeautifulSoup
import pandas as pd
import requests


url="https://www.linkedin.com"

response=requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

soup = BeautifulSoup(response.text, "html.parser")

print((soup.find_all("h1",))[0].text.strip()) #strip() pour enlever les espaces avant et après le texte

#ou 

# print(soup.h1.text)