import os
from os.path import isfile, join
from os import listdir
from itertools import islice

# split for 2017 or 2018 clef collection
numTrain2017or2018Topics = 20
numDev2017or2018Topics = 5
numTest2017or2018Topics = 25

# split for 2019 collection
numTrain2019Topics = 7
numDev2019Topics = 4
numTestn2019Topics = 14


pathTo2017Topics = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/2017'
pathTo2018Topics = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/2018'
pathTo2019Topics = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/2019'

pathToWriteTrainDevTestfor2017Topics = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/concatenated_2017'
pathToWriteTrainDevTestfor2018Topics = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/concatenated_2018'
pathToWriteTrainDevTestfor2019Topics = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/concatenated_2019'

nameOfTrainFiles = 'train.tsv'
nameOfDevFiles = 'dev.tsv'
nameOfTestFiles = 'test.tsv'

OUTDIR2017 = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/concatenated_2017'
OUTDIR2018 = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/concatenated_2018'
OUTDIR2019 = '/home/pfb16181/NetBeansProjects/hedwig-data/datasets/Pubmed/clef_docs/concatenated_2019'


length_to_splitFor2017_2018 = [numTrain2017or2018Topics, numDev2017or2018Topics, numTest2017or2018Topics]
length_to_splitFor2019 = [numTrain2019Topics, numDev2019Topics, numTestn2019Topics]

# --------------------------------------------------------------------------------
onlyfiles = [join(pathTo2017Topics, f) for f in listdir(pathTo2017Topics)]
output = [list(islice(onlyfiles, elem)) for elem in length_to_splitFor2017_2018]

trainList = output[0]
devList = output[1]
testList = output[2]

saveLinesTrainList = []
for i in trainList:
    f = open(i+'/'+nameOfTrainFiles, "r")
    for line in f:
        line = line.strip('\n')
        saveLinesTrainList.append(line)
saveLinesTrainList = list(filter(None, saveLinesTrainList))
saveLinesTrainList = filter(lambda item: item.strip(), saveLinesTrainList)

saveLinesDevList = []
for i in devList:
    f = open(i+'/'+nameOfDevFiles, "r")
    for line in f:
        line = line.strip('\n')
        saveLinesDevList.append(line)
saveLinesDevList = list(filter(None, saveLinesDevList))
saveLinesDevList = filter(lambda item: item.strip(), saveLinesDevList)


saveLinesTestList = []
for i in testList:
    f = open(i+'/'+nameOfTestFiles, "r")
    for line in f:
        line = line.strip('\n')
        saveLinesTestList.append(line)
saveLinesTestList = list(filter(None, saveLinesTestList))
saveLinesTestList = filter(lambda item: item.strip(), saveLinesTestList)

# store train.tsv
saveLinesTrainList = list(filter(None, saveLinesTrainList))
outfile = open(OUTDIR2017+"/train.tsv", "w+")
temp = "\n".join(i for i in saveLinesTrainList)
outfile.write(temp)
outfile.close()
print('train.tsv saved for 2017')

# store dev.tsv
saveLinesTrainList = list(filter(None, saveLinesTrainList))
outfile = open(OUTDIR2017+"/dev.tsv", "w+")
temp = "\n".join(i for i in saveLinesDevList)
outfile.write(temp)
outfile.close()
print('dev.tsv saved for 2017')

# store test.tsv
outfile = open(OUTDIR2017+"/test.tsv", "w+")
temp = "\n".join(i for i in saveLinesTestList)
outfile.write(temp)
outfile.close()
print('test.tsv saved 2017')
print('------------------------------------------')

# --------------------------------------------------------------------------------
onlyfiles = [join(pathTo2018Topics, f) for f in listdir(pathTo2018Topics)] 
output = [list(islice(onlyfiles, elem)) for elem in length_to_splitFor2017_2018]

trainList = output[0]
devList = output[1]
testList = output[2]


saveLinesTrainList = []
for i in trainList:
    f = open(i+'/'+nameOfTrainFiles, "r")
    for line in f:
        line = line.strip('\n')
        saveLinesTrainList.append(line)
saveLinesTrainList = list(filter(None, saveLinesTrainList))
saveLinesTrainList = filter(lambda item: item.strip(), saveLinesTrainList)


saveLinesDevList = []
for i in devList:
    f = open(i+'/'+nameOfDevFiles, "r")
    for line in f:
        line = line.strip('\n')
        saveLinesDevList.append(line)
saveLinesDevList = list(filter(None, saveLinesDevList))
saveLinesDevList = filter(lambda item: item.strip(), saveLinesDevList)


saveLinesTestList = []
for i in testList:
    f = open(i+'/'+nameOfTestFiles, "r")
    for line in f:
        line = line.strip('\n')
        saveLinesTestList.append(line)
saveLinesTestList = list(filter(None, saveLinesTestList))
saveLinesTestList = filter(lambda item: item.strip(), saveLinesTestList)

# store train.tsv
outfile = open(OUTDIR2018+"/train.tsv", "w+")
temp = "\n".join(i for i in saveLinesTrainList)
outfile.write(temp)
outfile.close()
print('train.tsv saved for 2018')

# store dev.tsv
outfile = open(OUTDIR2018+"/dev.tsv", "w+")
temp = "\n".join(i for i in saveLinesDevList)
outfile.write(temp)
outfile.close()
print('dev.tsv saved for 2018')

# store test.tsv
outfile = open(OUTDIR2018+"/test.tsv", "w+")
temp = "\n".join(i for i in saveLinesTestList)
outfile.write(temp)
outfile.close()
print('test.tsv saved 2018')
print('------------------------------------------')

# --------------------------------------------------------------------------------

onlyfiles = [join(pathTo2019Topics, f) for f in listdir(pathTo2019Topics)]
output = [list(islice(onlyfiles, elem)) for elem in length_to_splitFor2019]

trainList = output[0]
devList = output[1]
testList = output[2]

saveLinesTrainList = list(filter(None, saveLinesTrainList))
saveLinesTrainList = []
for i in trainList:
    f = open(i+'/'+nameOfTrainFiles, "r")
    for line in f:
        line = line.strip('\n')
        saveLinesTrainList.append(line)
saveLinesTrainList = list(filter(None, saveLinesTrainList))
saveLinesTrainList = filter(lambda item: item.strip(), saveLinesTrainList)

saveLinesDevList = []
for i in devList:
    f = open(i+'/'+nameOfDevFiles, "r")
    for line in f:
        line = line.strip('\n')
        saveLinesDevList.append(line)
saveLinesDevList = list(filter(None, saveLinesDevList))
saveLinesDevList = filter(lambda item: item.strip(), saveLinesDevList)


saveLinesTestList = []
for i in testList:
    f = open(i+'/'+nameOfTestFiles, "r")
    for line in f:
        line = line.strip('\n')
        saveLinesTestList.append(line)
saveLinesTestList = list(filter(None, saveLinesTestList))
saveLinesTestList = filter(lambda item: item.strip(), saveLinesTestList)

# store train.tsv
outfile = open(OUTDIR2019 + "/train.tsv", "w+")
temp = "\n".join(i for i in saveLinesTrainList)
outfile.write(temp)
outfile.close()
print('train.tsv saved for 2019')

# store dev.tsv
outfile = open(OUTDIR2019+"/dev.tsv", "w+")
temp = "\n".join(i for i in saveLinesDevList)
outfile.write(temp)
outfile.close()
print('dev.tsv saved for 2019')

# store test.tsv
outfile = open(OUTDIR2019+"/test.tsv", "w+")
temp = "\n".join(i for i in saveLinesTestList)
outfile.write(temp)
outfile.close()
print('test.tsv saved 2019')

