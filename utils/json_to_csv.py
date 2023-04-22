# importing packages
from glob import glob
import json
import csv
import pandas as pd
# open files and iterate through them
with open('../to be sorted/output.csv', 'w') as f:
    for f_name in glob('*.json'):
        if f_name in glob('decoded.*'):
            try:
                with open(f_name) as json_file:
                    stat_file = json.load(json_file)
                    sf = pd.json_normalize(stat_file)
                    df = f.write((sf.to_csv()))

            except json.JSONDecodeError:
                continue

"""export json files as a csv output"""