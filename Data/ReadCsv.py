import csv
import pandas as pd
import re

file_path = 'Register1/r1_1.csv'

date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
read_data = False

payment_types = ("EFTPOS", "CASH", "AMEX")

with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    read_data = False
    for row in csv_reader:
        for cell in row:
            if cell.strip():
                if date_pattern.match(cell.strip()): #Find Day (can treat this as start of new order)
                    read_data = True
                    print(cell)
                if read_data:
                    print(cell)