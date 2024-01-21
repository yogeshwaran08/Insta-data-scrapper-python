import csv
import json

class Json2Csv:
    def __init__(self, csvpath, jsonpath) -> None:
        self.csvpath = csvpath
        self.jsonpath = jsonpath
        self._convert()
    
    def _convert(self):
        try: 
            with open(self.jsonpath, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
        except Exception as e:
            print("Error occured in reading json file", e)
            return -1 
                
        if(len(data) <= 0):
            return 1
        
        try:
            with open(self.csvpath, 'w', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
                csv_writer.writeheader()
                csv_writer.writerows(data)
        except Exception as e:
            print("Error occured in writing csv file", e)
            return -1 