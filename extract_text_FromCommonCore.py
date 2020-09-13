# -*- coding: utf-8 -*-
# author = alexandros ioannidis

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
    

def main(docs_folder, output_folder):
    onlyfiles = [join(docs_folder, f) for f in listdir(docs_folder) if isfile(join(docs_folder, f))]
    
    titles_and_abs = []
    countNoAbs = 0
    
    cnt = 1 
    for idx, file in enumerate(onlyfiles):
        combinedText = ''
        xmlstr = open(file).read()
        tree = etree.parse(file)
        doc1 = xml.dom.minidom.parse(file)
        docid = doc1.getElementsByTagName('doc-id')
        
        try:
            docidattrib = docid[0].getAttribute('id-string')
            combinedText += docidattrib+' '
        except Exception as e:
            cnt += 1
            continue
        
        title = doc1.getElementsByTagName('hl1')
        try:
            titleText = title[0].firstChild.nodeValue
        except Exception as e:
            pass
        
        combinedText += titleText+' '
        
        abstract = doc1.getElementsByTagName('block')
        
        try:
            if abstract[0].getAttribute('class') == 'lead_paragraph':
                abstractText = ""
                for j in abstract[0].childNodes:
                    if j.firstChild is not None:
                        abstractText += " "+j.firstChild.nodeValue
        except Exception as e:
            pass
            
        combinedText += abstractText+' '       
            
        titles_and_abs.append(combinedText)
        
    print('missed {} xml docs'.format(cnt))
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
    outfile = open(output_folder+"common_core_data.tsv", "w+")
    temp = "\n".join(i for i in combinedTitlesAbstracts)
    outfile.write(temp)
    outfile.close()
    print('common_core_data.tsv saved')
