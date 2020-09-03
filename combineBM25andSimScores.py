#  author: alexandros ioannidis

# Does it really require you do that? Can you know think carefully about how documents are being scored, and why they would get a 
# score or not? And alternatively, if a document is not scored by Lucene, can’t you just add that document to the end of the list with a score of zero?

import sys 
import operator

TOPIC_LIST_TEST_2017 = [
    'CD007431', 'CD008081', 'CD008760', 'CD008782', 'CD008803', 'CD009135', 'CD009185', 'CD009372', 'CD009519', 'CD009551',
    'CD009579', 'CD009647', 'CD009786', 'CD009925', 'CD010023', 'CD010173', 'CD010276', 'CD010339', 'CD010386', 'CD010542',
    'CD010633', 'CD010653', 'CD010705', 'CD010772', 'CD010775', 'CD010783', 'CD010860', 'CD010896', 'CD011145', 'CD012019'
]

TOPIC_LIST_TEST_2018 = [
    'CD008122', 'CD008587', 'CD008759', 'CD008892', 'CD009175', 'CD009263', 'CD009694', 'CD010213', 'CD010296', 'CD010502',
    'CD010657', 'CD010680', 'CD010864', 'CD011053', 'CD011126', 'CD011420', 'CD011431', 'CD011515', 'CD011602', 'CD011686',
    'CD011912', 'CD011926', 'CD012009', 'CD012010', 'CD012083', 'CD012165', 'CD012179', 'CD012216', 'CD012281', 'CD012599'
]

TOPIC_LIST = TOPIC_LIST_TEST_2017 + TOPIC_LIST_TEST_2018
# SimResults_filepath = '/home/pfb16181/simScoreResults2.txt'
# SimResults_filepath = '/home/pfb16181/results5.txt'
SimResults_filepath = '/home/pfb16181/resultsFSSVmeanPoolingWithCorrectedCorpus.txt'
BM25Results_filepath = '/home/pfb16181/RetrievalAppSubset.pubmed5.seedDoc_title_and_query_and_queryExpansion_top20Terms_only_from_rel_docsResults.correct.res'


def readTRECresultsIntoDict(results_filepath):
    f = open(results_filepath, "r")
    topic_doc_score_dict = {}
    for i in TOPIC_LIST:
        topic_doc_score_dict[i] = {}
    flag = True
    for line in f:
        topic = line.split()[0]
        doc = line.split()[2]
        score = line.split()[4]            
        if topic not in TOPIC_LIST:
            continue
        else:
            if flag == True:
                prev_topic = topic
                max_score = score
                flag = False
            
            if topic != prev_topic:
                prev_topic = topic
                max_score = score                    
            
            topic_doc_score_dict[topic][doc] = str(float(score)/float(max_score))
    return(topic_doc_score_dict)

def readSimTRECresultsIntoDict(results_filepath):
    f = open(results_filepath, "r")
    topic_doc_score_dict = {}
    for i in TOPIC_LIST:
        topic_doc_score_dict[i] = {}
    for line in f:
        topic = line.split()[0]
        doc = line.split()[2]
        score = line.split()[4]
        if topic not in TOPIC_LIST:
            continue
        else:
            topic_doc_score_dict[topic][doc]= score
    return(topic_doc_score_dict)

BM25_topic_doc_score_dict = readTRECresultsIntoDict(BM25Results_filepath)
print('finished creating BM25_topic_doc_score_list & BM25_topic_doc_score_dict')
Sim_topic_doc_score_dict = readSimTRECresultsIntoDict(SimResults_filepath)
print('finished creating Sim_topic_doc_score_list & Sim_topic_doc_score_dict')

LambdaParam_list = [0.0, 0.5, 1.0]
lstToOutput = []

for idx, ilambda in enumerate(LambdaParam_list):
    resultslst = []
    for topic in TOPIC_LIST:
        ranking = 1
        temp_dict = {}
        for keySim, cur_itemSim in Sim_topic_doc_score_dict[topic].items():
            for keyBM25, cur_itemBM25 in BM25_topic_doc_score_dict[topic].items():
                if keySim == keyBM25:
                    try:
                        temp_dict[keySim] = ilambda * float(cur_itemBM25) + (1-ilambda) * float(cur_itemSim)                      
                    except:
                        print(float(cur_itemBM25))
                        print(float(cur_itemSim))
                    #     v = cur_itemBM25
                    #     temp_dict[keySim] = v
                    
        sorted_d = dict(sorted(temp_dict.items(), key=operator.itemgetter(1),reverse=True))
                      
        for k, v in sorted_d.items():
            temp = topic + " " + "QO" + " " + k + " " + str(ranking) + " "  + str(v) + " " + "similarity.tar.title.and.query"
            resultslst.append(temp)
            ranking += 1
                        
    dirToWrite = '/home/pfb16181/NetBeansProjects/hedwig/scripts/new_resultsBM25andSim.%s' % ilambda
    with open(dirToWrite, 'w') as f:
        for item in resultslst:
            f.write("%s\n" % item)
            
    print('saved result file for lambda param = {}'.format(ilambda))
