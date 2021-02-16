import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

def get_file(cik, doc_type, year):

    try:
        cik = str(cik)
        url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=" + cik + "&type=" + doc_type + "&owner=exclude"

        pd.set_option('max_colwidth',400)
        df = pd.read_html(url)[2]

        most_recent = df['Filing Date'][0]
        rec_year = re.search(r'\d{4}', most_recent).group()
        if year > rec_year:
            return "Financials not available for this year"

        search = df[df['Filing Date'].str.contains(year)]
        desc = search['Description'].to_string()
        acc_no = re.search(r'\d{10}-\d{2}-\d{6}', desc).group()
        acc_conc = acc_no.replace("-", "")
        #cik_short = acc_no[0:10].replace("0", "")
        strPattern = "^0+(?!$)"
        cik_short = cik.replace(strPattern, "")

        doc_page = "https://www.sec.gov/Archives/edgar/data/" + cik_short + "/" + acc_conc + "/" + acc_no + "-index.htm"

        df2 = pd.read_html(doc_page)[1]
        file_row = df2[df2['Type'].str.contains('EX-101.INS|XML')]
        file_s = file_row['Document'].to_string()
        file = re.search(r'\S+\.xml', file_s).group()

        address = "https://www.sec.gov/Archives/edgar/data/" + cik_short + "/" + acc_conc + "/" + file

        return address

    except:
        return "Financials not available for this year"

def gen_func(file_loc, year, doc_type):
    upload = pd.read_excel(file_loc)

    links_list = []
    for i in range(len(upload['CIK code'])):
        link = get_file(upload['CIK code'][i], doc_type, year)
        company = upload['Company name'][i]
        links_list.append({"link": link, "company": company})

    links_df = pd.DataFrame(links_list)
    output = links_df.to_excel('test_links.xlsx', encoding="UTF-16", index=False)

    return links_df

print(gen_func(r"C:\Users\Harry\Python\GWI_scrapers\SEC-scraper\CIK-codes-test.xlsx", "2019", "10-k"))
