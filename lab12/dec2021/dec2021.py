import csv
import pandas as pd
from sys import stderr
from pathlib import Path
from pprint import pprint
from datetime import datetime
from collections import defaultdict

def read_data_from_csv_file(fpath):

    # Option 1
    try:
        with open(fpath, 'r') as fobj:
            return list(csv.DictReader(fobj))
    except csv.Error as err:
        stderr.write(f"CSV-specific error while reading from csv file {fpath.name}:\n{err}\n")
        return None
    except OSError as err:
        stderr.write(f"OS error while reading from csv file {fpath.name}:\n{err}\n")
        return None

    # Option 2
    # try:
    #     with open(fpath, 'r') as fobj:
    #         rows = csv.reader(fobj)
    #         res_list = []
    #
    #         var_names = next(rows)
    #         for data_row in rows:
    #             res_list.append({key: val for key, val in zip(var_names, data_row)})
    #         return res_list
    #
    # except csv.Error as err:
    #     stderr.write(f"CSV-specific error while reading from csv file {fpath.name}:\n{err}\n")
    #     return None
    # except OSError as err:
    #     stderr.write(f"OS error while reading from csv file {fpath.name}:\n{err}\n")
    #     return None

    # Option 3
    # try:
    #     df = pd.read_csv(fpath)
    #     return df.to_dict('records')
    # except Exception as e:
    #     stderr.write(f"Error while reading from csv file {fpath.name}:\n{e}\n")
    #     return None


def max_yearly_funding_a_round(funding_list):

    yearly_fundings = defaultdict(list)

    for funding in funding_list:
        if funding['round'] != 'a': continue
        try:
            funded_dt = datetime.strptime(funding['fundedDate'], '%d-%b-%y')
        except ValueError:
            stderr.write(f"Error while parsing the funded date {funding['fundedDate']}. Will skip this entry\n")
        else:
            if funded_dt.year not in range(2005, 2009): continue
            try:
                yearly_fundings[funded_dt.year].append((funding['company'], float(funding['raisedAmt'])))
            except ValueError:
                stderr.write(f"Error while parsing the funded amount {funding['raisedAmt']}. Will skip this entry\n")

    res_dict = dict()
    for year, funding in sorted(yearly_fundings.items()):
        res_dict[year] = max(funding, key=lambda f: f[1])

    return res_dict


def write_results_to_csv(resullts_list):

    try:
        with open(Path.cwd() / 'task3_results.csv', 'w') as fobj:
            csv_writer = csv.writer(fobj)
            csv_writer.writerow(('year', 'state', 'tot_amount', 'city_cnt'))
            for result in resullts_list:
                csv_writer.writerow(result)
    except csv.Error as err:
        stderr.write(f"CSV-specific error while writing to csv file:\n{err}\n")
    except OSError as err:
        stderr.write(f"OS error while writing to csv file:\n{err}\n")


def teritorial_diversity_report(funding_list):

    year_state_tot_funding = defaultdict(float)
    year_state_cities = defaultdict(set)

    for funding in funding_list:
        try:
            funded_dt = datetime.strptime(funding['fundedDate'], '%d-%b-%y')
        except ValueError:
            stderr.write(f"Error while parsing the funded date {funding['fundedDate']}. Will skip this entry\n")
        else:
            year_state = funded_dt.year, funding['state']
            try:
                year_state_tot_funding[year_state] += float(funding['raisedAmt'])
                year_state_cities[year_state].add(funding['city'])
            except ValueError:
                stderr.write(f"Error while parsing the funded amount {funding['raisedAmt']}. Will skip this entry\n")

    res_list = []
    for year_state, tot_funds in year_state_tot_funding.items():
        year, state = year_state
        # print(f"{year}, {state}: total funding: {tot_funds}, in cities: {year_state_cities[year_state]}")
        res_list.append((year, state, tot_funds, len(year_state_cities[year_state])))

    res_list.sort(key=lambda res: (res[0], res[1]))

    write_results_to_csv(res_list)



if __name__  == '__main__':

    funding_list = read_data_from_csv_file(Path.cwd() / 'data/techcrunch.csv')
    # if funding_list:
    #     for funding in funding_list:
    #         pprint(funding)
    # max_funding = max_yearly_funding_a_round(funding_list)
    # for year, funding in max_funding.items():
    #     print(f'{year}: {funding}')

    teritorial_diversity_report(funding_list)