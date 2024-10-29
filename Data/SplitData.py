#pip install pandas openpyxl
#pip install xlrd
import pandas as pd
import os

file_path = 'Sales Registers/Till Export 021222.xls'

df = pd.read_excel(file_path)

output1 = 'register1'
output2 = 'register2'

first = df.iloc[:, :9] #A-I
second = df.iloc[:, 9:] #Everything after

first.to_csv(os.path.join(output1, 'first_part.csv'), index=False)
second.to_csv(os.path.join(output2, 'second_part.csv'), index=False)

