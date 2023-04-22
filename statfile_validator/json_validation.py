from glob import glob
import json
"""iterate through statfiles and indicate discrepancies as compared to the schema"""
import jsonschema

error_summary = []
with open(r'C:\Users\micah\Documents\GitHub\Project-Rio-Scripts\statfile_validator\jsonschema.json') as f:
    schema = json.load(f)
for f_name in glob('*.json'):
    if f_name in glob('decoded.*'):
        with open(f_name) as json_file:
            stat_file = json.load(json_file)
            sf = stat_file

            vd = jsonschema.Draft6Validator(schema)
            errors = vd.iter_errors(sf)

            for error in errors:
                error_summary.append(error)
                error_summary.append('----------------------------------------------')
with open('errormsg.txt', 'w') as f:
    for error in error_summary:
        f.write(str(error))
        f.write("\n")
