"""

Common Input/Output (IO) functions

"""
from pathlib import Path
from sys import stderr
import pickle


def get_data_dir():
    data_dir = Path.cwd() / 'data'
    if not data_dir.exists():
        data_dir.mkdir(parents=True)
    return data_dir


def get_results_dir():
    res_dir = Path.cwd() / 'results'
    if not res_dir.exists():
        res_dir.mkdir(parents=True)
    return res_dir


def write_to_txt_file(*text, fpath):
    try:
        with open(fpath, 'w') as fobj:
            for line in text:
                fobj.write(line + "\n")
    except OSError as err:
        stderr.write(f"Error while trying to write to file {fpath}; source message:\n{err}\n")


def read_from_txt_file(fpath):
    try:
        with open(fpath, 'r') as fobj:
            return [line.rstrip('\n') for line in fobj.readlines()]
    except FileNotFoundError:
        stderr.write(f"File {fpath} does not exist -> cannot proceed\n")
        return []
    except OSError as err:
        stderr.write(f"Error while trying to read from {fpath}; source message:\n{err}\n")
        return []


def serialise_to_file(obj, fpath):
    try:
        with open(fpath, 'wb') as fobj:
            pickle.dump(obj, fobj)
    except pickle.PicklingError as err:
        stderr.write(f"Pickling error when serialising data to file {fpath.name}:\{err}\n")
    except OSError as err:
        stderr.write(f"Error while trying to write to file {fpath}; source message:\n{err}\n")


def unpickle_from_file(fpath):
    try:
        with open(fpath, 'rb') as fobj:
            return pickle.load(fobj)
    except pickle.UnpicklingError as err:
        stderr.write(f"Pickling error when deserialising data from file {fpath.name}:\{err}\n")
        return None

def write_to_csv(data, fpath, fieldnames, delimiter=','):
    pass


def write_to_csv_as_dict(data, fpath, fieldnames, delimiter=','):
    pass


def read_from_csv(fpath, delimiter=','):
    pass


def read_from_csv_as_dict(fpath, delimiter=','):
    pass


def write_to_json(obj, fpath):
    pass


def read_from_json(fpath):
    pass
