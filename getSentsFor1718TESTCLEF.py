from csv import reader
from os import listdir
from os.path import isfile, join
import sys
import pandas as pd
import csv
csv.field_size_limit(sys.maxsize)

# declaring base dir path to CLEF topics. 
TOPICS_PATH = '/home/pfb16181/MeLIR/resources/topics/all.topics2017_2018_2019/'

''' Declaring different CLEF sub collections. ''' 

# CLEF_TOPIC_LIST = [
#     'CD010860'
# ]

# CLEF_TOPIC_LIST = [
#     'CD007431', 'CD008081', 'CD008760', 'CD008782', 'CD008803'
# ]

CLEF_TOPIC_LIST = [
    'CD007431', 'CD008081', 'CD008760', 'CD008782', 'CD008803', 'CD009135', 'CD009185', 'CD009372', 'CD009519', 'CD009551',
    'CD009579', 'CD009647', 'CD009786', 'CD009925', 'CD010023', 'CD010173', 'CD010276', 'CD010339', 'CD010386', 'CD010542',
    'CD010633', 'CD010653', 'CD010705', 'CD010772', 'CD010775', 'CD010783', 'CD010860', 'CD010896', 'CD011145', 'CD012019',
    'CD008122', 'CD008587', 'CD008759', 'CD008892', 'CD009175', 'CD009263', 'CD009694', 'CD010213', 'CD010296', 'CD010502', 
    'CD010657', 'CD010680', 'CD010864', 'CD011053', 'CD011126', 'CD011420', 'CD011431', 'CD011515', 'CD011602', 'CD011686',
    'CD011912', 'CD011926', 'CD012009', 'CD012010', 'CD012083', 'CD012165', 'CD012179', 'CD012216', 'CD012281', 'CD012599'
]

# initialising a list which will store sublists containing the PMIDs of each topic.
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
            # if the previously read line started with "Pids:" then this following block of code is executed. 
            if record:
                PMIDs_list_for_TOPIC.append(line.strip())
            if line.startswith("Pids:"):
                record = True
    LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC.append(PMIDs_list_for_TOPIC)
    
# print length of list 
print('created LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC.. with size {}'.format(len(LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC)))

# flatten the list with list comprehension.
flat_LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC = [item for sublist in LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC for item in sublist]

print('created flatten LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC.. with size {}'.format(len(flat_LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC)))

# remove duplicate pmids from flatten list.
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

print('created list_lines_saved_for_1718TestCLEF.. with {} exceptions and size = {}. length of csv reader {}'.format(cnt, len(list_lines_saved_for_1718TestCLEF), idx))

# write results to output.
sep = "\t"
with open('/home/pfb16181/NetBeansProjects/birch/data/datasets/clef1718.csv', 'w') as csv:
    for row in list_lines_saved_for_1718TestCLEF:
        csv.write(sep.join(row))
        csv.write("\n")
