import pandas as pd
import streamlit as st

import pandas as pd

# Read the CSV file using pandas
data = pd.read_csv('https://github.com/Sid330s/WisePMS/releases/download/v1.0/my-stocks.csv')


data['price_drop'] = (data['all_time_high_price'] - data['price_today']) * 100 / data['all_time_high_price']
data['eps_decrease'] = (data['all_time_high_eps'] - data['eps_this_quarter']) * 100 / data['all_time_high_eps']


data_sorted = data.sort_values(by=['price_drop', 'eps_decrease'], ascending=[False, True])

# Function to construct URL from name
def construct_url_from_name(route):
    url = f"https://www.screener.in/{route}"
    return url

# Apply the function to the 'Name' column to create the 'Website' column
data_sorted['route'] = data_sorted['route'].apply(construct_url_from_name)


# Function to convert URLs to clickable links
def make_clickable(url):
    return '<a href="{0}" target="_blank">Link</a>'.format(url)

# Apply the function to the 'Website' column
data_sorted['route'] = data_sorted['route'].apply(make_clickable)

data_sorted['price_drop'] = data_sorted['price_drop'].round(2)
data_sorted['eps_decrease'] = data_sorted['eps_decrease'].round(2)

data_sorted = data_sorted.reset_index()

data_sorted.insert(0, 'Rank', data_sorted.index + 1)

# Manually create the HTML table with clickable links
html_table = "<table>"
html_table += "<tr>"
for col in data_sorted.columns:
    html_table += f"<th>{col}</th>"
html_table += "</tr>"

for _, row in data_sorted.iterrows():
    html_table += "<tr>"
    for val in row:
        html_table += f"<td>{val}</td>"
    html_table += "</tr>"

html_table += "</table>"

# Display the HTML table using Streamlit
st.markdown(html_table, unsafe_allow_html=True)

