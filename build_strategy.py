import csv

def read_csv(filename):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        strategy = {rows[0]: rows[1:] for rows in reader}
    return strategy