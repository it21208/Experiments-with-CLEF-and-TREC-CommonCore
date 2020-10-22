from collections import OrderedDict
import operator

TOPICS_LIST = ["307", "310", "321", "325", "330", "336", "341", "344", "345", "347",
                "350", "353", "354", "355", "356", "362", "363", "367", "372", "375",
                "378", "379", "389", "393", "394", "397", "399", "400", "404", "408",
                "414", "416", "419", "422", "423", "426", "427", "433", "435", "436",
                "439", "442", "443", "445", "614", "620", "626", "646", "677", "690"]

reader = open('/home/pfb16181/NetBeansProjects/birch/data/predictions/predict.mb_core17')

d = OrderedDict()
for row in reader:
    splitrow = row.split()
    topic = splitrow[0]
    d[row] = topic
    

newlist = []
for topic in TOPICS_LIST:
    newordereddict = OrderedDict()
    for k, v in d.items():
        if v == topic:
            splitk = k.split()
            newordereddict[" ".join(splitk) + '\n'] = float(splitk[4])
    newlist.append(newordereddict)

for idx, i in enumerate(newlist):
    newlist[idx] = sorted(i.items(), key=operator.itemgetter(1), reverse=True)


newd = OrderedDict()
for dictionary in newlist:
    newd.update(dictionary)


d = OrderedDict()
for k, v in newd.items():
    splitrow = k.split()
    topic = splitrow[0]
    d[k] = topic


newlist2 = []
for topic in TOPICS_LIST:
    rank = 1
    for k, v in d.items():
        if v == topic:
            splitk = k.split()
            splitk[3] = str(rank)
            newlist2.append(" ".join(splitk) + '\n')
            rank += 1

# print(newlist2)        

with open('/home/pfb16181/Downloads/resorted.predict.mb_core17', 'w') as f:
    for item in newlist2:
        f.write("%s" % item)
