#%%
"""
LAB 7
"""
from io_util import *
from datetime import datetime, time
from sys import stderr
import csv

#%%
"""
TASK 1:

Write the *read_sort_write* function that reads in the content of the given text file,  
sorts it, and writes the (sorted) content to new textual files. The function receives 
the name of the file as its only input argument. 
Assume that the content of the given file consists of file names, some of which 
have an extension ('hello.txt'), others do not ('results'). Each file name is given in a separate line.
Sorting should be case insensitive and done in the ascending alphabetical order, as follows:
- for files with extension: first based on the extension and then based on the file name,
- for files without extension, based on the file name.
After sorting, file names with extension should be writen in one textual file 
('task1_files_with_extension.txt') and file names without extension in another text 
file ('task1_files_no_extension.txt')
Include appropriate try except blocks to prevent program from crushing in case of a non 
existing input file, or any other problem occurring while reading from / writing to a file.

To test the function, use the 'data/file_names_sample.txt' file
"""
#%%

def read_sort_write(fname):

    def no_ext_sort_order(fname_with_ext):
        name, ext = fname_with_ext.lower().rsplit('.', maxsplit=1)
        return ext, name

    fpath = get_data_dir() / fname

    with_ext = []
    no_ext = []
    for line in read_from_txt_file(fpath):
        if '.' in line:
            with_ext.append(line)
        else:
            no_ext.append(line)

    no_ext.sort(key=lambda elem: elem.lower())
    with_ext.sort(key=no_ext_sort_order)

    no_ext_fpath = get_results_dir() / 'task1_files_no_extension.txt'
    write_to_txt_file(*no_ext, fpath=no_ext_fpath)

    with_ext_fpath = get_results_dir() / 'task1_files_with_extension.txt'
    write_to_txt_file(*with_ext, fpath=with_ext_fpath)


#%%
# Test the function using the file 'file_names_sample.txt' in the data directory
# read_sort_write('file_names_sample.txt')



#%%
"""
TASK: 2

The file 'cities_and_times.txt' contains city names and time data.
More precisely, each line contains the name of a city, followed by
abbreviated weekday (e.g. "Sun"), and the time in the form "%H:%M".
Write the 'process_city_data' function that reads in the file and 
creates a time-ordered list of the form:
[('San Francisco', 'Sun', 00:52:00),
 ('Las Vegas', 'Sun', 00:52:00), ...].
Note that the hour and minute data are used to create an object of
the type datetime.time.
The function should also:
- serialise (pickle) the list into a file ('task2_cities_and_times.pkl'), as a list object
- write the list content into a csv file ('task2_cities_and_times.csv'), in the format:
   city; weekday; time
  where time is represented in the format '%H:%M:%S'
Include appropriate try except blocks to prevent the program from crushing
in the case of a non existing file, or a problem while reading from / writing to 
a file, or transforming data values.

Note: for a list of things that can be pickled, see this page:
https://docs.python.org/3/library/pickle.html#pickle-picklable

Bonus 1: use dictionary (instead of tuple) to represent and
manipulate the data read from the text file. This can be combined
with the csv.DictWriter to write data to csv file

Bonus 2: when testing the function, use csv.DictReader
to read in and print the content of the csv file
"""
#%%

def process_city_data(fpath):

    cities_times = []
    for line in read_from_txt_file(fpath):
        city, wday, t = line.rsplit(maxsplit=2)
        try:
            dt = datetime.strptime(t, "%H:%M")
        except ValueError as err:
            stderr.write(f"process_city_data: could not parse time string {t}:\n{err}\n")
        else:
            # Option 1
            # cities_times.append((city, wday, dt.time())
            # Option 2
            cities_times.append({'city': city, 'weekday': wday, 'time': dt.time()})

    # Option 1
    # cities_times.sort(key=lambda elem: elem[2])
    # Option 2
    cities_times.sort(key=lambda elem: elem['time'])

    pickle_fpath = get_results_dir() / 'task2_cities_and_times.pkl'
    serialise_to_file(cities_times, pickle_fpath)

    csv_fpath = get_results_dir() / 'task2_cities_and_times.csv'
    fieldnames = ['city', 'weekday', 'time']
    # Option 1
    # write_to_csv(cities_times, csv_fpath, fieldnames, delimiter=';')
    # Option 2
    write_to_csv_as_dict(cities_times, csv_fpath, fieldnames, delimiter=';')



#%%
# Test the function
# process_city_data(get_data_dir() / "cities_and_times.txt")


#%%
# Restore and print the serialised data
# cities_and_times = deserialise_from_file(get_results_dir() / 'task2_cities_and_times.pkl')
# if cities_and_times:
#     for city_time in cities_and_times:
#         city, wday, local_time = city_time.values()
#         print(f"{city}, {wday}, {local_time}")

#%%
# Restore and print data from the csv file
# city_data = read_from_csv(get_results_dir() / 'task2_cities_and_times.csv', delimiter=';')
# if len(city_data) > 0:
#     for city, wday, local_time in city_data[1:]:
#         print(f"{city}, {wday}, {local_time}")

# cities_and_times = read_from_csv_as_dict(get_results_dir() / 'task2_cities_and_times.csv', delimiter=';')
# if len(cities_and_times) > 0:
#     for city_time_dict in cities_and_times:
#         city, wday, local_time = city_time_dict.values()
#         print(f"{city}, {wday}, {local_time}")


#%%
"""
TASK 3:

In the data folder, there is a text file ('image_files_for_training.txt') that lists 
file paths for a bunch of images (one image file path per line). 
Write the 'process_image_files' function that reads in the content of this text file 
and does the following:
- counts the number of images in each category, and stores the computed
  counts in a csv file ('task3_img_category_stats.csv') in the format: category, image_count
- creates and stores (in a file) a dictionary with the image category as  
  the key and a list of image names in the corresponding category as value;
  for storage use 
  1) pickle ('task3_image_category_data.pkl'), and 
  2) json ('task3_image_category_data.json').
"""

#%%

def process_image_files(fpath):
    from collections import defaultdict
    img_dict = defaultdict(list)

    for line in read_from_txt_file(fpath):
        img_dir, img_fname = line.rsplit('/', maxsplit=1)
        _, _, img_category = img_dir.split('/', maxsplit=2)
        img_category = img_category.replace('/','_')
        img_dict[img_category].append(img_fname)

    pkl_fpath = get_results_dir() / 'task3_image_category_data.pkl'
    serialise_to_file(img_dict, pkl_fpath)

    img_counts = [{'category':img_cat, 'image_count': len(img_fnames)} for img_cat, img_fnames in img_dict.items()]
    csv_fpath = get_results_dir() / 'task3_img_category_stats.csv'
    fieldnames = ['category', 'image_count']
    write_to_csv_as_dict(img_counts, csv_fpath, fieldnames)

    json_fpath = get_results_dir() / 'task3_img_category_stats.json'
    write_to_json(img_dict, json_fpath)



#%%
# Test the function
# process_image_files(get_data_dir() / "image_files_for_training.txt")


#%%
# Read in and print data stored in the csv file
# img_counts_data = read_from_csv_as_dict(get_results_dir() / 'task3_img_category_stats.csv')
# if len(img_counts_data) > 0:
#     for category_count in img_counts_data:
#         print(f"{category_count['category']}: {category_count['image_count']}")

#%%
# Read in and print data stored in the json file
# img_dict = read_from_json(get_results_dir() / 'task3_img_category_stats.json')
# if img_dict:
#     for category, img_files in img_dict.items():
#         print(f"{category.upper()}: {','.join(img_files)}")


#%%
"""
TASK 4:

Write the 'identify_shared_numbers' function that receives file paths for  
two text files with lists of numbers (integers), one number per line. 
The function identifies the numbers present in both lists and stores them
in a new list. 
Finally, the function creates the results dictionary and serialises it to 
a json file ('task4_results.json'). The results dictionary should have the 
following structure:
{
    name_of_the_1st_file: list_of_numbers_from_the_1st_file,
    name_of_the_2nd_file: list_of_numbers_from_the_2nd_file,
    'common_numbers': list_of_the_identified_common_numbers
}

Note: it may happen that not all lines in the input files contain numbers, so,
ensure that only numerical values are considered for comparison.

To test the function use the files 'happy_numbers.txt' and 'prime_numbers.txt'
available in the 'data' folder.

Note: inspired by this exercise:
https://www.practicepython.org/exercise/2014/12/14/23-file-overlap.html
"""
#%%
def identify_shared_numbers(fpath_1, fpath_2):

    def str_to_numbers(lines):
        numbers = []
        for line in lines:
            try:
                number = float(line)
            except ValueError:
                stderr.write(f"could not parse {line} to number, will skip it\n")
            else:
                numbers.append(number)
        return numbers

    numbers_f1 = str_to_numbers(read_from_txt_file(fpath_1))
    numbers_f2 = str_to_numbers(read_from_txt_file(fpath_2))
    common_numbers = [number for number in numbers_f1 if number in numbers_f2]

    result_dict = {
        fpath_1.name:numbers_f1,
        fpath_2.name:numbers_f2,
        'common_numbers':common_numbers
    }

    write_to_json(result_dict, get_results_dir() / 'task4_results.json')


#%%
# Test the function
# t4_f1 = get_data_dir() / "prime_numbers.txt"
# t4_f2 = get_data_dir() / "happy_numbers.txt"
# identify_shared_numbers(t4_f1, t4_f2)


#%%
# Read in and print data stored in the json file
# numbers = read_from_json(get_results_dir() / 'task4_results.json')
# if numbers:
#     for list_name, numbers_list in numbers.items():
#         print(f"{list_name.upper()}: {','.join([str(number) for number in numbers_list])}")


#%%
"""
TASK 5:

Write a function ('collect_and_store_team_data') that prompts the user for name, age, and competition score (0-100)
of members of a sports team. All data items for one member should be entered in a single line, separated by a comma 
(e.g. Bob, 19, 55). The entry stops when the user enters 'done'.
The function stores the data for each team member as a dictionary, such as
{name:Bob, age:19, score:55}
where name is string, age is integer, and score is a real value.
The data for all team members should form a list of dictionaries.
The function sorts the list by the members' scores (from highest to lowest) and
then serialise the list to i) a .json file and ii) a .pkl file. 
"""

#%%
def collect_and_store_team_data():

    def create_member_dict(name, age_str, score_str):
        try:
            return {
                'name': name,
                'age': int(age_str.lstrip()),
                'score': float(score_str.lstrip())
            }
        except ValueError:
            stderr.write(f"Could not parse all the data for {name}, please enter the data again\n")
            return None

    print("You will be asked to enter team members data in the following format:")
    print("name, age, score")
    print("Please enter 'done' to terminate the data entry\n")

    members = []
    while True:
        entry = input("Please enter data (name, age, score) for a team member\n")
        if entry.lower() == 'done':
            break
        try:
            name, age, score = entry.split(',')
        except ValueError:
            stderr.write(f"Wrong input '{entry}', please see the instructions for data entry and try again\n")
        else:
            member_dict = create_member_dict(name, age, score)
            if member_dict:
                members.append(member_dict)

    members.sort(key=lambda member: member['score'], reverse=True)

    serialise_to_file(members, get_results_dir() / 'task5_members_data.pkl')
    write_to_json(members, get_results_dir() / 'task5_members_data.json')



#%%
# collect_and_store_team_data()


#%%
# Read in and print data stored in the json file
# members_data = read_from_json(get_results_dir() / 'task5_members_data.json')
# if members_data:
#     for member in members_data:
#         name, age, score = member.values()
#         print(f"{name}, age:{age}, scored:{score} points")


#%%
"""
TASK 6

Write the 'flights_to_json' function that receives i) an arbitrary number of objects of the
Flight class and ii) name of the json file where the objects should be serialised to. 
The Flight class is defined in the flight module, of the lab6 package.  

Write another function - flights_from_json - that reads, from a json file (given as the input argument), 
data about flights and reconstructs objects of the aforementioned Flight class. 
The function prints the flights, in the chronological order of their departure date and time. 

Hint: use the pyjson_trick package
Check the docs for json-tricks at: https://json-tricks.readthedocs.io/en/latest/
"""
#%%
import json_tricks
from lab6.flight import Flight


def flights_to_json(*flights, fname=None):
    fpath = get_results_dir() / fname
    try:
        with open(fpath, 'w') as fobj:
            json_tricks.dump(flights, fobj, indent=4)
    except Exception as e:
        stderr.write(f"An exception of the type {type(e)} occurred while trying to serialise flights to json\n")
        stderr.write(f"Original error message: {', '.join([str(a) for a in e.args])}\n")


def flights_from_json(fname):
    fpath = get_results_dir() / fname

    try:
        with open(fpath, 'r') as fobj:
            flights = json_tricks.load(fobj)
            if flights:
                for flight in sorted(flights, key=lambda f: f.departure):
                    print(flight)
                    print()
    except Exception as e:
        stderr.write(f"An exception of the type {type(e)} occurred while trying to read flights from json\n")
        stderr.write(f"Original error message: {', '.join([str(a) for a in e.args])}\n")



#%%
# Create a few flight objects to test the functions

lh1411 = Flight('LH1411', '2024-03-20 6:50', ('Belgrade', 'Munich'))

lh992 = Flight('LH992', '2024-02-25 12:20', 'Belgrade -> Frankfurt', 'Lufthansa')

lh1514_dict = {'fl_num':'lh1514',
               'departure': '2023-12-30 16:30',
               'operator': 'Lufthansa',
               'origin': 'Paris',
               'destination': 'Berlin'}
lh1514 = Flight.from_dict(lh1514_dict)

flights = [lh1411, lh992, lh1514]

#%%
# Serialise flight objects to a json file and read them back
# flights_to_json(*flights, fname='task6_flights.json')
#
# flights_from_json('task6_flights.json')


#%%
# Add a few passengers to one of the flights and check again the serialisation/ deserialisation

# from lab6.passenger import EconomyPassenger, BusinessPassenger, FlightService
#
# jim = EconomyPassenger("Jim Jonas", 'UK', '123456')
# bill = EconomyPassenger("Billy Stone", 'USA', "917253", is_covid_safe=True)
# dona = EconomyPassenger("Dona Stone", 'Australia', "917251", is_covid_safe=True)
# kate = BusinessPassenger(name="Kate Fox",
#                          country='Canada',
#                          passport="114252",
#                          is_covid_safe=True,
#                          services=[FlightService.ONBOARD_WIFI, FlightService.MEAL])
# bob = BusinessPassenger(name="Bob Smith", country='UK', passport="123456", checked_in=True)
#
# passengers = [jim, bill, dona, kate, bob]
# airfares = [450, 950, 1500, 1000, 475]
# for p, fare in zip(passengers, airfares):
#     lh992.add_passenger(p, fare)
#
# # Serialise flight objects to a json file and read them back
# flights_to_json(*flights, fname='task6_flights.json')
#
# flights_from_json('task6_flights.json')
