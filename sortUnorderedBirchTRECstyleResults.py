from collections import OrderedDict

TOPICS_LIST = ["307", "310", "321", "325", "330", "336", "341", "344", "345", "347",
                "350", "353", "354", "355", "356", "362", "363", "367", "372", "375",
                "378", "379", "389", "393", "394", "397", "399", "400", "404", "408",
                "414", "416", "419", "422", "423", "426", "427", "433", "435", "436",
                "439", "442", "443", "445", "614", "620", "626", "646", "677", "690"]

d = OrderedDict()

reader = open('/home/pfb16181/NetBeansProjects/birch/data/predictions/predict.mb_core17')

for row in reader:
    splitrow = row.split()
    topic = splitrow[0]
    d[row] = topic
    
newlist = []
for topic in TOPICS_LIST:
    for k, v in d.items():
        if v == topic:
            newlist.append(k)    

with open('/home/pfb16181/Downloads/sorted.predict.mb_core17', 'w') as f:
    for item in newlist:
        f.write("%s" % item)
