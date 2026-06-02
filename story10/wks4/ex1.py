from bs4 import BeautifulSoup
import pandas as pd
import requests


url="https://fr.wikipedia.org/robots.txt"

response=requests.get(url, headers={"User-Agent": "Mozilla/5.0"})



print(response.text)

