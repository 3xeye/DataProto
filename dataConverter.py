# -*- coding: gbk -*-


'''
Created on 2015年7月26日

@author: ml
'''

import cPickle as p
import pbjson
import struct
import zlib


class BytesDict(dict):
    def __init__(self, context, dic, name):
        self.context = context
        self.table_name = name
        self.table = dic
    
    def __len__(self):
        while 1:
            l = len(self.table)
            if l >= 0:
                return l
    
    def __repr__(self):
        raise Exception('not supported!')
    
    def __str__(self):
        raise Exception('not supported!')
    
    def clear(self):
        self.table.truncate()
    
    def __getitem__(self, key):
        value = self.table.get(key)
        if not value:
            return value
        return self.context.getValueFromBytes(value)

    def get(self, key, default=None):
        try:
            value = self.table.get(key, default)
            if not value:
                return value
            return self.context.getValueFromBytes(value)
        except:
            return default
        
    def __setitem__(self, key, value):
        self.table[key] = value
        
    def __delitem__(self, key):
        raise Exception('not supported!')
    
    def __contains__(self, key):
        return self.table.has_key(key)
    
    def has_key(self, key):
        return self.table.has_key(key)
    
    def __iter__(self):
        keys = self.table.keys()
        for k in keys:
            yield k
            
    def iterkeys(self):
        ks = self.table.keys()
        for k in ks:
            yield k
            
    def itervalues(self):
        raise Exception('not supported!')
    
    def iteritems(self):
        raise Exception('not supported!')
    
    def normal_dict(self):
        raise Exception('not supported!')
    
    def keys(self):
        ks = self.table.keys()
        return ks
    
    def values(self):
        raise Exception('not supported!')
    
    def items(self):
        raise Exception('not supported!')
    
    def update(self, other):
        raise Exception('not supported!')



class DataConverter(object):
    def __init__(self):
        super(DataConverter, self).__init__()
        
    def getFileName(self, name):
        return name + ".data"
    
    def genKeyBytes(self, key):
        return p.dumps(key)
    
    def genValueBytes(self, value):
        raise Exception('not implemnet!')
    
    def getKeyFromBytes(self, keyBytes):
        return p.loads(keyBytes)
    
    def getValueFromBytes(self, valueBytes):
        raise Exception('not implemnet!')
    
    def genConvertedBytes(self, key, value):
        byteList = []
        keyBytes = self.genKeyBytes(key)
        valueBytes = self.genValueBytes(value)
        lenBytes = struct.pack('2h', len(keyBytes), len(valueBytes))
        byteList.append(lenBytes)
        byteList.append(keyBytes)
        byteList.append(valueBytes)
        return byteList
    
    def convertDataToBytes(self, data):
        if not data:
            print '###################convertDataToBytes data empty#####################'
            return
        
        abytes = []
        for key, value in data.iteritems():
            byteList = self.genConvertedBytes(key, value)
            abytes.extend(byteList)
        return abytes
    
    def writeBytesToFile(self, abytes, name):
        fileName = self.getFileName(name)
        with open(fileName, 'wb') as f:
            f.writelines(abytes)
        print 'write file %s over' % name
        
    def writeData(self, data, name):
        abytes = self.convertDataToBytes(data)
        self.writeBytesToFile(abytes, name)
    
    def getKeyValueFromBytes(self, byts, begin):
        numOffset = begin + 4
        keyLen, valueLen = struct.unpack('2h', byts[begin: numOffset])
        keyOffset = numOffset + keyLen
        valueOffSet = keyOffset + valueLen
        key = self.getKeyFromBytes(byts[numOffset : keyOffset])
        value = byts[keyOffset : valueOffSet]
        return key, value, valueOffSet
        
    def loadData(self, name):
        fileName = self.getFileName(name)
        adict = BytesDict(self, {}, name)
        with open(fileName, 'rb') as f:
            abytes = f.read()
            begin = 0
            end = len(abytes)
            while(begin < end):
                key, value, valueOffSet = self.getKeyValueFromBytes(abytes, begin)
                adict[key] = value
                begin = valueOffSet
        return adict 


class DataZlibConverter(DataConverter):
    def __init__(self):
        super(DataZlibConverter, self).__init__()
        
    def genValueBytes(self, value):
        return zlib.compress(str(value), zlib.Z_BEST_COMPRESSION)
    
    def getValueFromBytes(self, valueBytes):
        return eval(zlib.decompress(valueBytes))


class DataPickleConverter(DataConverter):
    def __init__(self):
        super(DataPickleConverter, self).__init__()
    
    def genValueBytes(self, value):
        return p.dumps(value)
        
    def getValueFromBytes(self, valueBytes):
        return p.loads(valueBytes)
    
class DataPickleStrConverter(DataConverter):
    def __init__(self):
        super(DataPickleStrConverter, self).__init__()
        
    def genValueBytes(self, value):
        return p.dumps(str(value))
    
    def getValueFromBytes(self, valueBytes):
        return p.loads(valueBytes)



    
class DataProtoBufConverter(DataConverter):
    VALUE_TYPE_PB = 1  # 正常都应该是dict可以转成pb的
    VALUE_TYPE_E = 2  # G类型的特殊处理，直接用pickle
    def __init__(self):
        super(DataProtoBufConverter, self).__init__()
        self.pbClass = None
        self.eFields = None
        
    def setConverterClass(self, pbClass, eFields):
        self.pbClass = pbClass
        self.eFields = eFields
        
    def genValueBytes(self, value):
        return p.dumps(str(value))
    
    def pbToDict(self, valueDict):
        byts = valueDict.get('byteValue')
        decodeType = valueDict.get('decodeType')
        if decodeType == DataProtoBufConverter.VALUE_TYPE_PB:
            pb = self.pbClass()
            pb.ParseFromString(byts)
            adict = pbjson.pb2dict(pb)
            for k, v in adict.iteritems():
                if k in self.eFields:
                    adict[k] = eval(v)
            return adict
        else:
            return p.loads(byts)
    
    def getValueFromBytes(self, valueBytes):
        return self.pbToDict(valueBytes)
    
    # data的value格式修正，类型是e的直接转成string
    def convertToNormalDict(self, valueDict, eFields):
        if not valueDict or not eFields:
            return valueDict
        
        d = {}
        if type(valueDict) != dict:
            return valueDict
        for key, value in valueDict.iteritems():
            if key in eFields:
                d[key] = str(value)
            else:
                d[key] = value
        return d
    
    def genConvertedBytes(self, key, value):
        byteList = []
        keyBytes = self.genKeyBytes(key)
        
        fieldDict = self.convertToNormalDict(value, self.eFields)
        if type(value) == dict:
            dataType = DataProtoBufConverter.VALUE_TYPE_PB
            pbObj = pbjson.dict2pb(self.pbClass, fieldDict)
            vbytes = pbObj.SerializeToString()
        else:
            dataType = DataProtoBufConverter.VALUE_TYPE_E
            vbytes = p.dumps(fieldDict)
        
        lenBytes = struct.pack('2h1i', dataType, len(keyBytes), len(vbytes))
        byteList.append(lenBytes)
        byteList.append(keyBytes)
        byteList.append(vbytes)
        return byteList
    
    def getKeyValueFromBytes(self, byts, begin):
        numOffset = begin + 8
        dataType, keyLen, valueLen = struct.unpack('2h1i', byts[begin: numOffset])
        keyOffset = numOffset + keyLen
        valueOffSet = keyOffset + valueLen
        key = p.loads(byts[numOffset : keyOffset])
        if dataType == DataProtoBufConverter.VALUE_TYPE_PB:
            value = {'byteValue' : byts[keyOffset : valueOffSet], 'decodeType': DataProtoBufConverter.VALUE_TYPE_PB}
        elif dataType == DataProtoBufConverter.VALUE_TYPE_E:
            value = {'byteValue' : byts[keyOffset : valueOffSet], 'decodeType': DataProtoBufConverter.VALUE_TYPE_E}
        return key, value, valueOffSet
    
    


####################################################################zlib 4.9m 1.526s 14598
import item_data as ID
import time
d = DataZlibConverter()
d.writeData(ID.data, 'item_zlib_conver')
adict = d.loadData('item_zlib_conver')
print len(adict)
print adict.get(201102)
keys = adict.keys()
start = time.clock()
for key in keys:
    a = adict.get(key)
end = time.clock()
diff = end - start
print '--------------------m.l   ',diff


####################################################################pickle 11.2m 0.2275s
# import item_data as ID
# import time
# d = DataPickleConverter()
# d.writeData(ID.data, 'item_pickle_conver')
# adict = d.loadData('item_pickle_conver')
# print len(adict)
# print adict.get(201102)
# keys = adict.keys()
# start = time.clock()
# for key in keys:
#     a = adict.get(key)  # d.getValueFromBytes(adict.get(key))
# end = time.clock()
# diff = end - start
# print '--------------------m.l   ', diff


####################################################################pickleStr 10.3m 0.243s
# import item_data as ID
# import time
# d = DataPickleStrConverter()
# d.writeData(ID.data, 'item_pickle_str_conver')
# adict = d.loadData('item_pickle_conver')
# print len(adict)
# print d.getValueFromBytes(adict.get(201102))
# keys = adict.keys()
# start = time.clock()
# for key in keys:
#     a = d.getValueFromBytes(adict.get(key))
# end = time.clock()
# diff = end - start
# print '--------------------m.l   ',diff


####################################################################pb 2.18m 1.893s
# import item_data as ID
# import time
# from data_pb2 import Item_Data
# d = DataProtoBufConverter()
# d.setConverterClass(Item_Data, [])
# d.writeData(ID.data, 'item_proto_conver')
# adict = d.loadData('item_proto_conver')
# print len(adict)
# print adict.get(201102)
# keys = adict.keys()
# start = time.clock()
# for key in keys:
#     a = adict.get(key)
# end = time.clock()
# diff = end - start
# print '--------------------m.l   ',diff


####################################################################dict 
# import item_data as ID
# import time
# keys = ID.data.keys()
# start = time.clock()
# for key in keys:
#     a = ID.data.get(key)
# end = time.clock()
# diff = end - start
# print '--------------------m.l   ',diff


####################################################################sgd pickle 5.63m 0.1865s 7472
# import skill_general_data as SGD
# import time
# d = DataPickleConverter()
# d.writeData(SGD.data, 'sgd_pickle_conver')
# adict = d.loadData('sgd_pickle_conver')
# print len(adict)
# print adict.get((1101, 1))
# keys = adict.keys()
# start = time.clock()
# for key in keys:
#     a = adict.get(key)
# end = time.clock()
# diff = end - start
# print '--------------------m.l   ', diff



####################################################################sgd zlib 2.42m 1.11s 7472
# import skill_general_data as SGD
# import time
# d = DataZlibConverter()
# d.writeData(SGD.data, 'sgd_zlib_conver')
# adict = d.loadData('sgd_zlib_conver')
# print len(adict)
# print adict.get((1101, 1))
# keys = adict.keys()
# start = time.clock()
# for key in keys:
#     a = adict.get(key)
# end = time.clock()
# diff = end - start
# print '--------------------m.l   ',diff


####################################################################protobuf sgd 1.71m 1.6288s 7472
sgdEFields = ['uiShape', 'rangeMax', 'circleShape', 'auras', 'castDelay', 'seAfterCalc', 'tgtSelectStrategy', 'preAmmoType', 'consumEquipNeed', 'selfStates', 'se', 'selfNoStates', 'chargeStgs', 'creations', 'addWsEff', 'collideHeight', 'graph2', 'graph1', 'graph3', 'graph4', 'wpSkillType', 'effects']
import skill_general_data as SGD
import time
from data_pb2 import Skill_General_Data
d = DataProtoBufConverter()
d.setConverterClass(Skill_General_Data, sgdEFields)
d.writeData(SGD.data, 'sgd_proto_conver')
adict = d.loadData('sgd_proto_conver')
print len(adict)
print adict.get((1101, 1))
keys = adict.keys()
start = time.clock()
for key in keys:
    a = adict.get(key)
end = time.clock()
diff = (end - start)/len(keys)
print '--------------------m.l   ',diff


