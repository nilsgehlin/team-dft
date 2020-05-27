import json


json_filename = "patient_mint.json"
template_filename = "template.qss"
output_filename = "patient_mint.qss"
with open(json_filename) as json_file:
    data = json.load(json_file)
    with open(output_filename, "w") as output_file:
        with open(template_filename, "r") as template_file:
            for line in template_file:
                for key in data.keys():
                    line = line.replace(key, data[key])
                output_file.write(line)
