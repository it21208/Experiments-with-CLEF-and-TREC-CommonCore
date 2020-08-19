#  author: alexandros ioannidis
 
# 'TOTAL': [0.25013, 0.073, 0.1058]
# clef2017TestTopics = {'CD007431': [0.129, 0.028, 0.024], 'CD008081': [0.119, 0.051, 0.111], 'CD008760': [0.789, 0.336, 0.705], 'CD008782': [0.224, 0.004, 0.012], 'CD008803': [0.083, 0.067, 0.086],
#                       'CD009135': [0.154, 0.134, 0.184], 'CD009185': [0.456, 0.056, 0.155], 'CD009372': [0.172, 0.011, 0.013], 'CD009519': [0.122, 0.026, 0.028], 'CD009551': [0.097, 0.014, 0.02],
#                       'CD009579': [0.429, 0.03, 0.036], 'CD009647': [0.109, 0.083,  0.041], 'CD009786': [0.112, 0.009, 0.007], 'CD009925': [0.368, 0.146, 0.145], 'CD010023': [0.381, 0.067, 0.161], 
#                       'CD010173': [0.035, 0.003, 0.003], 'CD010276': [0.122, 0.01, 0.01], 'CD010339': [0.048, 0.016, 0.017], 'CD010386': [0.519, 0.019, 0.008], 'CD010542': [0.106, 0.052, 0.058], 
#                       'CD010633': [0.186, 0.006, 0.001], 'CD010653': [0.136, 0.006, 0.021], 'CD010705': [0.377, 0.229, 0.174], 'CD010772': [0.587, 0.361, 0.244], 'CD010775': [0.371, 0.086, 0.681], 
#                       'CD010783': [0.022, 0.004, 0.006], 'CD010860': [0.8, 0.242, 0.133], 'CD010896': [0.31, 0.063, 0.056], 'CD011145': [0.136, 0.022, 0.034], 'CD012019': [0.005, 0.0, 0.001]}


# 'TOTAL': [0.2126, 0.067, 0.0744]
# clef2018TestTopics = {'CD008122': [0.711, 0.238, 0.267], 'CD008587': [0.041, 0.01, 0.016], 'CD008759': [0.38, 0.102, 0.139], 'CD008892': [0.499, 0.105, 0.196], 'CD009175': [0.17, 0.013, 0.013], 
#                       'CD009263': [0.084, 0.004, 0.003], 'CD009694': [0.379, 0.138, 0.104], 'CD010213': [0.074, 0.068, 0.085], 'CD010296': [0.204, 0.017, 0.009], 'CD010502': [0.491, 0.086, 0.088],
#                       'CD010657': [0.116, 0.064, 0.123], 'CD010680': [0.046, 0.014, 0.024], 'CD010864': [0.072, 0.018, 0.03], 'CD011053': [0.061, 0.006, 0.004], 'CD011126': [0.09, 0.002, 0.006],
#                       'CD011420': [0.461, 0.0, 0.0], 'CD011431': [0.668, 0.347, 0.445], 'CD011515': [0.029, 0.019, 0.012], 'CD011602': [0.017, 0.003, 0.006], 'CD011686': [0.271, 0.079, 0.039], 
#                       'CD011912': [0.101, 0.021, 0.025], 'CD011926': [0.512, 0.062, 0.102], 'CD012009': [0.106, 0.067, 0.072], 'CD012010': [0.052, 0.058, 0.045], 'CD012083': [0.273, 0.156, 0.076],
#                       'CD012165': [0.084, 0.06, 0.077], 'CD012179': [0.062, 0.035, 0.043], 'CD012216': [0.038, 0.062, 0.058], 'CD012281': [0.005, 0.003, 0.003], 'CD012599': [0.281, 0.129, 0.121]}

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
SimResults_filepath = '/home/pfb16181/results5.txt'
BM25Results_filepath = '/home/pfb16181/RetrievalApp.pubmed5.seedDoc_title_and_query_and_queryExpansion_top20Terms_only_from_rel_docsResults.correct.res'

def readTRECresultsIntoDict(results_filepath):
    f = open(results_filepath, "r")
    topic_doc_score_list = []
    # topic_doc_score_dict = {}
    for line in f:
        topic = line.split()[0]
        doc = line.split()[2]
        score = line.split()[4]
        topic_doc_score_list.append([topic, [doc, score]])
    return(topic_doc_score_list)

BM25_topic_doc_score_list = readTRECresultsIntoDict(BM25Results_filepath)
print('finished creating BM25_topic_doc_score_list')
Sim_topic_doc_score_list = readTRECresultsIntoDict(SimResults_filepath)
print('finished creating Sim_topic_doc_score_list')

LambdaParam_list = [0, 0.2, 0.4, 0.6, 0.8, 1]
list_topic_score_copies2017 = [[]]*len(LambdaParam_list)
list_topic_score_copies2018 = [[]]*len(LambdaParam_list)

lstToOutput = []


for idx, ilambda in enumerate(LambdaParam_list):
    
    resultslst = []
    
    for topic in TOPIC_LIST:
        
        ranking = 1
        
        for cur_itemBM25 in BM25_topic_doc_score_list:
        
            for cur_itemSim in Sim_topic_doc_score_list:
        
                if (cur_itemBM25[0] == topic) and (cur_itemSim[0] == topic) and (cur_itemBM25[1][0] == cur_itemSim[1][0]):
                    
                    v = ilambda * cur_itemBM25[1][1] + (1-ilambda) * cur_itemSim[1][1]
                    
                    temp = cur_itemBM25[0] + " " + "QO" + " " + cur_itemBM25[1][0] + " " + str(ranking) + " "  + str(1 - v) + " " + "similarity.tar.title.and.query"
                    
                    resultslst.append(temp)
                    
                    ranking += 1

        print('completed topic ', topic)
        
    dirToWrite = '/home/pfb16181/NetBeansProjects/hedwig/scripts/resultsBM25andSim.%s' % ilambda
    
    with open(dirToWrite, 'w') as f:
        
        for item in resultslst:
            
            f.write("%s\n" % item)

    print('saved result file for lambda param = {}'.format(ilambda))
    print('-----------')
