import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

def get_data(link, company):

    tags = ["us-gaap:Revenues", "us-gaap:CostOfRevenue", "us-gaap:CostOfRevenue", "us-gaap:GrossProfit", "us-gaap:ProfitLoss", "us-gaap:Depreciation", "us-gaap:Assets"]

    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\ Chrome/80.0.3987.87 Safari/537.36"

    headers = {"user_agent" : USER_AGENT}
    url = link

    request = requests.get(url, headers=headers).content
    soup = BeautifulSoup(request, 'xml')

    main_df = pd.DataFrame(columns=['metric', 'contextRef', 'decimals', 'id', 'unitRef', 'value', 'company'])
    for tag in tags:
        test = soup.find_all(tag, {"contextRef": ["FD2019Q4YTD","FD2018Q4YTD"]})

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


    return main_df

def main_func():

    df_out = pd.DataFrame(columns=['metric', 'contextRef', 'decimals', 'id', 'unitRef', 'value', 'company'])
    input_data = pd.read_excel('test_input.xlsx')
    for i in range(len(input_data['link'])):
        company = input_data['company'][i]
        link = input_data['link'][i]
        df = get_data(link, company)
        df_out = df_out.append(df)

    return df_out


print(main_func())