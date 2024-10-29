import csv

file_path = 'Register1/r1_1.csv'

with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    for row in csv_reader:
        print(row)