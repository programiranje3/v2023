"""

Common Input/Output (IO) functions

"""

from pathlib import Path
# A handy tutorial for the pathlib.Path class: https://www.pythontutorial.net/python-standard-library/python-path/

from sys import stderr
import pickle
import json
import csv


def get_data_dir():
    data_dir = Path.cwd() / 'data'
    if not data_dir.exists():
        data_dir.mkdir()
    return data_dir


def get_results_dir():
    results_dir = Path.cwd() / 'results'
    if not results_dir.exists():
        results_dir.mkdir()
    return results_dir


def write_to_txt_file(*text, fpath):
    try:
        with open(fpath, 'w') as fobj:
            for line in text:
                fobj.write(line + "\n")
    except OSError as err:
        stderr.write(f"OSError occurred when trying to write to txt file {fpath}\n:{err}\n")


def read_from_txt_file(fpath):
    try:
        with open(fpath, "r") as fobj:
            return [line.rstrip('\n') for line in fobj.readlines()]
    except FileNotFoundError as err:
        stderr.write(f"Error - file <{fpath}> does not exist\n")
        return []
    except OSError as err:
        stderr.write(f"OSError occurred when trying to read data from txt file {fpath.name}:\n{err}\n")
        return []


def serialise_to_file(obj, fpath):
    try:
        with open(fpath, 'wb') as fobj:
            pickle.dump(obj, fobj)
    except pickle.PicklingError as perr:
        stderr.write(f"Pickling error when trying to serialise object to {fpath.name} file\n:{perr}\n")
    except OSError as err:
        stderr.write(f"OSError when serialising object to {fpath.name} file\n:{err}\n")


def deserialise_from_file(fpath):
    try:
        with open(fpath, 'rb') as fobj:
            return pickle.load(fobj)
    except pickle.UnpicklingError as perr:
        stderr.write(f"Error when unpickling object from file {fpath.name}:\n{perr}\n")
        return None
    except OSError as err:
        stderr.write(f"OS error while trying to deserialise data from {fpath.name} file:\n{err}\n")
        return None


def write_to_csv(data, fpath, fieldnames, delimiter=','):
    try:
        with open(fpath, 'w') as fobj:
            csv_writer = csv.writer(fobj, delimiter=delimiter)
            csv_writer.writerow(fieldnames)
            for data_row in data:
                csv_writer.writerow(data_row)
    except csv.Error as err:
        stderr.write(f"CSV specific error occurred while trying to write to file {fpath}:\n{err}\n")
    except OSError as err:
        stderr.write(f"OS error occurred while trying to wtite to file {fpath}:\n{err}\n")


def write_to_csv_as_dict(data, fpath, fieldnames, delimiter=','):
    try:
        with open(fpath, 'w') as fobj:
            csv_writer = csv.DictWriter(fobj, delimiter=delimiter, fieldnames=fieldnames)
            csv_writer.writeheader()
            for data_row in data:
                csv_writer.writerow(data_row)
    except csv.Error as err:
        stderr.write(f"CSV specific error occurred while trying to write to file {fpath}:\n{err}\n")
    except OSError as err:
        stderr.write(f"OS error occurred while trying to write to file {fpath}:\n{err}\n")


def read_from_csv(fpath, delimiter=','):
    try:
        with open(fpath, 'r') as fobj:
            return list(csv.reader(fobj, delimiter=delimiter))
    except csv.Error as err:
        stderr.write(f"CSV specific error occurred while trying to read from file {fpath}:\n{err}\n")
        return []
    except OSError as err:
        stderr.write(f"OS error occurred while trying to read from csv file <{fpath}>:\n{err}\n")
        return []


def read_from_csv_as_dict(fpath, delimiter=','):
    try:
        with open(fpath, 'r') as fobj:
            return list(csv.DictReader(fobj, delimiter=delimiter))
    except csv.Error as err:
        stderr.write(f"CSV specific error occurred while trying to read from file {fpath}:\n{err}\n")
        return []
    except OSError as err:
        stderr.write(f"OS error occurred while trying to read from csv file <{fpath}>:\n{err}\n")
        return []


def write_to_json(obj, fpath):
    try:
        with open(fpath, 'w') as fobj:
            json.dump(obj, fobj, indent=3)
    except OSError as err:
        stderr.write(f"OS error occurred while trying to write to file {fpath}:\n{err}\n")


def read_from_json(fpath):
    try:
        with open(fpath, 'r') as fobj:
            return json.load(fobj)
    except json.JSONDecodeError as err:
        stderr.write(f"Error occurred while trying to decode data from json file {fpath}:\n{err}\n")
        return None
    except OSError as err:
        stderr.write(f"OS error occurred while trying to read from json file {fpath}:\n{err}\n")
        return None