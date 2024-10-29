import csv
import pandas as pd

file_path = 'Register1/r1_1.csv'

with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    read_data = False
    for row in csv_reader:
        for cell in row:
            if cell.strip():
                print(cell)