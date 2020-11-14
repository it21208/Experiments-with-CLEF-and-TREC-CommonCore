from csv import reader
from os import listdir
from os.path import isfile, join
import sys
import pandas as pd
import csv
csv.field_size_limit(sys.maxsize)

TOPICS_PATH = '/home/pfb16181/MeLIR/resources/topics/all.topics2017_2018_2019/'

CLEF_TOPIC_LIST = [
    'CD010860'
]

LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC = []
for TOPIC in CLEF_TOPIC_LIST:
    TOPIC_FILE_PATH = TOPICS_PATH+TOPIC
    record = False
    PMIDs_list_for_TOPIC = []
    with open(TOPIC_FILE_PATH, "r") as f:
        while f:
            line = f.readline()
            if not line:
                break
            if record:
                PMIDs_list_for_TOPIC.append(line.strip())
            if line.startswith("Pids:"):
                record = True
    LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC.append(PMIDs_list_for_TOPIC)
    
print('created LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC.. with size {}'.format(len(LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC)))
flat_LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC = [item for sublist in LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC for item in sublist]
print('created flatten LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC.. with size {}'.format(len(flat_LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC)))
unique_flat_LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC = set(flat_LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC)
print('created unique_flat_LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC.. with size {}'.format(len(unique_flat_LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC)))

list_lines_saved_for_1718TestCLEF = []
cnt = 0
cnt2 = 0
with open('/home/pfb16181/NetBeansProjects/birch/data/datasets/clef171819.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    for idx, row in enumerate(csv_reader):
        try:
            line = row[0]
            docid = line.split('\t')[-3].split('_')[0]
            qid = line.split('\t')[-2]
            # if docid in unique_flat_LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC and qid in CLEF_TOPIC_LIST:
            if qid in CLEF_TOPIC_LIST:
                modified_line = row[0]
                temp = modified_line.split('\t') 
                temp[-1] = str(cnt2)      
                list_lines_saved_for_1718TestCLEF.append(temp)
                cnt2 += 1
        except Exception:
            cnt += 1
print(row[0])
print('created list_lines_saved_for_1718TestCLEF.. with {} exceptions and size = {}. length of csv reader {}'.format(cnt, len(list_lines_saved_for_1718TestCLEF), idx))

sep = "\t"
with open('/home/pfb16181/NetBeansProjects/birch/data/datasets/clef.csv', 'w') as csv:
    for row in list_lines_saved_for_1718TestCLEF:
        csv.write(sep.join(row))
        csv.write("\n")
