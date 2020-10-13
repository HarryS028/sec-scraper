import pandas as pd
from bs4 import BeautifulSoup
import requests

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\ Chrome/80.0.3987.87 Safari/537.36"

headers = {"user_agent" : USER_AGENT}
url = "https://www.sec.gov/Archives/edgar/data/1524472/000152447220000006/xyl1231201910kv1_htm.xml"

request = requests.get(url, headers=headers).content
soup = BeautifulSoup(request, 'xml')

company = "Xylem"

tags = ["us-gaap:Revenues", "us-gaap:CostOfRevenue", "us-gaap:CostOfRevenue", "us-gaap:GrossProfit", "us-gaap:ProfitLoss", "us-gaap:Depreciation", "us-gaap:Assets"]

main_df = pd.DataFrame(columns=['metric', 'contextRef', 'decimals', 'id', 'unitRef', 'value', 'company'])
for tag in tags:
    test = soup.find_all(tag, {"contextRef": "FD2019Q4YTD"})

    dict_list = []

    for t in test:
        context = t.attrs
        context['value'] = t.text
        context['company'] = company
        context['metric'] = tag
        dict_list.append(context)

    df = pd.DataFrame(dict_list)
    df.drop_duplicates(subset=['contextRef', 'value', 'company'], inplace=True)
    main_df = main_df.append(df)

# for tag in tags:
#     items = soup.find_all(tag)
#     for item in items:
#         context = item.find('contextRef')
print(main_df)
#print(main_df)
# with open ("Output_xyl.xml", "w") as text_file:
#     text_file.write(str(soup))