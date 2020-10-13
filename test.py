import pandas as pd
from bs4 import BeautifulSoup
import requests

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\ Chrome/80.0.3987.87 Safari/537.36"

headers = {"user_agent" : USER_AGENT}
url = "https://www.sec.gov/Archives/edgar/data/1524472/000152447220000006/xyl1231201910kv1_htm.xml"

request = requests.get(url, headers=headers).content
soup = BeautifulSoup(request, 'xml')

#print(soup)
with open ("Output_xyl.xml", "w") as text_file:
    text_file.write(str(soup))