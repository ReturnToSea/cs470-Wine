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

#change output name when changing to work on all files
first.to_csv(os.path.join(output1, 'r1_1.csv'), index=False)
second.to_csv(os.path.join(output2, 'r2_2.csv'), index=False)

