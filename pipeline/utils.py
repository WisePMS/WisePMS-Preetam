import math
import datetime
import requests
import time
from bs4 import BeautifulSoup

def cal_realPE(eps_list,pe):

    try:

        pe = float(pe)

        if type(eps_list)==str:
            eps_list = [float(eps.replace(',', '')) for eps in eps_list.split()]
        
        percentage_increases = [(eps - eps_list[i - 1]) / abs(eps_list[i - 1]) * 100 if i > 0 else 0 for i, eps in enumerate(eps_list)]
        percentage_increases.pop(0)
        average_increase = sum(percentage_increases) / len(percentage_increases)
        r = 1 + average_increase/100
        y = math.log(pe * (r - 1) + 1) / math.log(r)

        return {
            "EPS List" :  eps_list,
            "YOY % Increase" : percentage_increases,
            "Avg % Increase" : average_increase,
            "PE" : pe,
            "RealPE" : y
        }
    except Exception as e:
        print(e)
        return {
            "EPS List" :  None,
            "YOY % Increase" : None,
            "Avg % Increase" : None,
            "PE" : None,
            "RealPE" : None
        }

def fetch_data(url):
    response = requests.get(url)

    if response.status_code == 429:
        time.sleep(2)
        response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None

def pe_data(company_id,route):

    route = route.strip('/').split('/')

    # print(route)

    if len(route) == 3:
        consolidated = "&consolidated=true"
    else:
        consolidated = ""

    pe_url = "https://www.screener.in/api/company/{}/chart/?q=Price+to+Earning-Median+PE-EPS&days=10000{}".format(company_id,consolidated)

    data = fetch_data(pe_url)

    return data


def price_data(company_id,route):

    route = route.strip('/').split('/')

    # print(route)

    if len(route) == 3:
        consolidated = "&consolidated=true"
    else:
        consolidated = ""

    price_url = "https://www.screener.in/api/company/{}/chart/?q=Price-DMA50-DMA200-Volume&days=10000{}".format(company_id,consolidated)

    data = fetch_data(price_url)

    return data


def get_profit_cagr(route):

    # URL of the webpage with the HTML content
    url = f'https://www.screener.in/{route}'

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    if response.status_code == 429:
        time.sleep(2)
        response = requests.get(url)

    # Initialize dictionaries to store the data
    profit_growth = {'3 Years': None, '5 Years': None, '10 Years': None, 'TTM' : None, 'PE' : None}

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # spans = soup.find_all('span', class_='name')

        lis = soup.find_all('li', class_='flex flex-space-between')

        # Initialize a variable to store the P/E ratio
        pe_ratio = None

        # Check if the <li> element is found
        for pe_li in lis:
            # Find the <span> element with class "number" within the <li> element
            spans = pe_li.find_all('span', class_='name')
            spans.extend(pe_li.find_all('span', class_='number'))

            try:
                # Check if the <span> element is found
                if 'Stock P/E' in spans[0].text:
                    # Extract the P/E ratio
                    pe_ratio = float(spans[1].text.strip())
            except Exception as e:
                print(e)



        
        # Find the tables with class "ranges-table"
        tables = soup.find_all('table', class_='ranges-table')
        
        # Loop through the tables to extract profit growth data
        for table in tables:
            header = table.find('th', colspan='2')
            if header:
                title = header.text.strip()
                if 'Compounded Profit Growth' in title:
                    rows = table.find_all('tr')
                    for row in rows[1:]:
                        try:
                            columns = row.find_all('td')
                            profit_growth[columns[0].text.strip().replace(':','')] = float(columns[1].text.strip().replace('%',''))
                        except Exception as e:
                            print(e)
        profit_growth['PE'] = pe_ratio
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    return profit_growth




def get_number_of_shareholders(route):

    # URL of the webpage with the HTML content
    url = f'https://www.screener.in/{route}'

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    if response.status_code == 429:
        time.sleep(2)
        response = requests.get(url)

    # Initialize dictionaries to store the data
    res = None

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the tables with class "ranges-table"
        tables = soup.find_all('tr', class_='sub')
        
        # Loop through the tables to extract profit growth data
        print("Tabels:",tables)
        for table in tables:
            header = table.find('td', class_='text')
            if header:
                title = header.text.strip()
                if 'No. of Shareholders' in title:
                    cols = table.find_all('td')
                    print(cols)
                    try:
                        res = int(cols[-1].text.strip().replace(",", ""))
                    except Exception as e:
                        print(e)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    return res