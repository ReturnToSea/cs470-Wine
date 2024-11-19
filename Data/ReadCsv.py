import csv
import pandas as pd
import re
import os

directories = ['Register1', 'Register2']
output_file = 'CsvReaderOutput.txt'

date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
read_data = False

payment_types = ("EFTPOS", "CASH", "AMEX")
with open(output_file, mode='w', newline='', encoding='utf-8') as output_file_obj:
    for directory_path in directories:
        for filename in os.listdir(directory_path):
            if filename.endswith('.csv') or (directory_path == 'Register2' and filename.startswith('r2_')):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    read_data = False
                    for row in csv_reader:
                        for cell in row:
                            if cell.strip():
                                if date_pattern.match(cell.strip()): #Find Day (can treat this as start of new order)
                                    read_data = True
                                    #output_file_obj.write(cell + '\n')
                                if read_data:
                                    output_file_obj.write(cell + '\n')