import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\ Chrome/80.0.3987.87 Safari/537.36"

headers = {"user_agent" : USER_AGENT}
url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001524472&owner=exclude"

request = requests.get(url, headers=headers).content
soup = BeautifulSoup(request, 'html.parser')

table = soup.find('table', {"summary": "Results"})
df = pd.read_html("https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001524472&owner=exclude")[2]

most_recent = df['Filing Date'][0]

print(most_recent)
