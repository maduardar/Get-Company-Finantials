import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


def search_company(search_string):
    url = 'https://finance.yahoo.com/quote/' + search_string + '/financials?p=' + search_string
    client = Request(url)
    response = urlopen(client).read()
    html = BeautifulSoup(response, "html.parser")
    return html


def company_financials(string_search):
    headers, temp_list, label_list, final = ([] for i in range(4))
    index = 0

    html_content = search_company(string_search)
    features = html_content.find_all('div', class_='D(tbr)')

    for item in features[0].find_all('div', class_='D(ib)'):
        headers.append(item.text)

    while index <= len(features) - 1:
        temp = features[index].find_all('div', class_='D(tbc)')
        for line in temp:
            temp_list.append(line.text)
        final.append(temp_list)
        temp_list = []
        index += 1
    df = pd.DataFrame(final[1:])
    df.columns = headers
    df.rename(columns={'ttm': 'Trailing 12 months'}, inplace=True)
    df.style.set_properties(subset=["Breakdown"], **{'text-align': 'left'})
    return df
