
from functools import reduce
import operator
import json


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