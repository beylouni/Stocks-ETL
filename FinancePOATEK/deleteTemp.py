"""
A code to clean all the directories.

Sometimes the lines 19 to 21 can generata a permission error, if this happens it means that you are not
running Python in adm mode.

OBS: don't worry, you don't need to run in adm mode to work, it's just a plus, not an obligation.
"""
import os

directories_temp = os.listdir('temp')
directories_csv = os.listdir('csv')

for local_dir in directories_temp:
    for file in os.listdir('./temp/' + local_dir):
        os.remove(f'./temp/{local_dir}/{file}')


for file in directories_csv:
    os.remove(f'./csv/{file}')


try:
    for local_dir in directories_temp:
        os.remove(f'./temp/{local_dir}')

except PermissionError as error:
    print(f'Error: {error}', 'Try to run in adm mode.', sep='\n')
