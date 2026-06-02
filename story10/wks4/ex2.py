from bs4 import BeautifulSoup

import requests


url="https://data.gov/"

response=requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

soup = BeautifulSoup(response.text, "html.parser")

print((soup.find_all("span", class_="text-color-red"))[0].text)