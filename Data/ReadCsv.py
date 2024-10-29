import csv
import pandas as pd

file_path = 'Register1/r1_1.csv'

with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    read_data = False
    for row in csv_reader:
        try:
            date = pd.to_datetime(row[0], errors='raise')
            if not read_data:
                read_data = True
                print(date)
        except ValueError:
            pass
        if read_data:
            #change this to work with all payment types
            #also add here for if it reads in a new date before a payment type
            #it will reset since that last data is incomplete
            if 'EFTPOS' in row: 
                break
            print(row)