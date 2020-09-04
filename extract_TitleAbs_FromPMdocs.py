# -*- coding: utf-8 -*-
# author = alexandros ioannidis

# indexing schema 2+MHLMTA that means indexing multiple fields Title, Abstract, PMID, 
# Authors, Journal Title, Year, Mesh Heading list, MedlineTA! In the 1_FSSV-mean_pooling T+Q+QE strategy we only use the Title and the Abstract of the parsed documents 

from os import listdir
from os.path import isfile, join
import argparse
import xml.dom.minidom
from itertools import islice
import xml.etree.ElementTree as ET
import random
from lxml import etree
from bs4 import BeautifulSoup
import sys
    
# train_docs = 500
# dev_docs = 300
# test_docs = 200


def main(docs_folder, output_folder):
    onlyfiles = [join(docs_folder, f) for f in listdir(docs_folder) if isfile(join(docs_folder, f))]
    
    titles_and_abs = []
    countNoAbs = 0
    
    for idx, file in enumerate(onlyfiles):
        combinedText = ' '
        try:
            xmlstr = open(file).read()
            try:
                tree = etree.parse(file)
                pmid = tree.xpath('//MedlineCitation/PMID[@Version="1"]')
                pmid_str = pmid[0].text
                
                doc1 = xml.dom.minidom.parse(file)
                title = doc1.getElementsByTagName('ArticleTitle')
                
                # parsing Title
                try:
                    titleText = title[0].firstChild.data
                except:
                    titleText = title[0].lastChild.data
                
                # parsing year field
                try:
                    year = doc1.getElementsByTagName('Year')
                    yearText = year[0].firstChild.nodeValue
                except:
                    print('Could not parse year field for file ', file)
                
                combinedText += ' '+yearText

                #  parsing Journal title field
                try:
                    journalTitle = doc1.getElementsByTagName('Title')
                    journalTitleText = journalTitle[0].firstChild.nodeValue
                except:
                    print('Could not parse Journal title field for file ', file)
                
                combinedText += ' '+journalTitleText
                
                # parsing Author List field
                try:
                    authorList = doc1.getElementsByTagName('AuthorList')
                    authorListText = authorList[0].firstChild.nodeValue
                except:
                    print('Could not parse Author List field for file ', file)
                
                combinedText = ' '+authorListText
                
                # parsing Mesh Heading List
                try:
                    meshHeadingList = doc1.getElementsByTagName('MeshHeading')
                    xLen = meshHeadingList.length
                    meshHeadingListText = " "
                    for i in range(xLen):
                        cnt = 1
                        for j in meshHeadingList[i].childNodes:
                            if cnt == 2:
                                meshHeadingListText  += " "+j.firstChild.nodeValue
                            cnt += 1
                except:
                    print('Could not parse Mesh Heading List field for file ', file)
                
                combinedText = ' '+meshHeadingListText
                
                # parsing MedlineTA
                try:
                    medlineTA = doc1.getElementsByTagName('MedlineTA')
                    MedlineTAText = medlineTA[0].firstChild.nodeValue
                except: 
                    print('Could not parse MedlineTA field for file ', file)
                
                combinedText = ' '+MedlineTAText
                
                
                abstractText = " "
                root_node = ET.parse(file).getroot()
                listElemTags = [elem.tag for elem in root_node.iter()]
                
                if 'AbstractText' in listElemTags:                    
                    for AbstractText in root_node.iter('AbstractText'):
                        abstractText += str(AbstractText.text)                           
                    combinedText = pmid_str + ' ' + titleText + ' ' + abstractText + combinedText
                else:            
                    combinedText = pmid_str + ' ' + titleText + combinedText
            
            except:
                try:
                    combinedText = pmid_str + ' ' + titleText + combinedText
                    countNoAbs += 1
                    print(countNoAbs, 'From file ', file, 'could not extract abstract')
                except:
                    combinedText = pmid_str + ' ' + combinedText
                    print('From file ', file, 'could not extract title & abstract')
                
        except:
            print('File ' + file + 'does not exist.')

        titles_and_abs.append(combinedText)
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
    
    '''
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
    '''    
    
    ''' store train.tsv '''   
    # outfile = open(output_folder+"train.tsv", "w+")
    # temp = "\n".join(i for i in trainList)
    # outfile.write(temp)
    # outfile.close()
    # print('train.tsv saved')
    
    ''' store dev.tsv '''  
    # outfile = open(output_folder+"dev.tsv", "w+")
    # temp = "\n".join(i for i in devList)
    # outfile.write(temp)
    # outfile.close()
    # print('dev.tsv saved')
    
    ''' store test.tsv '''  
    # outfile = open(output_folder+"test.tsv", "w+")
    # temp = "\n".join(i for i in testList)
    # outfile.write(temp)
    # outfile.close()
    # print('test.tsv saved')
    
    outfile = open(output_folder+"2MHLMTA_data.tsv", "w+")
    temp = "\n".join(i for i in combinedTitlesAbstracts)
    outfile.write(temp)
    outfile.close()
    print('2MHLMTA_data.tsv saved')
