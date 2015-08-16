# -*- coding: gbk -*-


'''
Created on 2015年7月26日

@author: ml
'''

import tracemalloc
tracemalloc.start()
#tracemalloc.start(25)

from dataProtoConverter import DataProtoConverter
from dataProtoConverter import pbToDict
import pbjson
import zlib
from data_pb2 import Item_Data
from data_pb2 import Skill_General_Data

print '-------------------start'

# write item_data
import item_data as ID
DataProtoConverter().processData(ID.data, Item_Data, 'item_data', [])


# read item_data
# adict = DataProtoConverter().readFromFile('item_data')
# byts = adict.get(103831)
# print type(byts)
# print len(byts)
# item = Item_Data()
# item.ParseFromString(byts)
# print item


sgdEFields = ['uiShape', 'rangeMax', 'circleShape', 'auras', 'castDelay', 'seAfterCalc', 'tgtSelectStrategy', 'preAmmoType', 'consumEquipNeed', 'selfStates', 'se', 'selfNoStates', 'chargeStgs', 'creations', 'addWsEff', 'collideHeight', 'graph2', 'graph1', 'graph3', 'graph4', 'wpSkillType', 'effects']

# write skill_general_data
# import skill_general_data as SGD
# DataProtoConverter().processData(SGD.data, Skill_General_Data, 'skill_general_data', sgdEFields)

# adict = DataProtoConverter().readFromFile('skill_general_data')
# valueDict = adict.get((1646, 19))
# print len(valueDict)
# keys = adict.keys()
# import time
# start = time.clock()
# for key in keys:
#     try:
#         d = pbToDict(Skill_General_Data, adict.get(key), sgdEFields)
#     except:
#         print '-------------error', key, adict.get(key)
#     if type(d) == dict:
#         graph2 =  d.get('graph2',(-99,-99))
#         print key, graph2, graph2[0]
#     else:
#         print key, d
#    
# end = time.clock()
# diff = end - start
# if diff > 0.005:
#     print '--------------------m.l   ', len(keys), diff



def getAllMems():
    import gc
    import sys
    memDict = {}
    objs = gc.get_objects()
    for o in objs:
        key = type(o)
        if not memDict.has_key(key):
            memDict[key] = (sys.getsizeof(o), 1)
        else:
            memDict[key] = (memDict[key][0] + sys.getsizeof(o, 0), memDict[key][1]+1)
    memDict = sorted(memDict.iteritems(), key=lambda d:d[1][0], reverse=True)
    return memDict

def printAllMems():
    mems = getAllMems()
    size = 0
    print '[ Top 10 ]'
    for v in mems[:10]:
        size += v[1][0]
        print 'type is %s, size is %f, count is %d' % (str(v[0]), v[1][0] / 1024.0 / 1024.0, v[1][1])
    print 'all mem size is %f' % (size / 1024.0 / 1024.0)
    print '------------------------------------------------------------------'

printAllMems()
    
    
# snapshot = tracemalloc.take_snapshot()
# top_stats = snapshot.statistics('lineno')
# 
# print("[ Top 10 ]")
# for stat in top_stats[:10]:
#     print(stat)



snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('traceback')
# pick the biggest memory block
for stat in top_stats[:10]:
    print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
    for line in stat.traceback.format():
        print(line)
    print('------------------------------------------------------------------')
