from functools import reduce
import operator
import json
#new
import pandas as pd
from io import BytesIO
import xlsxwriter

def flat_result_data(data):
   return reduce(operator.iconcat, data, [])

def filter_data_by_treshold(records, threshold):
    return list(filter(lambda record: record['confidence'] > threshold, records))

def get_categories(data):
    categories_found = []
    for obj in data:
        category = obj['name']
        if categories_found.count(category) == 0:
            categories_found.append(category)
    return categories_found

def export_to_json(data, file_number):
    with open("./output/batch-"+str(file_number)+".json", "w") as outfile:
        json.dump(data, outfile)
    outfile.close()

#exporting xls file
# def create_xls(records_list, file_names):
#     all_records = []
#     for i, records in enumerate(records_list):
#         for record in records:
#             record['file_name'] = file_names[i]
#         all_records.extend(records)
#     df = pd.DataFrame.from_records(all_records)
#     with BytesIO() as buffer:
#         writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
#         df.to_excel(writer, index=False)
#         writer.save()
#         xls_data = buffer.getvalue()
#     return xls_data

# exporting csv file
def create_csv(records_list, file_names):
    all_records = []
    for i, records in enumerate(records_list):
        for record in records:
            record['file_name'] = file_names[i]
        all_records.extend(records)
    df = pd.DataFrame.from_records(all_records)
    csv_data = df.to_csv(index=False)
    return csv_data

def print_json_data(data):
    for obj in data:
        print(f"Name: {obj['name']}, Confidence: {obj['confidence']}")