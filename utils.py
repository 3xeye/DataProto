# -*- coding: gbk -*-

'''
Created on 2015年7月26日

@author: ml
'''
import sys
import gc
#import item_data as ID
import skill_general_data


data = {}

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
#data = ID.data


printAllMems()

import time
start = time.clock()
for i in xrange(10000):
    d = {}.get('')#dict({1:1, 2:2, 3:3,4:4,5:5,6:6,11:1, 12:2, 13:3,14:4,15:5,16:6})
end = time.clock()
diff = end - start
print '--------------------m.l   ',diff


import struct

def writeCppBytes():
    abytes = []
    abytes.append( struct.pack('i', 3))
    abytes.append( struct.pack('i', 2))
    abytes.append( struct.pack('i', 1))
    abytes.append( struct.pack('i', 88))
    abytes.append( struct.pack('i', 90))
    abytes.append( struct.pack('i', 9))
    
    with open("cpp.data", 'wb') as f:
        f.writelines(abytes)

writeCppBytes()