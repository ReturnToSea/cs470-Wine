#pip install pandas openpyxl
#pip install xlrd
import pandas as pd
import os

input_folder = 'Sales Registers'

output1 = 'register1'
output2 = 'register2'

counter = 1

for file_name in os.listdir(input_folder):
    if file_name.endswith('.xls') or file_name.endswith('xlsx'):
        file_path = os.path.join(input_folder, file_name)

        df = pd.read_excel(file_path)

        first_path = df.iloc[:, :9] #A-I
        second_path = df.iloc[:, 9:] #Everything after

        first_output = os.path.join(output1, f'r1_{counter}.csv')
        second_output = os.path.join(output2, f'r2_{counter}.csv')

        first_path.to_csv(first_output, index=False)
        second_path.to_csv(second_output, index=False)

        counter += 1

