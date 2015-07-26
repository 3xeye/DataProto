# -*- coding: gbk -*-


import tracemalloc
tracemalloc.start(25)

import pickle as p
import gc
import pbjson
import sys
import struct
import time

from data_pb2 import Item_Data

#

def getAllMems():
    memDict = {}
    objs = gc.get_objects()
    for o in objs:
        key = type(o)
        if not memDict.has_key(key):
            memDict[key] = sys.getsizeof(o, 0)
        else:
            memDict[key] = memDict[key] + sys.getsizeof(o, 0)
    memDict = sorted(memDict.iteritems(), key=lambda d:d[1], reverse=True)
    return memDict

def printAllMems():
    mems = getAllMems()
    size = 0
    print '[ Top 10 ]'
    for v in mems[:10]:
        size += v[1]
        print 'type is %s, size is %f' % (str(v[0]), v[1] / 1024.0 / 1024.0)
    print 'all mem size is %f' % (size / 1024.0 / 1024.0)
    print '------------------------------------------------------------------'
    
def convertToPB():
    pbDict = {}
    import item_data as ID
    return pbDict
    
    for k, v in ID.data.iteritems():
        pb = pbjson.dict2pb(Item_Data, v)
        pbDict[k] = pb
    return pbDict

def dumpToFile(pbs):
    f = file('pbs.txt', 'w')
    try:
        p.dump(pbs, f)
    except Exception, e:
        print 'write error', e.message
    print 'write over'


def loadFromFiles():
    f = file('pbs.txt', 'r')
    pbDict = {}
    try:
        pbDict = p.load(f)
    except Exception, e:
        print 'load error', e.message
    f.close()
    f = None
    # print 'readFromFiles', sys.getsizeof(pbDict, 0)
    return pbDict


def writeToFile(pbs):
    f = file('pbs.txt', 'w')
    lines = []
    for k, v in pbs.iteritems():
        print k, len(v.SerializeToString())  # ,v.SerializeToString()
        lines.append(v.SerializeToString())
    f.writelines(lines)
    f.close()
    print 'write over'


def readFromFiles():
    pbDict = {}
    f = file('pbs.txt', 'r')
    idx = 0
    for i in f.readlines():
        print len(i)
        item1 = Item_Data()
        item1.ParseFromString(i)
        pbDict[idx] = item1
        idx = idx + 1
    f.close()
    f = None
    # print 'readFromFiles', sys.getsizeof(pbDict, 0)
    return pbDict

def manyDict():
    a = {1:1}
    for i in xrange(10000000):
        b = dict(a)
    return

def writePyFile(pbs):
    f = file('data_proto.py', 'w')
    f.write("# -*- coding: gbk -*-\n")
    f.write("data = {\n")
    for k, v in pbs.iteritems():
        f.write(str(k) + ":\'\'\'" + v.SerializeToString() + "\'\'\',\n")
    f.write('}')
    f.close()
    
    
def testMemory():
    adict = {}
    for i in xrange(10000):
        d = Item_Data()
        d.name = 'namexxxxxxxxxxx' + str(i)
        d.desc = 'asdfawasdfasdfafwefsdkfjas;dkjfasdhguhe' + str(i)
        adict[i] = d
    return adict
# def readPyFile():
#     import data_proto as DP
    

def writeBinFile(pbs):
    f = file('pbs.data', 'wb')
    for k, value in pbs.iteritems():
        v = value.SerializeToString()
        print k, len(v)
        bytes = struct.pack('2i', k, len(v))
        f.write(bytes)
        f.write(v)
    f.close()
    print 'write over'
    
def readBinFile():
    dic = {}
    f = file('pbs.data', 'rb')
    bytes = f.read()
    bytesCount = len(bytes)
    start = 0
    while(start < bytesCount):
        a, b = struct.unpack('2i', bytes[start: start + 8])
        d = bytes[start + 8: start + 8 + b]
        start = start + 8 + b
        dic[a] = d
    f.close()
    f = None
    return dic

def binToPb(dic):
    pbDic = {}
    for k,v in dic.iteritems():
        item = Item_Data()
        item.ParseFromString(v)
        pbDic[k] = item
    return pbDic

def testGetDict(dic):
    keys = dic.keys()
    for i in xrange(10000):
        itemBin = dic.get(keys[i%10000])
        item = Item_Data()
        item.ParseFromString(itemBin)
        #dd = pbjson.pb2dict(item)
    #print len(dic),len(itemBin),item.descTitle,item
    
# import item_data as ID
# writeBinFile(ID.data)
# printAllMems()

dic = readBinFile()

dic = binToPb(dic)

#testGetDict(dic)

# see top10
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')
print("[ Top 10 ]")
for stat in top_stats[:10]:
    print(stat)
    
# see top10 with traceback, 这里需要tracemalloc.start(25)
# snapshot = tracemalloc.take_snapshot()
# top_stats = snapshot.statistics('traceback')
# # pick the biggest memory block
# for stat in top_stats[:5]:
#     print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
#     for line in stat.traceback.format():
#         print(line)
#     print('------------------------------------------------------------------')
    
# writePyFile(pbs)

# pbs = convertToPB()
# writeToFile(pbs)
# pbs = readFromFiles()
# printAllMems()


# pbs = convertToPB()
# dumpToFile(pbs)
# pbs = loadFromFiles()
# print len(pbs)
# printAllMems()

# pbs = {}
# start = time.clock()
# pbs = convertToPB()
# end = time.clock()
# print len(pbs)
# print 'time is %f' % (end - start)
# print gc.isenabled()
# gc.collect()
# printAllMems()
# writeToFile(pbs)

# item = pbs.get(330293)
# print type(item)
# print dir(item)
# print item.name
# bytes = item.SerializeToString()  
# print len(bytes),type(bytes)
# 
# 
# item1 = Item_Data()
# item1.ParseFromString(bytes)
# print type(item1)
# print item1#,item1.name
