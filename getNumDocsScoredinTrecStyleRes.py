# import

TOPIC_LIST_UWA_UWB = [
    'CD008122', 'CD008587', 'CD008759', 'CD008892', 'CD009175', 'CD009263', 'CD009694', 'CD010213', 'CD010296', 'CD010502', 
    'CD010657', 'CD010680', 'CD010864', 'CD011053', 'CD011126', 'CD011420', 'CD011431', 'CD011515', 'CD011602', 'CD011686', 
    'CD011912', 'CD011926', 'CD012009', 'CD012010', 'CD012083', 'CD012165', 'CD012179', 'CD012216', 'CD012281', 'CD012599'
]

TOPIC_LIST_A_B_RANK_THRESH_NORMAL = [
    'CD007431', 'CD008081', 'CD008760', 'CD008782', 'CD008803', 'CD009135', 'CD009185', 'CD009372', 'CD009519', 'CD009551',
    'CD009579', 'CD009647', 'CD009786', 'CD009925', 'CD010023', 'CD010173', 'CD010276', 'CD010339', 'CD010386', 'CD010542',
    'CD010633', 'CD010653', 'CD010705', 'CD010772', 'CD010775', 'CD010783', 'CD010860', 'CD010896', 'CD011145', 'CD012019'
]

TOPIC_LIST = TOPIC_LIST_A_B_RANK_THRESH_NORMAL + TOPIC_LIST_UWA_UWB

pathToTrecStyleResults = '/home/pfb16181/RetrievalAppSubset.pubmed5.seedDoc_title_and_query_and_queryExpansion_top20Terms_only_from_rel_docsResults.correct.res'

def readTrecStyleResultsFile(pathToTrecStyleResults):
    
    list_num_pmids_for_topic = []
    
    with open(pathToTrecStyleResults, "r") as f:
        
        try:
            firstline = f.readline()
            cur_topic = firstline.split()[0]
        except:
            print('No lines in file to read')
        
        countDocsPerTopic = 1
        
        try:
            while f:
                previous_topic = cur_topic
                next_line = f.readline()
                # print(next_line, type(next_line), len(next_line))
                cur_topic = next_line.split()[0]
                
                if cur_topic == previous_topic:
                    # increase the counter by 1
                    countDocsPerTopic += 1
                else:
                    # save the topic and the number of documents scored
                    list_num_pmids_for_topic.append([previous_topic, countDocsPerTopic])
                    # reset the document counter for the next topic 
                    countDocsPerTopic = 1
        except:
            list_num_pmids_for_topic.append([previous_topic, countDocsPerTopic])
            print('Reached EOF')
                
    return(list_num_pmids_for_topic)


if __name__ == "__main__":
    
    list_num_pmids_for_topic = readTrecStyleResultsFile(pathToTrecStyleResults)
    
    # for i in list_num_pmids_for_topic:
    #     print(i)
    
    for i in list_num_pmids_for_topic:
        if i[0] in TOPIC_LIST:
            print(i)
