from csv import reader
from os import listdir
from os.path import isfile, join
import sys
import pandas as pd
import csv
csv.field_size_limit(sys.maxsize)

TOPICS_PATH = '/home/pfb16181/MeLIR/resources/topics/all.topics2017_2018_2019/'

CLEF_TOPIC_LIST2017=[
    'CD007431', 'CD008081', 'CD008760', 'CD008782', 'CD008803', 'CD009135', 'CD009185', 'CD009372', 'CD009519', 'CD009551',
    'CD009579', 'CD009647', 'CD009786', 'CD009925', 'CD010023', 'CD010173', 'CD010276', 'CD010339', 'CD010386', 'CD010542',
    'CD010633', 'CD010653', 'CD010705', 'CD010772', 'CD010775', 'CD010783', 'CD010860', 'CD010896', 'CD011145', 'CD012019'
]

CLEF_TOPIC_LIST2018 = [
    'CD008122', 'CD008587', 'CD008759', 'CD008892', 'CD009175', 'CD009263', 'CD009694', 'CD010213', 'CD010296', 'CD010502', 
    'CD010657', 'CD010680', 'CD010864', 'CD011053', 'CD011126', 'CD011420', 'CD011431', 'CD011515', 'CD011602', 'CD011686',
    'CD011912', 'CD011926', 'CD012009', 'CD012010', 'CD012083', 'CD012165', 'CD012179', 'CD012216', 'CD012281', 'CD012599'
]

CLEF_TOPIC_LIST = CLEF_TOPIC_LIST2017 + CLEF_TOPIC_LIST2018

LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC = []
full_csv_file = []
for TOPIC in CLEF_TOPIC_LIST:
    TOPIC_FILE_PATH = TOPICS_PATH+TOPIC
    record = False
    PMIDs_list_for_TOPIC = []
    with open(TOPIC_FILE_PATH, "r") as f:
        while f:
            line = f.readline()
            full_csv_file.append(line)
            if not line:
                break
            if record:
                PMIDs_list_for_TOPIC.append(line.strip())
            if line.startswith("Pids:"):
                record = True
    LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC.append(PMIDs_list_for_TOPIC)
    
print('created LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC..')

flat_LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC = [
    item for sublist in LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC for item in sublist]

print('flatten LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC..')

list_saved_pmids_for_1718TestCLEF = []
with open('/home/pfb16181/NetBeansProjects/birch/data/datasets/clef171819_sents.csv', 'r') as read_obj:
    csv_reader = reader(read_obj)
    for row in csv_reader:
        try:
            docid = row[0].split('\t')[-3].split('_')[0]     
            if docid in flat_LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC:
                list_saved_pmids_for_1718TestCLEF.append(docid)
        except Exception:
            pass
        
print('created list_saved_pmids_for_1718TestCLEF..')
new_csv_file = []
cnt = 0
for row in full_csv_file:
    try:
        if row[0].split('\t')[-3].split('_')[0] in list_saved_pmids_for_1718TestCLEF:
            new_csv_file.append(row[0].split('\t'))
    except Exception as e:
        print(row)
        cnt += 1        
print('created new_csv_file.. with {} exceptions'.format(cnt))

PATH_TO_SAVE_CSV_1718TestCLEF = '/home/pfb16181/NetBeansProjects/birch/data/datasets/clef1718_sents.csv'
df = pd.DataFrame(new_csv_file)
df.to_csv(PATH_TO_SAVE_CSV_1718TestCLEF, index=False, header=False)
print('written new_csv_file')

# with open(PATH_TO_SAVE_CSV_1718TestCLEF, 'w+') as f:
#     write = csv.writer(f)
#     write.writerows(new_csv_file)

