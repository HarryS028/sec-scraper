import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\ Chrome/80.0.3987.87 Safari/537.36"

headers = {"user_agent" : USER_AGENT}
#url = "https://www.sec.gov/Archives/edgar/data/868857/000110465919063367/acm-20190930x10k94a79f_htm.xml"
url = "https://www.sec.gov/Archives/edgar/data/1524472/000152447219000009/xyl1231201810k_htm.xml"

request = requests.get(url, headers=headers).content
soup = BeautifulSoup(request, 'xml')

pattern = re.compile('^.+2019.+$')
output = soup.find_all("us-gaap:Revenues", {"contextRef": ["FD2018Q4YTD", "FD2019Q4YTD"]})

if not output:
    output = soup.find_all("us-gaap:Revenues", {"contextRef": pattern})

print(output)