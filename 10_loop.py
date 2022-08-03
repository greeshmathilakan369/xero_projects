import json
import csv

# Opening JSON file
f = open('bs_response.json')
data = json.load(f)
list1=[]
list2=[]
# # now we will open a file for writing
data_file = open('balancesheet_report_demo.csv', 'w', encoding='utf-8')

csv_writer = csv.writer(data_file)

balancesheet_header = ['Title','Value','Value']
csv_writer.writerow(balancesheet_header)
for row_obj in data["Reports"][0]["Rows"]:

    # print(row_obj)
    if 'Title' in row_obj:
        print(row_obj['Title'])
        list1.append(row_obj['Title'])
        # csv_writer.writerow([row_obj['Title']])
        # print("in rows...", row_obj['Rows'])
    # if 'Rows' in row_obj:
        for i in row_obj['Rows']:
            # print("value of i==========",i["Cells"])
            for j in i['Cells']:
                print(j["Value"])
                list2.append(j["Value"])
            # print("row_obj inside inner loop...",i['Cells'])
            # if 'Value' in i:
            #     print("new....",i['Value'])




                # csv_writer.writerow([j['Value']])


    else:
        print("else")
print("list1====",list1)
print(("list2====",list2))
data_file.close()