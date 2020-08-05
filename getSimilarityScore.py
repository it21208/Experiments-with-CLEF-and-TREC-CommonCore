# author: alexandros ioannidis
''' 
Get similarity scores for the documents of the CLEF 2017, 2018 and 2019 collections using the 125 queries (CLEF Title + processed queries) Application for sentence embeddings: semantic search. We have a corpus with 
various sentences. Then, for a given query sentence, we want to find the most similar sentence in this corpus. This script outputs for various queries the top 5 most similar sentences in the corpus. 
'''
import sys
from sentence_transformers import SentenceTransformer, util, models
import scipy.spatial
import pickle

TOPIC_LIST_2017 = [
    'CD005139', 'CD005253', 'CD006715', 'CD007431', 'CD007868', 'CD008018', 'CD008081', 'CD008170', 'CD008201', 'CD010019', 'CD010355', 'CD010502', 'CD010526', 'CD010657', 'CD010680', 'CD010771',
    'CD010772', 'CD010775', 'CD010778', 'CD010783', 'CD010860', 'CD010864', 'CD010896', 'CD011053', 'CD011126', 'CD011145', 'CD011380', 'CD011420', 'CD011431', 'CD011436', 'CD011515', 'CD011571',
    'CD011602', 'CD011686', 'CD011912', 'CD011926', 'CD012009', 'CD012010', 'CD012083', 'CD012120', 'CD012164', 'CD012165', 'CD012179', 'CD012216', 'CD012223', 'CD012281', 'CD012347', 'CD012521',
    'CD012599', 'CD012930'
]
# complete CLEF 2018 topics list
TOPIC_LIST_2018 = [
    'CD007394', 'CD007427', 'CD008054', 'CD008122', 'CD008587', 'CD008643', 'CD008686', 'CD008691', 'CD008759', 'CD008760', 'CD008782', 'CD008803', 'CD008892', 'CD009020', 'CD009135', 'CD009175',
    'CD009185', 'CD009263', 'CD009323', 'CD009372', 'CD009519', 'CD009591', 'CD009579', 'CD009551', 'CD009593', 'CD009647', 'CD009694', 'CD009786', 'CD009925', 'CD009944', 'CD010023', 'CD010173',
    'CD010213', 'CD010276', 'CD010296', 'CD010339', 'CD010386', 'CD010409', 'CD010438', 'CD010542', 'CD010632', 'CD010633', 'CD010653', 'CD010705', 'CD011134', 'CD011548', 'CD011549', 'CD011975',
    'CD011984', 'CD012019'
]

# complete CLEF 2019 topics list
TOPIC_LIST_2019 = [
    'CD000996', 'CD001261', 'CD004414', 'CD006468', 'CD007867', 'CD008874', 'CD009044', 'CD009069', 'CD009642', 'CD010038', 'CD010239', 'CD010558', 'CD010753', 'CD011140', 'CD011768', 'CD011977',
    'CD012069', 'CD012080', 'CD012233', 'CD012342', 'CD012455', 'CD012551', 'CD012567', 'CD012669', 'CD012768'
]
# 30 topics (test topics) Waterloo 2018 CLEF
TOPIC_LIST_UWA_UWB = [
    'CD008122', 'CD008587', 'CD008759', 'CD008892', 'CD009175', 'CD009263', 'CD009694', 'CD010213', 'CD010296', 'CD010502', 'CD010657', 'CD010680', 'CD010864', 'CD011053', 'CD011126', 'CD011420',
    'CD011431', 'CD011515', 'CD011602', 'CD011686', 'CD011912', 'CD011926', 'CD012009', 'CD012010', 'CD012083', 'CD012165', 'CD012179', 'CD012216', 'CD012281', 'CD012599'
]
# 3 topics for quick testing
TOPIC_LIST_UWA_UWBC = ['CD008122', 'CD008759', 'CD008892']
# 30 topics (test topics) Waterloo 2017 CLEF
TOPIC_LIST_A_B_RANK_THRESH_NORMAL = [
    'CD007431', 'CD008081', 'CD008760', 'CD008782', 'CD008803', 'CD009135', 'CD009185', 'CD009372', 'CD009519', 'CD009551',
    'CD009579', 'CD009647', 'CD009786', 'CD009925', 'CD010023', 'CD010173', 'CD010276', 'CD010339', 'CD010386', 'CD010542',
    'CD010633', 'CD010653', 'CD010705', 'CD010772', 'CD010775', 'CD010783', 'CD010860', 'CD010896', 'CD011145', 'CD012019'
]


# TOPIC_LIST = TOPIC_LIST_2017 + TOPIC_LIST_2018 + TOPIC_LIST_2019
# TOPIC_LIST = TOPIC_LIST_UWA_UWB  # 2018 test collection
TOPIC_LIST = TOPIC_LIST_A_B_RANK_THRESH_NORMAL  # 2017 test collection

# pathToCorpus = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/merged/new.tsv'
pathToCorpus = '/home/pfb16181/clef_docs/merged_files/new_removedLinesNotStartingWithNumbersAndLinesWithLessThan3chars.tsv'
# Query sentences:
pathToQueries = '/home/pfb16181/tar.query6.2017-2019train_and_2019test'


def save_obj(obj, name):
    with open('/home/pfb16181/NetBeansProjects/hedwig/scripts/' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def readInitialRanking(filename):    
    list_of_pmids_for_topic = []
    record = False
    with open(filename, "r") as f:
        while f:
            line = f.readline()
            if not line:
                break
            if record == True:
                list_of_pmids_for_topic.append(line.strip())
            if line.startswith("Pids:"):
                record = True
    return(list_of_pmids_for_topic)



queriesDict = {}
queries = []
with open(pathToQueries) as file_in:
    for idx, line in enumerate(file_in):
        newLine = line.split(" ", 1)
        queries.append(newLine[0]+' '+newLine[1].rstrip())
        queriesDict[newLine[0]+' '+newLine[1].rstrip()] = newLine[0]
print('loaded queries')
print('created queries dictionary')

dictWithPMIDS = {}
tempList = []
with open(pathToCorpus) as file_in:
    corpus = []
    for line in file_in:
        newLine = line.split(" ", 1)
        if len(line) <= 4 or newLine[0] in tempList:
            continue 
        tempList.append(newLine[0])
        corpus.append(newLine[1].rstrip())
        dictWithPMIDS[newLine[0]] = newLine[1].rstrip()
print('corpus size: {}'.format(len(corpus)))
print('corpus loaded')

for i in queries:
    for idx, j in enumerate(corpus):
        if i.split(" ", 1)[1] in j:
            corpus[idx] = j.replace(i.split(" ", 1)[1], '')
print('removed from corpus the clef topic title prefixes')

for i in queries:
    for idx, (k, v) in enumerate(dictWithPMIDS.items()):
        if i.split(" ", 1)[1] in v:
            dictWithPMIDS[k] = v.replace(i.split(" ", 1)[1], '')
print('removed from dictWithPMIDS the clef topic title prefixes')


# Swap Keys and Values in Dictionary dictWithPMIDS
new_dictWithPMIDS = dict([(value, key) for key, value in dictWithPMIDS.items()])
save_obj(new_dictWithPMIDS, 'new_dictWithPMIDS')
print('saved dictionary with docs and pmids')


corpus125 = {}
resultslst = []

print(queries)

for query in queries:
    
    dictForIndexing = {}
    
      
    # Use BERT for mapping tokens to embeddings
    word_embedding_model = models.Transformer('bert-base-uncased')
    # Apply mean pooling to get one fixed sized sentence vector
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    embedder = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    
    # embedder = SentenceTransformer('bert-base-nli-mean-tokens')
    list_of_pmids_for_topic = readInitialRanking("/home/pfb16181/NetBeansProjects/hedwig/scripts/all.topics2017_2018_2019/"+query.split(" ", 1)[0])
    print('size of corpus for topic {}: {}'.format(query.split(" ", 1)[0], len(list_of_pmids_for_topic)))
    
    corpus125[query.split(" ", 1)[0]] = []
    for pmid in list_of_pmids_for_topic:
        try:
            corpus125[query.split(" ", 1)[0]].append(dictWithPMIDS[pmid])
            dictForIndexing[dictWithPMIDS[pmid]] = pmid
        except:
            pass
            
    cur_corpus = corpus125[query.split(" ", 1)[0]]
    cur_corpus = list(dict.fromkeys(cur_corpus))
    
    def removeDuplicateValuesFromDict(dictForIndexing):
        seen = set()
        for key in dictForIndexing.keys():
            value = tuple(dictForIndexing[key])
            if value in seen:
                del dictForIndexing[key]
            else:
                seen.add(value)
        return(dictForIndexing)
    
    
    dictForIndexing = removeDuplicateValuesFromDict(dictForIndexing)

    print('corpus with size {} created'.format(len(cur_corpus)))
    
    corpus_embeddings = embedder.encode(cur_corpus)
    query_embeddings = embedder.encode(query)
    
    # Find the closest 50 sentences of the corpus for each query sentence based on cosine similarity
    closest_n = len(list_of_pmids_for_topic)-1
    ranking = 1
    for query_embedding in query_embeddings:
        distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]
        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])
        
        for idx, distance in results[0:closest_n]:
            try:
                # temp = str(queriesDict[query]) + " " + "QO" + " " + str(new_dictWithPMIDS[corpus[idx]]) + " " + str(ranking) + " "  + "%.6f" % (1.00 - distance) + " " + "similarity.tar.title.and.query"
                temp = str(queriesDict[query]) + " " + "QO" + " " + str(dictForIndexing[cur_corpus[idx]]) + " " + str(ranking) + " "  + "%.6f" % (1.00 - distance) + " " + "similarity.tar.title.and.query"
                resultslst.append(temp)
                ranking += 1
            except:
                pass
    
    print('-------------------------------------------------')
    # break
            
# dirToWrite = '/home/pfb16181/NetBeansProjects/hedwig/scripts/results.txt'
dirToWrite = '/home/pfb16181/NetBeansProjects/hedwig/scripts/results2.txt'
with open(dirToWrite, 'w') as f:
    for item in resultslst:
        f.write("%s\n" % item)
            
    # sys.exit()

print('Done')
