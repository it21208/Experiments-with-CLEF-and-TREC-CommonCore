# author: alexandros ioannidis
from sentence_transformers import SentenceTransformer, util, models
import scipy.spatial

queriesDict = {}
queries = []
with open('/home/pfb16181/NetBeansProjects/lucene4ir-master/data/TREC-CommonCore/topicsfile') as file_in:
    for idx, line in enumerate(file_in):
        newLine = line.split(" ", 1)
        queries.append(newLine[0]+' '+newLine[1].rstrip())
        queriesDict[newLine[0]+' '+newLine[1].rstrip()] = newLine[0]
print('created queries dictionary')

dictWithPMIDS = {}
list_of_ids = []
corpus = []
with open('/home/pfb16181/common_core_data1855658.tsv') as file_in:
    for line in file_in:
        newLine = line.split(" ", 1)
        if len(line) < 1 or newLine[0] in list_of_ids:
            continue 
        try: 
            list_of_ids.append(newLine[0])
            corpus.append(newLine[1].rstrip())
            dictWithPMIDS[newLine[0]] = newLine[1].rstrip()
        except Exception as e:
            pass

print('corpus size: {}'.format(len(corpus)))
dictForIndexing = dict([(value, key) for key, value in dictWithPMIDS.items()]) # Swap Keys and Values in Dictionary dictWithPMIDS

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
print('saved dictionary with docs and ids')
word_embedding_model = models.Transformer('bert-base-uncased')
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
embedder = SentenceTransformer(modules=[word_embedding_model, pooling_model])
corpus_embeddings = embedder.encode(corpus)
resultslst = []
cnt = 1
for query in queries:
    print('corpus with size {} created for {} query'.format(len(corpus), cnt))
    cnt += 1
    query_embeddings = embedder.encode(query)
    closest_n = 1000  # closest_n = len(list_of_ids)-1
    ranking = 1
    for query_embedding in query_embeddings:
        distances = scipy.spatial.distance.cdist([query_embedding], corpus_embeddings, "cosine")[0]
        results = zip(range(len(distances)), distances)
        results = sorted(results, key=lambda x: x[1])
        for idx, distance in results[0:closest_n]:
            try:
                resultslst.append(str(queriesDict[query]) + " " + "QO" + " " + str(dictForIndexing[corpus[idx]]) + " " + str(
                    ranking) + " " + "%.6f" % (1.00 - distance) + " " + "similarity.tar.title.and.query")
                ranking += 1
            except Exception as e:
                pass
            
with open('/home/pfb16181/NetBeansProjects/hedwig/scripts/resultsFSSVmeanPoolingCommonCore.txt', 'w') as f:
    for item in resultslst:
        f.write("%s\n" % item)
