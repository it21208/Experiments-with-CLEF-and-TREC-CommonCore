import sys

CLEF_TOPIC_LIST = [
    'CD005139', 'CD005253', 'CD006715', 'CD007431', 'CD007868', 'CD008018', 'CD008081', 'CD008170', 'CD008201', 
    'CD010019', 'CD010355', 'CD010502', 'CD010526', 'CD010657', 'CD010680', 'CD010771', 'CD010772', 'CD010775', 
    'CD010778', 'CD010783', 'CD010860', 'CD010864', 'CD010896', 'CD011053', 'CD011126', 'CD011145', 'CD011380', 
    'CD011420', 'CD011431', 'CD011436', 'CD011515', 'CD011571', 'CD011602', 'CD011686', 'CD011912', 'CD011926', 
    'CD012009', 'CD012010', 'CD012083', 'CD012120', 'CD012164', 'CD012165', 'CD012179', 'CD012216', 'CD012223', 
    'CD012281', 'CD012347', 'CD012521', 'CD012599', 'CD012930', 'CD007394', 'CD007427', 'CD008054', 'CD008122', 
    'CD008587', 'CD008643', 'CD008686', 'CD008691', 'CD008759', 'CD008760', 'CD008782', 'CD008803', 'CD008892', 
    'CD009020', 'CD009135', 'CD009175', 'CD009185', 'CD009263', 'CD009323', 'CD009372', 'CD009519', 'CD009591', 
    'CD009579', 'CD009551', 'CD009593', 'CD009647', 'CD009694', 'CD009786', 'CD009925', 'CD009944', 'CD010023', 
    'CD010173', 'CD010213', 'CD010276', 'CD010296', 'CD010339', 'CD010386', 'CD010409', 'CD010438', 'CD010542', 
    'CD010632', 'CD010633', 'CD010653', 'CD010705', 'CD011134', 'CD011548', 'CD011549', 'CD011975', 'CD011984',
    'CD012019', 'CD000996', 'CD001261', 'CD004414', 'CD006468', 'CD007867', 'CD008874', 'CD009044', 'CD009069',
    'CD009642', 'CD010038', 'CD010239', 'CD010558', 'CD010753', 'CD011140', 'CD011768', 'CD011977', 'CD012069',
    'CD012080', 'CD012233', 'CD012342', 'CD012455', 'CD012551', 'CD012567', 'CD012669', 'CD012768'
]

RES_PATH = '/home/pfb16181/NetBeansProjects/new-anserini-master/runs/run.clef171819.bm25+rm3.topics.clef171819.txt'
TOPICS_PATH = '/home/pfb16181/MeLIR/resources/topics/all.topics2017_2018_2019/'
OUT_PATH = '/home/pfb16181/NetBeansProjects/new-anserini-master/runs/ONLY_SUBSET_run.clef171819.bm25+rm3.topics.clef171819.txt'

LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC = {}
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
    LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC[TOPIC] = PMIDs_list_for_TOPIC

print('created LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC.. with size {}'.format(
    len(LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC)))

trecStyleRes = []
previous_topic = open(RES_PATH).readline().split()[0]
rank = 1
with open(RES_PATH, 'r') as fp:
    for line in fp:
        topic, tag1, pmid, orig_rank, score, tag2 = line.split()
            
        if topic != previous_topic:
            rank = 1

        if pmid in LIST_OF_LISTs_OF_PMIDS_FOR_EACH_TOPIC[topic]:
            newline = topic+" "+tag1+" "+pmid+" "+str(rank)+" "+score+" "+tag2
            trecStyleRes.append(newline)
            rank += 1
        
        previous_topic = topic

# print(trecStyleRes)

with open(OUT_PATH, 'w') as f:
    for item in trecStyleRes:
        f.write("%s\n" % item)
