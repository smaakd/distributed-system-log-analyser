# import re
#
# timeregx = ['[0-9]+:[0-9]+:[0-9]+\.[0-9]+' , 'INFO']
#
# time = '2019-03-03 13:18:40.925259 INFO gflags_handler.py:288 Gathering logs from all nodes'
# x=[]
# for regex in timeregx:
#     x = x + re.findall(regex,time)
# print(x)


import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db1 = client["dbg"]
db2 = client["info"]
db3 = client["error"]
db4 = client['gen']
db5 = client['traceback']

filetrack = db5['filetrack']
errtype = db5['errortype']
error = db5['error']
traceback = db5['trace']
filename4 = db4["filename"]
msg = db4["message"]
x = db1.collection_names()
for col in x:
    y = db1[col].find({})
    for docs in y:
        print(docs['raw'])
