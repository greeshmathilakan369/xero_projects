import json
import csv

# Opening JSON file
f = open('response_bancesheet.json')
data = json.load(f)

# now we will open a file for writing
data_file = open('data_file5.csv', 'w')

csv_writer = csv.writer(data_file)
# Counter variable used for writing
# headers to the CSV file
count = 0

for row_obj in data["Reports"][0]["Rows"]:
        if 'Title' in row_obj:
            if len(row_obj["Rows"]):
               print(row_obj) 
               csv_writer.writerow(row_obj.values())
data_file.close()

