
pathToTopics = "/home/pfb16181/NetBeansProjects/lucene4ir-master/data/TREC-CommonCore/307-690.topics"
pathToSave = "/home/pfb16181/NetBeansProjects/lucene4ir-master/data/TREC-CommonCore/topicsfile"


file = open(pathToTopics, 'r')
Lines = file.readlines()

tempList = ["" for i in range(50)]
idx = 0
flagdesc = False
flagnarr = False
for line in Lines:
    newline = line.strip()
    
    if flagdesc == True:
        tempList[idx] += newline + " "
        flagdesc = False
    
    if flagnarr == True: 
        tempList[idx] += newline + " "
        flagnarr = False
        
    if newline.partition(' ')[0] == "</top>":
        idx += 1
        
    if newline.partition(' ')[0] == "<num>":
        tempList[idx] += line.partition(':')[2].strip()+" "
    
    if newline.partition(' ')[0] == "<title>":
        tempList[idx] += line.partition(' ')[2].strip()+" "
        
    if newline.partition(' ')[0] == "<desc>":
        flagdesc = True
        
    if newline.partition(' ')[0] == "<narr>":
        flagnarr = True
    
with open(pathToSave, 'w') as f:
    for item in tempList:
        f.write("%s\n" % item)
