import argparse
import time
import pymongo
import re
def parse_args():
    parser = argparse.ArgumentParser(description="prog to make database",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("file", action="store",
                        help="file name of log file")
    options = parser.parse_args()
    return options

args = parse_args()
def follow(file):
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

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
list1 = db1.list_collection_names()
def update_database():
    logfile = open(args.file,'r')
    loglines = follow(logfile)
    trace=0
    buflist=[]
    for line in loglines:
        print(args.file)
        linelist = line.split(sep=' ',maxsplit=4)
        # case of traceback error
        txt = linelist[0]
        x = re.findall("[0-9]", txt)
        if(linelist[0]=='' or not x):
            linelist = line.split(sep=" ")
            if not trace:
                if(linelist[0]=='Traceback'):
                    trace = 1
                    buflist=[]
            else:
                if ',' not in line:
                    flist = line.split(":")
                    check = errtype.find_one({"errortype": flist[0]})
                    if check ==  None:
                        errtypeidx = errtype.insert_one({ "errortype": flist[0]})
                        err1idx = (errtypeidx.inserted_id)

                    else:
                        err1idx = check['_id']
                    check = error.find_one({"error": flist[1]})
                    if check ==  None:
                        erroridx = error.insert_one({ "error": flist[1]})
                        err2idx = erroridx.inserted_id
                    else:
                        err2idx = check['_id']
                    buflist=map(str,buflist)
                    seq = ','.join(buflist)
                    traceback.insert_one({"errortype":err1idx,"error":err2idx,"seq":seq , 'raw' : line})
                    trace = 0
                    continue
                errfile = linelist[3].split("\"")[1]
                lineno = linelist[5].split(",")[0]
                funcname = linelist[7]
                check = filetrack.find_one({"file":errfile , "lineno" : lineno , "funcname" : funcname})
                if check == None:
                    trackidx = filetrack.insert_one({"file": errfile, "lineno": lineno, "funcname": funcname , 'raw' : line})
                    fileidx = trackidx.inserted_id
                else :
                    fileidx = check['_id']
                buflist.append(fileidx)

            continue
        prog = linelist[3].split(sep=':')[0]
        message = linelist[4].split(sep='\n')[0]
        h,m,s = map(int , linelist[1].split('.')[0].split(':'))
        time = h*3600+m*60+s
        if(linelist[2]=='DBG'):
            progl = filename4.find_one({'name': prog})
            if(progl== None):
                fileidx = filename4.insert_one({'name':prog})
                progidx = fileidx.inserted_id
            else :
                progidx = progl['_id']
            msgl = msg.find_one({'message':message})
            if(msgl==None):
                msgidx = msg.insert_one({ 'message': message})
                messageidx = msgidx.inserted_id
            else:
                messageidx = msgl['_id']
            curr = db1[f"prog{progidx}"]
            curr.insert_one({'date':linelist[0] , 'time' : time  , 'messageidx' : messageidx , 'raw' : line})

        if(linelist[2]=='INFO'):
            progl = filename4.find_one({'name': prog})
            if(progl== None):
                fileidx = filename4.insert_one({'name':prog})
                progidx = fileidx.inserted_id
            else :
                progidx = progl['_id']
            msgl = msg.find_one({'message':message})
            if(msgl==None):
                msgidx = msg.insert_one({ 'message': message})
                messageidx = msgidx.inserted_id
            else:
                messageidx = msgl['_id']
            curr = db2[f"prog{progidx}"]
            curr.insert_one({'date':linelist[0] , 'time' : time  , 'messageidx' : messageidx , 'raw' : line})

        if(linelist[2]=='ERROR'):
            progl = filename4.find_one({'name': prog})
            if(progl== None):
                fileidx = filename4.insert_one({'name':prog})
                progidx = fileidx.inserted_id
            else :
                progidx = progl['_id']
            msgl = msg.find_one({'message':message})
            if(msgl==None):
                msgidx = msg.insert_one({ 'message': message})
                messageidx = msgidx.inserted_id
            else:
                messageidx = msgl['_id']
            curr = db3[f"prog{progidx}"]
            curr.insert_one({'date':linelist[0] , 'time' : time  , 'messageidx' : messageidx , 'raw' : line})
update_database()