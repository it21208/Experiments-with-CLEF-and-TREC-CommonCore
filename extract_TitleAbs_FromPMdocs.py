# -*- coding: utf-8 -*-
# author = alexandros ioannidis

from os import listdir
from os.path import isfile, join
import argparse
import xml.dom.minidom
from itertools import islice
import xml.etree.ElementTree as ET
import random
from bs4 import BeautifulSoup
    
train_docs = 500
dev_docs = 300
test_docs = 200

def main(docs_folder, output_folder):
    onlyfiles = [join(docs_folder, f) for f in listdir(
        docs_folder) if isfile(join(docs_folder, f))]
    
    titles_and_abs = []
    for idx, file in enumerate(onlyfiles):
        try:
            xmlstr = open(file).read()
            doc1 = xml.dom.minidom.parse(file)
            title = doc1.getElementsByTagName('ArticleTitle')
            try:
                titleText = title[0].firstChild.data
            except Exception as e:
                titleText = title[0].lastChild.data
            #print(idx, title)
            abstractText = " "
            root_node = ET.parse(file).getroot()
            listElemTags = [elem.tag for elem in root_node.iter()]
            combinedText = ''
            if 'AbstractText' in listElemTags:                    
                for AbstractText in root_node.iter('AbstractText'):
                    abstractText += str(AbstractText.text)                    
                combinedText = titleText + abstractText
            else:            
                combinedText = titleText 
            titles_and_abs.append(combinedText)
        except Exception as e:
            #print(xmlstr)
            print('---------------',e,'---------------')
            #print(title[0].nodeName)
            #print(title[0].firstChild.nodeValue)
            #print(title[0].lastChild.data)
            # if there is an error I might have to check the all childNodes 0, 1, 2, ...
            #print(title[0].firstChild.childNodes[0].data)
            #print(title[0].firstChild.nodeType)
    return(titles_and_abs)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Parse some directory strings params to execute the extraction of PubMed titles and abstracts.')
    
    parser.add_argument("--docs-folder", '-d', type=str,
                        help='path to folder with the desired PubMed XML docs', required=True)
    
    parser.add_argument("--output-folder", '-o', type=str,
                        help='output folder to dump every tsv file into', required=True)

    # argument parse
    args = parser.parse_args()
    docs_folder = args.docs_folder
    output_folder = args.output_folder
    
    combinedTitlesAbstracts = main(docs_folder, output_folder)
    print('Length is {}'.format(len(combinedTitlesAbstracts)))
    
    # split the list in 500 items (train_docs) , 300 items (dev_docs), 200 items (test_docs)
    # list of length in which we have to split 
    length_to_split = [500, 300, 200]     
    
    # Using islice 
    input_combinedTitlesAbstracts = iter(combinedTitlesAbstracts) 
    output = [list(islice(input_combinedTitlesAbstracts, elem)) for elem in length_to_split] 
    
    trainList = output[0]
    devList = output[1]
    testList = output[2]
    
    labels = ['0', '1']
    
    for i in range(length_to_split[0]):
        trainList[i] = random.choice(labels) + "\t" + trainList[i] +'\r'
    
    
    for i in range(length_to_split[1]):
        devList[i] = random.choice(labels) + "\t" + devList[i] +'\r'
        
        
    for i in range(length_to_split[2]):
        testList[i] = random.choice(labels) + "\t" + testList[i] +'\r'
        
    
    ''' store train.tsv '''   
    outfile = open(output_folder+"train.tsv", "w+")
    temp = "\n".join(i for i in trainList)
    outfile.write(temp)
    outfile.close()
    print('train.tsv saved')
    
    ''' store dev.tsv '''  
    outfile = open(output_folder+"dev.tsv", "w+")
    temp = "\n".join(i for i in devList)
    outfile.write(temp)
    outfile.close()
    print('dev.tsv saved')
    
    ''' store test.tsv '''  
    outfile = open(output_folder+"test.tsv", "w+")
    temp = "\n".join(i for i in testList)
    outfile.write(temp)
    outfile.close()
    print('test.tsv saved')
    
    print('Done')
