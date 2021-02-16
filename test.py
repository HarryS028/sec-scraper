import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import urllib
from urllib import request

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\ Chrome/80.0.3987.87 Safari/537.36"

headers = {"user_agent" : USER_AGENT}
url = "https://uk.reuters.com/companies/UU.L/financials/income-statement-annual"

request = requests.get(url, headers=headers)
test = request.json()
# soup = BeautifulSoup(request, 'html.parser')

# head = soup.find('thead').find('tr').find_all('th')

# for h in head:
#     print(h.innerHTML)

# print(head)

# resp = request.urlopen(url)
# data = resp.read()
# html = data.decode("UTF-8")
# soup = BeautifulSoup(html, 'html.parser')
# soup = str(soup.encode('UTF-8'))

# with open("output.txt", "w") as text_file:
#     text_file.write(soup)

# html = resp.decode("UTF-8")
# soup2 = BeautifulSoup(html, 'html.parser')

# head2 = soup.find('thead').find('tr').find_all('th')

print(test)

