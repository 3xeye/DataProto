# -*- coding: gbk -*-


'''
Created on 2015年7月26日

@author: ml
'''

import tracemalloc
tracemalloc.start(25)

import cPickle as p
import pbjson
import struct
from data_pb2 import Item_Data

class DataProtoConverter(object):
    def getFileName(self, name):
        return name + ".data"
    
    def convertDataToPbBytes(self, data, pbCls):
        if not data:
            raise Exception('data empty')
        abytes = []
        for k, v in data.iteritems():
            kb = p.dumps(k)
            pbObj = pbjson.dict2pb(pbCls, v)
            vb = pbObj.SerializeToString()
            lb = struct.pack('2i', len(kb), len(vb))
            abytes.append(lb)
            abytes.append(kb)
            abytes.append(vb)
        return abytes
    
    def writeBytesToFile(self, abytes, name):
        fileName = self.getFileName(name)
        f = open(fileName, 'wb')
        f.writelines(abytes)
        f.close()
        print 'write file %s over' % name
        
    def processData(self, data, pbCls, name):
        abytes = self.convertDataToPbBytes(data, pbCls)
        self.writeBytesToFile(abytes, name)
        
    def readFromFile(self, name):
        fileName = self.getFileName(name)
        adict = {}
        f = open(fileName, 'rb')
        abytes = f.read()
        begin = 0
        end = len(abytes)
        while(begin < end):
            a, b = struct.unpack('2i', abytes[begin: begin + 8])
            keyOffset = begin + 8 +a
            valueOffSet = keyOffset + b
            key = p.loads(abytes[begin + 8 : keyOffset])
            begin = valueOffSet
            adict[key] = abytes[keyOffset : valueOffSet]
        return adict 
        

#import item_data as ID
#DataProtoConverter().processData(ID.data, Item_Data, 'item_data')

adict = DataProtoConverter().readFromFile('item_data')


snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('traceback')
# pick the biggest memory block
for stat in top_stats[:5]:
    print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
    for line in stat.traceback.format():
        print(line)
    print('------------------------------------------------------------------')
