#  author: alexandros ioannidis
import os
import csv

testfile2017 = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/concatenated_2017/test.tsv'
testfile2018 = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/concatenated_2018/test.tsv'
testfile2019 = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/concatenated_2019/test.tsv'

count_docs2017test = 0
count_relevant_docs2017test = 0
with open(testfile2017) as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for line in reader:
        if line[0] == '01':
            count_relevant_docs2017test += 1
            count_docs2017test += 1
        else:
            count_docs2017test += 1

print('For the 2017 CLEF testing collection (25 topics)')
print('The total number of relevant documents in the 2017 CLEF test collection {}'.format(count_relevant_docs2017test))
print('The total number of documents in the 2017 CLEF collection is {}'.format(count_docs2017test))
print('When Relevant documents are classified correctly as Relevant the loss function will be rewarded with {}'.format( count_docs2017test/count_relevant_docs2017test) )
print('When Relevant documents are classified correctly as Relevant the loss function will be penaltised with {}'.format( -(count_docs2017test/count_relevant_docs2017test) ) )
print('When a Non Relevant document is classified correctly as Non Relevant the loss function will be rewarded with {} '.format( (count_docs2017test/count_relevant_docs2017test)/100 ) )
print('When a Non Relevant document is classified correctly as Relevant the loss function will be penaltised with {} '.format( -(count_docs2017test/count_relevant_docs2017test)/100 ) )


print('----------------------------------------------------------------')


count_docs2018test = 0
count_relevant_docs2018test = 0
with open(testfile2018) as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for line in reader:
        if line[0] == '01':
            count_relevant_docs2018test += 1
            count_docs2018test += 1
        else:
            count_docs2018test += 1


print('For the 2018 CLEF testing collection (25 topics)')
print('The total number of relevant documents in the 2017 CLEF test collection {}'.format(count_relevant_docs2018test))
print('The total number of documents in the 2017 CLEF collection is {}'.format(count_docs2018test))
print('When Relevant documents are classified correctly as Relevant the loss function will be rewarded with {}'.format(count_docs2018test/count_relevant_docs2018test))
print('When Relevant documents are classified correctly as Relevant the loss function will be penaltised with {}'.format( -(count_docs2018test/count_relevant_docs2018test) ))
print('When a Non Relevant document is classified correctly as Non Relevant the loss function will be rewarded with {} '.format( (count_docs2018test/count_relevant_docs2018test)/100 ) )
print('When a Non Relevant document is classified correctly as Relevant the loss function will be penaltised with {} '.format(  -(count_docs2018test/count_relevant_docs2018test)/100 ) )
        
print('----------------------------------------------------------------')

        
count_docs2019test = 0
count_relevant_docs2019test = 0
with open(testfile2019) as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for line in reader:
        if line[0] == '01':
            count_relevant_docs2019test += 1
            count_docs2019test += 1
        else:
            count_docs2019test += 1


print('For the 2019 CLEF testing collection (14 topics)')
print('The total number of relevant documents in the 2019 CLEF test collection {}'.format(count_relevant_docs2019test))
print('The total number of documents in the 2019 CLEF collection is {}'.format(count_docs2019test))
print('When Relevant documents are classified correctly as Relevant the loss function will be rewarded with {}'.format( count_docs2019test/count_relevant_docs2019test) )
print('When Relevant documents are classified correctly as Relevant the loss function will be penaltised with {}'.format( -(count_docs2019test/count_relevant_docs2019test) ) )
print('When a Non Relevant document is classified correctly as Non Relevant the loss function will be rewarded with {} '.format( (count_docs2019test/count_relevant_docs2019test)/100 ) )
print('When a Non Relevant document is classified correctly as Relevant the loss function will be penaltised with {} '.format( -(count_docs2019test/count_relevant_docs2019test)/100 ) )
