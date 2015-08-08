# -*- coding: gbk -*-


import tracemalloc
tracemalloc.start(25)

import cPickle as p
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
# import skill_general_data
# d = skill_general_data.data
# dic = readBinFile()
# 
# #dic = binToPb(dic)
# 
# testGetDict(dic)
printAllMems()

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

# a = ['sePa2', 'sePa', 'sePaAfterCalc']
# ab = p.dumps(a)
# print len(ab)
# d = p.loads(ab)
# print type(d), d

# formu = lambda d:int((d['lv']+2.2)**1.45/2.0)
# print type(formu)
# from cloud.serialization import cloudpickle as p
# formulaBytes = p.dumps(formu)
# print len(formulaBytes)
# f = p.loads(formulaBytes)
# print type(f), f

 
a = { (1101, 1): {'addWsEff': [10001,], 'autoUseSkill': 1
, 'canLearn': 1
, 'castMoveType': 1
, 'cd': 0.6
, 'effects': [10001, 10879, 10880, 10881, 10882, 10883]
, 'forceHit': 1
, 'gcd': 0
, 'graph1': ('前方扇形', 6, '5米')
, 'graph2': ('冷却时间', 0, '0.6秒')
, 'id': 1101001
, 'isGcdAdd': 1
, 'learnLv': 1
, 'lv': 1
, 'mpNeed': 1
, 'name': '猛击'
, 'noTgt': 1
, 'school': 3
, 'sid': 1101
, 'skillCategory': 1
, 'skillType': 1
, 'spellTime': 0
, 'unShowPush': 1
, 'wpSkillType': [10001, 10002]
, 'wsAdd1': 180
, 'wsType': 1
},
}
import zlib
import item_data
s = str(item_data.data)
print len(s)
c = zlib.compress(s)
print len(c)
print 'zlib compress 1:%d,2:%d,3:%d,4:%d,5:%d,6:%d,7:%d,8:%d,9:%d'%(len(zlib.compress(s, 1)), len(zlib.compress(s, 2)), len(zlib.compress(s, 3)), len(zlib.compress(s, 4)), \
                len(zlib.compress(s, 5)), len(zlib.compress(s, 6)), len(zlib.compress(s, 7)), len(zlib.compress(s, 8)), len(zlib.compress(s, 9)) )
f = open('idall.data', 'wb')
f.write(c)
f.close()
# d =  zlib.decompress(c)
# print d
# print type(eval(d))
# wpSkillType = eval(d).get((1101, 1)).get('wpSkillType')
# print type(wpSkillType)

############################################################################zlib
# import zlib
# import item_data as ID
# bytes = []
# for k, v in ID.data.iteritems():
#     keyBytes = zlib.compress(str(k), 9)
#     valueBytes = zlib.compress(str(v), 9)
#     print 'key:%d,%d, %d; value:%d,%d'%(len(str(k)), len(keyBytes), len(p.dumps(k)),len(str(v)), len(valueBytes))
#     lenBytes = struct.pack('2h', len(keyBytes), len(valueBytes))
#     bytes.append(lenBytes)
#     bytes.append(keyBytes)
#     bytes.append(valueBytes)
# f = open('id.data', 'wb')
# f.writelines(bytes)
# f.close()
# f = None

# import zlib
# f = open('id.data', 'rb')
# abytes = f.read()
# begin = 0
# end = len(abytes)
# i_dict = {}
# while(begin < end):
#     numOffset = begin + 4
#     keyLen, valueLen = struct.unpack('2h', abytes[begin: numOffset])
#     keyOffset = numOffset + keyLen
#     valueOffSet = keyOffset + valueLen
#     i_dict[eval(zlib.decompress(abytes[numOffset : keyOffset]))] = abytes[keyOffset : valueOffSet]
#     begin = valueOffSet
# print len(i_dict)
# #print i_dict[401]#, i_dict[401].get('funcDesc')
# 
# keys = i_dict.keys()
# start = time.clock()
# for key in keys:
#     value = eval(zlib.decompress(i_dict.get(key)))
# end = time.clock()
# diff = end - start
# print '--------------------m.l   ',diff


############################################################################zlib sgd
import zlib
import sys
import skill_general_data as SGD
bytes = []
for k, v in SGD.data.iteritems():
    keyBytes = zlib.compress(str(k), 9)
    valueBytes = zlib.compress(str(v), 9)
    print 'key:%d,%d, %d; value:%d,%d,%d'%(sys.getsizeof(str(k)), len(keyBytes), len(p.dumps(k)),len(str(v)), len(valueBytes),len(zlib.compress(p.dumps(v,2), 9)))
    lenBytes = struct.pack('2h', len(keyBytes), len(valueBytes))
    bytes.append(lenBytes)
    bytes.append(keyBytes)
    bytes.append(valueBytes)
f = open('sgd.data', 'wb')
f.writelines(bytes)
f.close()
f = None