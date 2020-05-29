import json

stylename = "patient_mint"
# stylename = "patient_mint_dark"
json_filename = stylename + ".json"
template_filename = "template.qss"
output_filename = stylename + ".qss"
with open(json_filename) as json_file:
    data = json.load(json_file)
    with open(output_filename, "w") as output_file:
        with open(template_filename, "r") as template_file:
            for line in template_file:
                for key in data.keys():
                    line = line.replace(key, data[key])
                output_file.write(line)
