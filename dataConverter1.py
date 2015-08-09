# -*- coding: gbk -*-

'''
Created on 2015年8月9日

@author: ml
'''

import struct

# data的key类型，只支持int和int的数组
KEY_TYPE_INT = 1
KEY_TYPE_TUPLE_INT = 2

# 具体属性值的类型
ATTR_TYPE_INT = 1
ATTR_TYPE_FLOAT = 2
ATTR_TYPE_STR = 3

def getAttrType(aType):
    if aType == int:
        return ATTR_TYPE_INT
    elif aType == float:
        return ATTR_TYPE_FLOAT
    elif aType == str:
        return ATTR_TYPE_STR
    else:
        raise Exception('%s not implement!' % str(aType))

def getSingleBit(x, index):
    return x & (1 << index)

def setSingleBit(x, index, on):
    if on:
        return int(x | (1 << index))
    else:
        return int(x & ~(1 << index))
    
class DataConverter(object):
    def __init__(self):
        super(DataConverter, self).__init__()

    # 数据表的名字
    def getModuleNameByte(self, keyType, name):
        length = len(name)
        key = 'ii%ds' % length
        return struct.pack(key, keyType, length, name)
    
    # 数据表的属性定义
    def getModuleAttrByte(self, valueAttrs):
        attrBytes = []
        length = len(valueAttrs)
        attrBytes.append(struct.pack('i', length))
        for keyName, (aType, seq) in valueAttrs.iteritems():
            packKey = '3h%ds' % len(keyName)
            attrType = getAttrType(aType)
            byte = struct.pack(packKey, len(keyName), attrType, seq, keyName)
            print 'getModuleAttrByte:', len(keyName), attrType, seq, keyName
            attrBytes.append(byte)
        return attrBytes
    
    # 数据每行数据的key
    def getKeyByte(self, keyType, key):
        if keyType == KEY_TYPE_INT:
            return [struct.pack('I', key)]
        else:
            raise Exception("%s, %s not implemented!" % (str(keyType), str(key)))
    
    def getValueByteSeperate(self, valueType, value):
        if valueType == int:
            return struct.pack('i', value)
        elif valueType == float:
            return struct.pack('f', value)
        elif valueType == str:
            packKey = 'i%ds' % len(value)
            return struct.pack(packKey, len(value), value)
        else:
            raise Exception('%s %s not implemented!' % (str(valueType), str(value)))
    
    def setValueFlag(self, flags, index, on):
        x = index / 32
        y = index % 32 
        # print 'setValueFlag:',index,x,y
        flags[x] = setSingleBit(flags[x], y, on)
        return flags
    
    # 数据每行的value
    def getValueByte(self, valueAttrs, valueDict):
        valueBytes = []
        flags = [0, 0, 0, 0, 0]  # 支持160个属性
        seqs = []
        for valueName, (valueType, seq) in valueAttrs:
            if valueDict.has_key(valueName):
                valueByte = self.getValueByteSeperate(valueType, valueDict.get(valueName))
                valueBytes.append(valueByte)
                flags = self.setValueFlag(flags, seq, 1)
                seqs.append(seq)
        print 'value flags:', flags,seqs
        a = struct.pack('I', flags[0])
        return [struct.pack('5I', *flags)] + valueBytes
        
    # kv数据
    def getModuleValueByte(self, module):
        dataBytes = []
        i = 0;
        keyType = module.keyType
        valueAttrs = sorted(module.valueAttrs.iteritems(), key=lambda d:d[1][1])
        print 'getModuleValueByte1:', valueAttrs
        for key, value in module.data.iteritems():
            keyByte = self.getKeyByte(keyType, key)
            dataBytes.extend(keyByte)
            valueByte = self.getValueByte(valueAttrs, value)
            dataBytes.extend(valueByte)
            i = i + 1
        print 'getModuleValueByte2:', i
        return [struct.pack('I', i)] + dataBytes
    
    def convertDataToBytes(self, module):
        if not module.data:
            raise Exception('data empty!')
        if not hasattr(module, 'keyType'):
            raise Exception('keyType empty!')
        if not hasattr(module, 'valueAttrs'):
            raise Exception('valueAttrs empty!')
        
        dataBytes = []
        nameBytes = self.getModuleNameByte(module.keyType, module.__name__)
        dataBytes.append(nameBytes)  # 数据表的名字
        
        attrBytes = self.getModuleAttrByte(module.valueAttrs)
        dataBytes.extend(attrBytes)  # 数据表的属性定义
        
        attrBytes = self.getModuleValueByte(module)
        dataBytes.extend(attrBytes)  # kv数据
        print 'data length:', sum([len(i) for i in dataBytes])
        return dataBytes
    
    def writeBytesToFile(self, abytes):
        with open('cpptest.data', 'wb') as f:
            f.writelines(abytes)
        print 'write file over'
    
    def writeData(self, data):
        abytes = self.convertDataToBytes(data)
        self.writeBytesToFile(abytes)
    
import item_data as ID
ID.valueAttrs = {'name':(str, 1),
'icon':(int, 2),
'modelId':(int, 3),
'modelScale':(float, 4),
'dropItemSound':(int, 5),
'useItemSound':(int, 6),
'dragItemSound':(int, 7),
'parentId':(int, 8),
'isDisplayInDb':(int, 9),
'quality':(int, 10),
'type':(int, 11),
'category':(int, 12),
'subcategory':(int, 13),
'valuable':(int, 14),
'precious':(int, 15),
'runeEquipExp':(int, 16),
'heightOffset':(float, 17),
'questItem':(int, 18),
'cdgroup':(int, 19),
'cd':(int, 20),
'bPrice':(int, 21),
'bPriceType':(int, 22),
'sPrice':(int, 23),
'sPriceType':(int, 24),
'fPrice':(int, 25),
'auctionPrice':(int, 26),
'noBuyBack':(int, 28),
'shopJingJieRequire':(int, 30),
'bindType':(int, 31),
'lvReq':(int, 32),
'maxLvReq':(int, 33),
'sexReq':(int, 34),
'allowBodyType':(int, 35),
'combatReq':(int, 37),
'combatEquReq':(int, 38),
'zaijuReq':(int, 39),
'conType1':(int, 42),
'conId1':(int, 43),
'conOp1':(int, 44),
'conParam1':(int, 45),
'conType2':(int, 46),
'conId2':(int, 47),
'conOp2':(int, 48),
'conParam2':(int, 49),
'conType3':(int, 50),
'conId3':(int, 51),
'conOp3':(int, 52),
'conParam3':(int, 53),
'mwrap':(int, 54),
'holdMax':(int, 55),
'tgtType':(int, 56),
'tgtDist':(float, 57),
'ttlType':(int, 59),
'ttl':(int, 60),
'ttlExpireType':(int, 61),
'ttlChangeId':(int, 62),
'ttlChangeAmount':(int, 63),
'ownership':(int, 65),
'renewalType':(int, 66),
'commonRenewalType':(int, 67),
'mallRenewal30Days':(int, 68),
'mallRenewalOwnership':(int, 69),
'mallRenewalForever':(int, 70),
'noSell':(int, 71),
'noTrade':(int, 72),
'noDrop':(int, 73),
'noMail':(int, 74),
'noConsign':(int, 75),
'coinConsign':(int, 76),
'noBooth':(int, 77),
'noBoothBuy':(int, 78),
'noStorage':(int, 79),
'noRepair':(int, 80),
'noLatch':(int, 81),
'noReturn':(int, 82),
'rideItemType':(int, 83),
'spellTime':(float, 84),
'accordingType':(int, 85),
'ctrl':(int, 86),
'navigatorName':(str, 87),
'descTitle':(str, 89),
'funcDesc':(str, 90),
'desc':(str, 91),
'historyDesc':(str, 92)}

DataConverter().writeData(ID)


with open('test.data', 'wb') as f:
    f.writelines([struct.pack('3I', 1,1,2147483647)])