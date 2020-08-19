# author: alexandros ioannidis
import sys
from sentence_transformers import SentenceTransformer, util, models
import scipy.spatial
import pickle
from collections import OrderedDict
import operator

pathToCorpus = '/home/pfb16181/clef_docs/merged_files/new_removedLinesNotStartingWithNumbersAndLinesWithLessThan3chars.tsv'
pathToQueries = '/home/pfb16181/tar.query6.2017-2019train_and_2019test'
# pathToQueries = '/home/pfb16181/tar.query6.2017-2019train_and_2019test_T_Q_QE'

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

for idx, j in enumerate(corpus):
    corpus[idx] = j.split('.')
print('split documents into sentences in corpus data structure')

for idx, (k, v) in enumerate(dictWithPMIDS.items()):
    dictWithPMIDS[k] = v.split('.')
print('split documents into sentences in dictWithPMIDS data structure')

New_dictWithPMIDS = {}
for k, v in dictWithPMIDS.items():
    for i in v:
        New_dictWithPMIDS[i] = k
print('created dictionary New_dictWithPMIDS to relate sentences with pmids')

corpus125 = {}
resultslst = []
print('======================================================')
for query in queries:
    dictForIndexing = {}
    # Use BERT for mapping tokens to embeddings - Apply mean pooling to get one fixed s0ized sentence vector
    word_embedding_model = models.Transformer('bert-base-uncased')
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    embedder = SentenceTransformer(modules=[word_embedding_model, pooling_model])
    # embedder = SentenceTransformer('bert-base-nli-mean-tokens')
    list_of_pmids_for_topic = readInitialRanking("/home/pfb16181/NetBeansProjects/hedwig/scripts/all.topics2017_2018_2019/"+query.split(" ", 1)[0])
    print('size of corpus for topic {}: {}'.format(query.split(" ", 1)[0], len(list_of_pmids_for_topic)))
    corpus125[query.split(" ", 1)[0]] = []
    for pmid in list_of_pmids_for_topic:
        try:
            corpus125[query.split(" ", 1)[0]].append(dictWithPMIDS[pmid]) 
            # dictForIndexing[dictWithPMIDS[pmid]] = pmid
        except:
            pass
    cur_corpus = [item for sublist in corpus125[query.split(" ", 1)[0]] for item in sublist]
    cur_corpus = list(dict.fromkeys(cur_corpus))
    print('corpus with {} sentences created'.format(len(cur_corpus)))
    def removeDuplicateValuesFromDict(dictForIndexing):
        seen = set()
        for key in dictForIndexing.keys():
            value = tuple(dictForIndexing[key])
            if value in seen:  del dictForIndexing[key]
            else: seen.add(value)
        return(dictForIndexing)
    # New_dictWithPMIDS = removeDuplicateValuesFromDict(New_dictWithPMIDS)
    print('length New_dictWithPMIDS: ', len(New_dictWithPMIDS))
    corpus_embeddings = embedder.encode(cur_corpus)
    print('corpus embeddings created for topic {}'.format(query.split(" ", 1)[0]))
    query_embeddings = embedder.encode(query)
    print('query embeddings created for topic {}'.format(query.split(" ", 1)[0]))
    closest_n = len(list_of_pmids_for_topic)-1
    ranking = 1
    savedPMIDSwithTheirAggregatedSentenceScores = OrderedDict()  # declare ordered dictionary
    for query_embedding in query_embeddings:
        distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]
        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])
        for idx, distance in results[0:closest_n]:
            try:
                if New_dictWithPMIDS[cur_corpus[idx]] in savedPMIDSwithTheirAggregatedSentenceScores:
                    # aggregate the sentences scores of each doc
                    # get maximum sentence score
                    if savedPMIDSwithTheirAggregatedSentenceScores[New_dictWithPMIDS[cur_corpus[idx]]] < distance: 
                        savedPMIDSwithTheirAggregatedSentenceScores[New_dictWithPMIDS[cur_corpus[idx]]] =  distance
                else:
                    # initialise ordered dictionary with zeros to aggregate the sentences scores for each doc
                    savedPMIDSwithTheirAggregatedSentenceScores[New_dictWithPMIDS[cur_corpus[idx]]] =  distance
                # print(New_dictWithPMIDS[cur_corpus[idx]], 1.00 - distance)
            except:
                pass
    print('created savedPMIDSwithTheirAggregatedSentenceScores dictionary')
    
    sorted_d = dict(sorted(savedPMIDSwithTheirAggregatedSentenceScores.items(), key=operator.itemgetter(1),reverse=True))
    # for k, v in savedPMIDSwithTheirAggregatedSentenceScores.items():
    for k, v in sorted_d.items():
        try:
            temp = str(queriesDict[query]) + " " + "QO" + " " + k + " " + str(ranking) + " "  + str(1 - v) + " " + "similarity.tar.title.and.query"
            resultslst.append(temp)
            ranking += 1
        except:
            pass
    print('-------------------------------------------------')
    # break
    
dirToWrite = '/home/pfb16181/NetBeansProjects/hedwig/scripts/results5.txt'
with open(dirToWrite, 'w') as f:
    for item in resultslst:
        f.write("%s\n" % item)
