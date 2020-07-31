# created in june
# author: alexandros ioannidis

import os
import sys
import xml.etree.ElementTree as ET
from lxml import etree
import xml.dom.minidom
from os.path import isfile, join
from os import listdir
import re
from lxml.etree import tostring
from itertools import chain


from xml.etree import ElementTree

# topic_list contains the unique train and test topics of the CLEF TAR e-Health Task 2 from 2017, 2018 and 2019.
# complete CLEF 2017 topics list
TOPIC_LIST_2017 = [
'CD005139','CD005253','CD006715','CD007431','CD007868','CD008018','CD008081','CD008170','CD008201','CD010019','CD010355','CD010502','CD010526','CD010657','CD010680','CD010771',
'CD010772','CD010775','CD010778','CD010783','CD010860','CD010864','CD010896','CD011053','CD011126','CD011145','CD011380','CD011420','CD011431','CD011436','CD011515','CD011571',
'CD011602','CD011686','CD011912','CD011926','CD012009','CD012010','CD012083','CD012120','CD012164','CD012165','CD012179','CD012216','CD012223','CD012281','CD012347','CD012521',
'CD012599','CD012930'
]

# complete CLEF 2018 topics list
TOPIC_LIST_2018 = [
'CD007394','CD007427','CD008054','CD008122','CD008587','CD008643','CD008686','CD008691','CD008759','CD008760','CD008782','CD008803','CD008892','CD009020','CD009135','CD009175',
'CD009185','CD009263','CD009323','CD009372','CD009519','CD009591','CD009579','CD009551','CD009593','CD009647','CD009694','CD009786','CD009925','CD009944','CD010023','CD010173',
'CD010213','CD010276','CD010296','CD010339','CD010386','CD010409','CD010438','CD010542','CD010632','CD010633','CD010653','CD010705','CD011134','CD011548','CD011549','CD011975',
'CD011984','CD012019'
]
# TOPIC_LIST_2018 = ['CD007427']

# complete CLEF 2019 topics list
TOPIC_LIST_2019 = [
'CD000996','CD001261','CD004414','CD006468','CD007867','CD008874','CD009044','CD009069','CD009642','CD010038','CD010239','CD010558','CD010753','CD011140','CD011768','CD011977',
'CD012069','CD012080','CD012233','CD012342','CD012455','CD012551','CD012567','CD012669','CD012768'
]

# 30 topics (test topics) Waterloo 2018 CLEF
TOPIC_LIST_UWA_UWB = [
'CD008122','CD008587','CD008759','CD008892','CD009175','CD009263','CD009694','CD010213','CD010296','CD010502','CD010657','CD010680','CD010864','CD011053','CD011126','CD011420',
'CD011431','CD011515','CD011602','CD011686','CD011912','CD011926','CD012009','CD012010','CD012083','CD012165','CD012179','CD012216','CD012281','CD012599'
]

# 3 topics for quick testing
TOPIC_LIST_UWA_UWBC=['CD008122','CD008759','CD008892']

# 30 topics (test topics) Waterloo 2017 CLEF
TOPIC_LIST_A_B_RANK_THRESH_NORMAL = [
'CD007431','CD008081','CD008760','CD008782','CD008803','CD009135','CD009185','CD009372','CD009519','CD009551',
'CD009579','CD009647','CD009786','CD009925','CD010023','CD010173','CD010276','CD010339','CD010386','CD010542',
'CD010633','CD010653','CD010705','CD010772','CD010775','CD010783','CD010860','CD010896','CD011145','CD012019'
]

# 'CD010705' #'CD007431', 'CD008081', 'CD008760', 'CD008782'
TOPIC_LIST_SMALL=['CD007431','CD008081','CD008760','CD011686','CD008759']
#TOPIC_LIST = TOPIC_LIST_2017+TOPIC_LIST_2018+TOPIC_LIST_2019
#TOPIC_LIST = TOPIC_LIST_2018+TOPIC_LIST_2019

TOPIC_LIST = TOPIC_LIST_2017+TOPIC_LIST_2018+TOPIC_LIST_2019

# some global variables
suf_OUTDIR = '/home/pfb16181/clef_docs/'
fin_OUTDIR = ''
qrels_filepath = '/home/pfb16181/full.train.abs.2017.2018.2019_and_full.test.abs.2019.qrels'
path_to_CLEF_docs = '/home/pfb16181/pubmed_filter_2017_2018_2019/'

def readFeedbackQRELSintoDict(current_topic, qrels_filepath, path_to_CLEF_docs):
    f = open(qrels_filepath, "r")
    topic_qrels_dict = {}
    for line in f:
        topic = line.split()[0]
        if topic == current_topic:
            doc = line.split()[2]
            # relevancy 0 or 1]
            relevancy = line.split()[3]
            if relevancy == '0' or relevancy == '1':
                if relevancy == '0':
                    relevancy = '10'
                else: 
                    relevancy =  '01' # int(relevancy)
            # Check if relevancy is 2 and if yes and make it 1.
            if relevancy == '2' or relevancy == '3' or relevancy == '4':
                # relevancy = '1'
                relevancy = '01'
            temp_key = path_to_CLEF_docs+doc+'.xml'
            temp_dictionary = {temp_key: [relevancy, current_topic]}
            topic_qrels_dict.update(temp_dictionary)
    return(topic_qrels_dict)


def readCLEFtitle_query():
    clef_TQ_list = [] 
    f = open('/home/pfb16181/tar.query6.2017-2019train_and_2019test', 'rt')
    strtxt = f.read()
    clef_TQ_list = strtxt.split('\n')
    del clef_TQ_list[-1]
    clef_TQ_dict = {}
    for topic in clef_TQ_list:
        temp = re.split('\s', topic, 1)
        clef_TQ_dict[temp[0]] = temp[1]
    return(clef_TQ_dict)


def stringify_children(node):
    parts = ([node.text] +  list(chain(*([c.text, tostring(c), c.tail] for c in node.getchildren()))) + [node.tail])
    # filter removes possible Nones in texts and tails
    return ''.join(filter(None, parts))


def main(current_topic, qrels_filepath, path_to_CLEF_docs):
    topic_qrels_dict = readFeedbackQRELSintoDict(current_topic, qrels_filepath, path_to_CLEF_docs)
    # onlyfiles = [join(path_to_CLEF_docs, f) for f in listdir(path_to_CLEF_docs) if isfile(join(path_to_CLEF_docs, f))]    
    
    clef_TQ_dict = readCLEFtitle_query()
    
    mainlistOfLists = []
    
    for key, value in topic_qrels_dict.items():
        combinedText = ''
        
        try:
            
            xmlstr = open(key).read()
            
            try:
                
                tree = etree.parse(key)
                pmid = tree.xpath('//MedlineCitation/PMID[@Version="1"]')
                pmid_str = pmid[0].text
                
                
                doc1 = xml.dom.minidom.parse(key)
                title = doc1.getElementsByTagName('ArticleTitle')            
                                    
                try:
                    titleText = title[0].firstChild.data
                except Exception as e:
                    titleText = title[0].lastChild.data    
                abstractText = " "
                root_node = ET.parse(key).getroot()
                listElemTags = [elem.tag for elem in root_node.iter()]
                if 'AbstractText' in listElemTags:
                    for AbstractText in root_node.iter('AbstractText'):
                        abstractText += str(AbstractText.text)
                    combinedText = pmid_str + ' ' + clef_TQ_dict[topic_qrels_dict[key]
                                                    [1]] + ' ' + titleText + ' ' + abstractText
                else:
                    combinedText = pmid_str + ' ' + clef_TQ_dict[topic_qrels_dict[key]
                                                    [1]] + ' ' + titleText
            except Exception as e:
                # print(xmlstr)
                print('---------------', e, '---------------')      
                combinedText = pmid_str + ' ' + \
                    clef_TQ_dict[topic_qrels_dict[key][1]]
        
        except:
            print('File ' + key + ' does not exist.')
            
            
        mainlistOfLists.append([topic_qrels_dict[key][0], combinedText])
    return(mainlistOfLists)
    
    

if __name__ == "__main__":

    for current_topic in TOPIC_LIST:
        # receive a list of lists, each sublist contains the label of the clef document and a string,
        # each string in a sublist corresponds to a document (concatenated title and abstract)
        listOfLists = main(current_topic, qrels_filepath, path_to_CLEF_docs)
        print('Finished extracting text and labels from clef docs for topic {}'.format(current_topic))
        # percentage_to_split train=50%, dev=30%, test=20%    
        train_end=0.5
        dev_end=0.8        
        train_listOfLists = listOfLists[:int(len(listOfLists)*train_end)]
        dev__listOfLists = listOfLists[int(len(listOfLists)*train_end):int(len(listOfLists)*dev_end)] 
        test_listOfLists = listOfLists[int(len(listOfLists)*dev_end):]
        
        
        # get correct path to save Pubmed docs in a .tsv file for certain clef topic 
        if current_topic in TOPIC_LIST_2017:
            fin_OUTDIR = suf_OUTDIR + '2017/' + current_topic + '/'

        if current_topic in TOPIC_LIST_2018:
            fin_OUTDIR = suf_OUTDIR + '2018/' + current_topic + '/'
            
        if current_topic in TOPIC_LIST_2019:
            fin_OUTDIR = suf_OUTDIR + '2019/' + current_topic + '/'
            
        
        train=0.5
        dev=0.3
        test=0.2
        trainList = []
        devList = []
        testList = []
        for i in range(int(len(listOfLists)*train)):
            temp_train_str = str(train_listOfLists[i][0]) + "\t" + train_listOfLists[i][1] + '\r'
            trainList.append(temp_train_str)
    
        for i in range(int(len(listOfLists)*dev)):
            temp_dev_str = str(dev__listOfLists[i][0]) + "\t" + dev__listOfLists[i][1] + '\r'
            devList.append(temp_dev_str)
        
        for i in range(int(len(listOfLists)*test)):
            temp_test_str = str(test_listOfLists[i][0]) + "\t" + test_listOfLists[i][1] + '\r'
            testList.append(temp_test_str)
        
        print('Finished train, dev and test splits for topic {}'.format(current_topic))
        
        # store train.tsv
        outfile = open(fin_OUTDIR+"train.tsv", "w+")
        temp = "\n".join(i for i in trainList)
        outfile.write(temp)
        outfile.close()
        print('train.tsv saved for {}'.format(current_topic))
        
        # store dev.tsv   
        outfile = open(fin_OUTDIR+"dev.tsv", "w+")
        temp = "\n".join(i for i in devList)
        outfile.write(temp)
        outfile.close()
        print('dev.tsv saved for {}'.format(current_topic))
        
        # store test.tsv
        outfile = open(fin_OUTDIR+"test.tsv", "w+")
        temp = "\n".join(i for i in testList)
        outfile.write(temp)
        outfile.close()
        print('test.tsv saved {}'.format(current_topic))
        print('------------------------------------------')
        
