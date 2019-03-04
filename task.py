import re

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

class task():
    def __init__(self,line=None):
        # self.line = '9 INFO gflags_handler.py:288 Gathering logs from all nodes'
        self.line = line

    def searchphrase(self,line):
        isdbg = 0
        isinfo = 0
        iserror = 0
        istime = 0
        isfilename = 0
        line = str(self.line)
        list1 = line.split(sep=" ")
        y = []
        x = []
        # msg = line.split(sep="py:")[1].split(sep=" ",maxsplit=1)[1]
        # for word in list1:
        #     timeregx = '[0-9]+:[0-9]+:[0-9]+\.[0-9]+'
        #     fileregx = '[a-zA-z]+\.py'
        #     if(word == 'INFO'):
        #         isinfo = 1
        #     if(word == 'DBG'):
        #         isdbg = 1
        #     if(word == 'ERROR'):
        #         iserror = 1
        #     x += re.findall(timeregx,word)
        #     if(x):
        #         istime = 1
        #     y += re.findall(fileregx,word.split(sep=":")[0])
        #     if(y) :
        #         isfilename = 1
        #
        #
        # if ( isdbg == 1 ):
        #     if (isfilename == 1):
        #         res = []
        #         for w in y:
        #             res += filename4.find({'name' : w})
        #         x = msg.find({})
        #         collectmsgid = []
        #         for docs in x:
        #             t = re.split(msg,docs['message'])
        #             if t:
        #                 collectmsgid += docs['_id']
        #                 pass

        retrieve = []
        x = db1.collection_names()
        for col in x:
            y = db1[col].find({})
            for docs in y:
                z = re.findall(line, docs['raw'])
                if (z):
                    retrieve.append(docs['raw'])
        x = db2.collection_names()
        for col in x:
            y = db2[col].find({})
            for docs in y:
                z = re.findall(line, docs['raw'])
                if (z):
                    retrieve.append(docs['raw'])
        x = db3.collection_names()
        for col in x:
            y = db3[col].find({})
            for docs in y:
                z = re.findall(line, docs['raw'])
                if (z):
                    retrieve.append(docs['raw'])

        y = db5['trace'].find({})
        for docs in y:
            z = re.findall(line, docs['raw'])
            if (z):
                retrieve.append(docs['raw'])
        #
        #
        # for x in retrieve:
        #     print(x)
        return retrieve

