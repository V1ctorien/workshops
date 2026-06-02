from bs4 import BeautifulSoup
import pandas as pd
import requests
from lxml import html
from io import StringIO

url="https://x.com/ElonMusk"

response=requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

tree = html.parse(StringIO(response.text))

root = tree.getroot()

followers = root.xpath("//a[contains(@href, 'followers')]")
print(followers)
text = followers[0].xpath(".//span//text()")

print(text)

# followers = root.xpath("//*[contains(@class, 'css-1jxf684 r-bcqeeo r-1ttztb7 r-qvutc0 r-poiln3 r-1b43r93 r-1cwl3u0 r-b88u0q')]")
# print(followers)
# for follower in followers:
#     print(follower)





