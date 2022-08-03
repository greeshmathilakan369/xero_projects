import json
import csv

# Opening JSON file
f = open('bs_response.json')
data = json.load(f)

# # now we will open a file for writing
data_file = open('balancesheet_report.csv', 'w', encoding='utf-8')

csv_writer = csv.writer(data_file)

balancesheet_header = ['Title','Value','Value']
csv_writer.writerow(balancesheet_header)
for row_obj in data["Reports"][0]["Rows"]:

    # print(row_obj)
    if 'Title' in row_obj:
        print(row_obj['Title'])
        csv_writer.writerow([row_obj['Title']])
        # print("in rows...", row_obj['Rows'])
    # if 'Rows' in row_obj:
        for i in row_obj['Rows']:
            # print("value of i==========",i["Cells"])
            for j in i['Cells']:
                print(j["Value"])
            # print("row_obj inside inner loop...",i['Cells'])
            # if 'Value' in i:
            #     print("new....",i['Value'])




                csv_writer.writerow([j['Value']])


    else:
        print("else")
data_file.close()

# [{
#     'RowType': 'Row',
#     'Cells': [{
#         'Value': 'Business Trans Acct',
#         'Attributes': [{
#             'Value': '7bf9d0f1-f0be-4f08-8c4a-a1712ebe3ee9',
#             'Id': 'account'
#         }]},
#         {'Value': '11921.88',
#          'Attributes': [{
#              'Value': '7bf9d0f1-f0be-4f08-8c4a-a1712ebe3ee9',
#              'Id': 'account'
#          }]},
#         {'Value': '10702.55',
#          'Attributes':
#              [{
#                  'Value': '7bf9d0f1-f0be-4f08-8c4a-a1712ebe3ee9',
#                  'Id': 'account'
#              }]}]},
#     {'RowType': 'SummaryRow',
#      'Cells': [{
#          'Value': 'Total Bank'
#      },
#          {'Value': '11921.88'},
#          {'Value': '10702.55'}
#      ]}]

#     {'RowType': 'Header', 'Cells': [{'Value': ''}, {'Value': '31 Jul 2022'}, {'Value': '31 Jul 2021'}]}


# dict1={'id':101,'id2':102,'id3':103}
# print(dict1)

# print(dict1['id'])