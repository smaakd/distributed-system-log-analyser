import os
import pymongo
from multiprocessing import Pool , Value
client = pymongo.MongoClient('mongodb://localhost:27017/')
db1 = client["dbg"]
list = db1.list_collection_names()
for name in list:
    db1.drop_collection(name)

db2 = client["info"]
list = db2.list_collection_names()
for name in list:
    db2.drop_collection(name)

db3 = client["error"]
list = db3.list_collection_names()
for name in list:
    db3.drop_collection(name)
db4 = client['gen']
list = db4.list_collection_names()
for name in list:
    db4.drop_collection(name)
db5 = client['traceback']
list = db5.list_collection_names()
for name in list:
    db5.drop_collection(name)

processes = []
cnt = 0
files = os.listdir('log_simulator')
for file in files:
    logs = os.listdir(os.path.join('log_simulator',file))
    for log in logs :
        name = os.path.join('log_simulator',file,log)
        processes.append(f"python3 make.py {name}")
        cnt += 1

print(processes)

def run_process(process):
    os.system('{}'.format(process))

pool = Pool(processes=cnt)
pool.map(run_process, processes)