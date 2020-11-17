#!/usr/bin/env python
# open up a terminal and run the following chmod +x removeTopicsfromQRELSfile.py
# then you can also execute this script from terminal like this ./removeTopicsfromQRELSfile.py
CLEF_TOPIC_LIST2017 = [
    'CD007431', 'CD008081', 'CD008760', 'CD008782', 'CD008803', 'CD009135', 'CD009185', 'CD009372', 'CD009519', 'CD009551',
    'CD009579', 'CD009647', 'CD009786', 'CD009925', 'CD010023', 'CD010173', 'CD010276', 'CD010339', 'CD010386', 'CD010542',
    'CD010633', 'CD010653', 'CD010705', 'CD010772', 'CD010775', 'CD010783', 'CD010860', 'CD010896', 'CD011145', 'CD012019'
]

CLEF_TOPIC_LIST2018 = [
    'CD008122', 'CD008587', 'CD008759', 'CD008892', 'CD009175', 'CD009263', 'CD009694', 'CD010213', 'CD010296', 'CD010502',
    'CD010657', 'CD010680', 'CD010864', 'CD011053', 'CD011126', 'CD011420', 'CD011431', 'CD011515', 'CD011602', 'CD011686',
    'CD011912', 'CD011926', 'CD012009', 'CD012010', 'CD012083', 'CD012165', 'CD012179', 'CD012216', 'CD012281', 'CD012599'
]

CLEF_TOPIC_LIST = CLEF_TOPIC_LIST2017 + CLEF_TOPIC_LIST2018

with open("/home/pfb16181/NetBeansProjects/birch/data/qrels/qrels.clef1718.txt") as file_in:
    lines = []
    for line in file_in:        
        if line.split()[0] in CLEF_TOPIC_LIST:
            lines.append(line.replace("\t", " "))


seen = set()
result = []
for item in lines:
    if item not in seen:
        seen.add(item)
        result.append(item)

with open('/home/pfb16181/NetBeansProjects/birch/data/qrels/updated.qrels.clef1718.txt', 'w') as filehandle:
    for line in result:
        filehandle.write('%s' % line)

