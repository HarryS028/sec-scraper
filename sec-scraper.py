import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from generate_links import gen_func
from gaap_tags import gaap_tags
from gaap_tags import map_df

def get_data(link, company, dates):

    tags = gaap_tags

    USER_AGENT = r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\ Chrome/80.0.3987.87 Safari/537.36"

    headers = {"user_agent" : USER_AGENT}
    url = link

    request = requests.get(url, headers=headers).content
    soup = BeautifulSoup(request, 'xml')

    main_df = pd.DataFrame(columns=['metric', 'contextRef', 'decimals', 'id', 'unitRef', 'value', 'company'])

    date_list = []

    for year in dates:
        date_list.append("FD"+ year + "Q4YTD")

    for tag in tags:
        test = soup.find_all(tag, {"contextRef": date_list})

        if not test:
            try:       
                test1 = [soup.find_all(tag, {"contextRef": re.compile('^.+' + dates[0] + '.+$')})[0]]
            except:
                test1 = []
            try:
                test2 = [soup.find_all(tag, {"contextRef": re.compile('^.+' + dates[1] + '.+$')})[0]]
            except:
                test2 =[]

            test = test1 + test2
            
        dict_list = []

        try:
            for t in test:
                context = t.attrs
                context['value'] = t.text
                context['company'] = company
                context['metric'] = tag
                dict_list.append(context)
        except: 
            dict_list = []

        df = pd.DataFrame(dict_list)
        df.drop_duplicates(subset=['contextRef', 'value', 'company'], inplace=True)
        main_df = main_df.append(df)

    return main_df

def main_func(years, up_file):

    prior_year = str(int(years) - 1)
    year_list = [prior_year, years]

    df_out = pd.DataFrame(columns=['metric', 'contextRef', 'decimals', 'id', 'unitRef', 'value', 'company'])
    input_data = gen_func(up_file, years, "10-k")
    for i in range(len(input_data['link'])):
        company = input_data['company'][i]
        link = input_data['link'][i]
        df = get_data(link, company, year_list)
        if isinstance(df, str):
            pass
        else:
            df_out = df_out.append(df)
            #df_out = df_out.drop(['decimals', 'id'], axis=1)

    df_out = df_out.drop(['id', 'decimals'], axis = 1)
    df_out.columns = ['Metric', 'FYE', 'Units', 'Value', 'Company']
    
    df_out['Units'] = df_out['Units'].replace('^(.*)?(?i)usd(.+)?|Unit1', 'USD', regex=True)

    df_out = df_out.merge(map_df, how='left', left_on='Metric', right_on='metric')
    df_out.drop(columns=['Metric', 'metric'], inplace=True)
    df_out = df_out[['Company','Standard metric','Value','Units', 'FYE']]

    pattern1 = '^(.+)?' + prior_year + '(.+)?'
    pattern2 = '^(.+)?' + years + '(.+)?'
    df_out['Year'] = df_out['FYE']
    df_out['Year'] = df_out['Year'].str.replace(pattern2, years)
    df_out['Year'] = df_out['Year'].str.replace(pattern1, prior_year)
    

    df_out.to_excel('test_output.xlsx', encoding="UTF-16", index=False)


    return "Scraping complete"
