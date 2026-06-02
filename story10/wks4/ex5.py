from bs4 import BeautifulSoup
import pandas as pd
import requests

url="https://en.wikipedia.org/wiki/Elizabeth_II"
response=requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")
ok=soup.find(id="bodyContent")
im= ok.find_all("img")
for i in im:
    
    if any(mot in str(i) for mot in ["Elizabeth_II", "elizabeth_II","queen","Queen",'elizabeth','Elizabeth',"reine","Reine",'princess','Princess']):
        print(i["src"])




# print(.find_all("img")[0]["src"]) #pour trouver le lien de la premiere image de la page


