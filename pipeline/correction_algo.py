from utils import *
import pandas as pd
import os

file_name = 'my-stocks.csv'
file_path = f'pipeline/screens/{file_name}'
output_path = f'pipeline/outputs/{file_name}'
csv_tuples = []

current_directory = os.getcwd()
print("Current Working Directory:", current_directory)

# Check if the directory exists, and create it if it doesn't
if not os.path.exists(output_path):
    os.makedirs(output_path)
    print(f"Directory '{output_path}' created.")
else:
    print(f"Directory '{output_path}' already exists.")


try:
    with open(file_path, 'r') as file:
        for line in file:
            values = line.strip().split(',')
            csv_tuples.append(tuple(values))
except FileNotFoundError:
    print(f"The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")


output_data = {
    "company_id" : [],
    "company_name" : [],
    "route" : [],
    "all_time_high_eps" : [],
    "eps_this_quarter" : [],
    "all_time_high_price" : [],
    "price_today" : []
}


for tup in csv_tuples:

    company_id = tup[0]
    company_name = tup[1]
    route = tup[2]

    output_data["company_id"].append(company_id)
    output_data["company_name"].append(company_name)
    output_data["route"].append(route)

    print(f"Calculating For {company_name}")

    try:

        data = pe_data(company_id,route)
        eps_list = [ float(x[1]) for x in  data["datasets"][0]["values"] ]

        data = price_data(company_id,route)
        price_list = [ float(x[1]) for x in  data["datasets"][0]["values"] ]

        price_today = price_list[-1]
        eps_this_quarter = eps_list[-1]
        all_time_high_price = max(price_list)
        all_time_high_eps = max(eps_list)

        output_data["all_time_high_eps"].append(all_time_high_eps)
        output_data["eps_this_quarter"].append(eps_this_quarter)
        output_data["all_time_high_price"].append(all_time_high_price)
        output_data["price_today"].append(price_today)


    except Exception as e:
        print(f"Exeption Occured: {e}")

        output_data["all_time_high_eps"].append(None)
        output_data["eps_this_quarter"].append(None)
        output_data["all_time_high_price"].append(None)
        output_data["price_today"].append(None)



df = pd.DataFrame(output_data)
df.to_csv(output_path, index=False)
















    





