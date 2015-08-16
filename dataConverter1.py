# -*- coding: gbk -*-

'''
Created on 2015��8��9��

@author: ml
'''

import struct

# data��key���ͣ�ֻ֧��int��int������
KEY_TYPE_INT = 1
KEY_TYPE_TUPLE_INT = 2

# ��������ֵ������
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

    # ���ݱ������
    def getModuleNameByte(self, keyType, name):
        length = len(name)
        key = 'ii%dsc' % length # %d��ʾ�ַ������������������'\0'
        return struct.pack(key, keyType, length+1, name, '\0')
    
    # ���ݱ�����Զ���
    def getModuleAttrByte(self, valueAttrs):
        attrBytes = []
        length = len(valueAttrs)
        attrBytes.append(struct.pack('i', length))
        for i in xrange(len(valueAttrs)):
            keyName = valueAttrs[i][0]
            aType = valueAttrs[i][1]
            packKey = '3h%dsc' % len(keyName)
            attrType = getAttrType(aType)
            byte = struct.pack(packKey, len(keyName)+1, attrType, i, keyName, '\0')
            print 'getModuleAttrByte:', len(keyName)+1, attrType, i, keyName
            attrBytes.append(byte)
        return attrBytes
    
    # ����ÿ�����ݵ�key
    def getKeyByte(self, keyType, key):
        if keyType == KEY_TYPE_INT:
            return [struct.pack('I', key)]
        elif keyType == KEY_TYPE_TUPLE_INT:
            #print '-----getKeyByte',key
            if type(key)!= tuple:
                raise Exception("%s, %s not implemented!" % (str(keyType), str(key)))
            if len(key)!=2:
                raise Exception("%s, %s not implemented!" % (str(keyType), str(key)))
            return [struct.pack('2I', *key)]
        else:
            raise Exception("%s, %s not implemented!" % (str(keyType), str(key)))
    
    def getValueByteSeperate(self, valueType, value):
        if valueType == int:
            return struct.pack('i', value)
        elif valueType == float:
            return struct.pack('f', value)
        elif valueType == str:
            packKey = 'i%dsc' % len(value)
            #print '--------------------m.l DataConverter.getValueByteSeperate ',packKey,len(value)
            return struct.pack(packKey, len(value)+1, value, '\0')
        else:
            raise Exception('%s %s not implemented!' % (str(valueType), str(value)))
    
    def setValueFlag(self, flags, index, on):
        x = index / 32
        y = index % 32 
        # print 'setValueFlag:',index,x,y
        flags[x] = setSingleBit(flags[x], y, on)
        return flags
    
    # ����ÿ�е�value
    def getValueByte(self, valueAttrs, valueDict):
        valueBytes = []
        flags = [0, 0, 0, 0, 0]  # ֧��160������
        seqs = []
        seq = 0
        for valueName, valueType in valueAttrs:
            if valueDict.has_key(valueName):
                valueByte = self.getValueByteSeperate(valueType, valueDict.get(valueName))
                valueBytes.append(valueByte)
                flags = self.setValueFlag(flags, seq, 1)
                seqs.append(seq)
            seq = seq + 1
        print 'value flags:', flags, seqs
        return [struct.pack('5I', *flags)] + valueBytes
        
    # kv����
    def getModuleValueByte(self, module):
        dataBytes = []
        i = 0;
        keyType = module.keyType
        valueAttrs = module.valueAttrs
        print 'getModuleValueByte1:', valueAttrs
        for key, value in module.data.iteritems():
            keyByte = self.getKeyByte(keyType, key)
            dataBytes.extend(keyByte)
            valueByte = self.getValueByte(valueAttrs, value)
            dataBytes.extend(valueByte)
            i = i + 1
        print 'getModuleValueByte2:', i
        return [struct.pack('I', i)] + dataBytes
    
    def getModuleLenBytes(self, datas):
        return [struct.pack('I', len(datas))]
    
    def convertDataToBytes(self, module):
        if not module.data:
            raise Exception('data empty!')
        if not hasattr(module, 'keyType'):
            raise Exception('keyType empty!')
        if not hasattr(module, 'valueAttrs'):
            raise Exception('valueAttrs empty!')
        
        dataBytes = []
        nameBytes = self.getModuleNameByte(module.keyType, module.__name__)
        dataBytes.append(nameBytes)  # ���ݱ������
        
        attrBytes = self.getModuleAttrByte(module.valueAttrs)
        dataBytes.extend(attrBytes)  # ���ݱ�����Զ���
        
        attrBytes = self.getModuleValueByte(module)
        dataBytes.extend(attrBytes)  # kv����
        print 'data length:', sum([len(i) for i in dataBytes])
        return dataBytes
    
    def writeBytesToFile(self, abytes):
        with open('cpptest.data', 'wb') as f:
            f.writelines(abytes)
        print 'write file over'
    
    def writeData(self, datas):
        abytes = self.getModuleLenBytes(datas)
        for data in datas:
            temp = self.convertDataToBytes(data)
            abytes.extend(temp)
        self.writeBytesToFile(abytes)
    
import item_data as ID
ID.keyType = 1
ID.valueAttrs = [('name', str),
('icon', int),
('modelId', int),
('modelScale', float),
('dropItemSound', int),
('useItemSound', int),
('dragItemSound', int),
('parentId', int),
('isDisplayInDb', int),
('quality', int),
('type', int),
('category', int),
('subcategory', int),
('valuable', int),
('precious', int),
('runeEquipExp', int),
('heightOffset', float),
('questItem', int),
('cdgroup', int),
('cd', int),
('bPrice', int),
('bPriceType', int,),
('sPrice', int),
('sPriceType', int),
('fPrice', int),
('auctionPrice', int),
('noBuyBack', int),
('shopJingJieRequire', int),
('bindType', int),
('lvReq', int),
('maxLvReq', int),
('sexReq', int),
('allowBodyType', int),
('combatReq', int),
('combatEquReq', int),
('zaijuReq', int),
('conType1', int),
('conId1', int),
('conOp1', int),
('conParam1', int),
('conType2', int),
('conId2', int),
('conOp2', int),
('conParam2', int),
('conType3', int),
('conId3', int),
('conOp3', int),
('conParam3', int),
('mwrap', int),
('holdMax', int),
('tgtType', int),
('tgtDist', float),
('ttlType', int),
('ttl', int),
('ttlExpireType', int),
('ttlChangeId', int),
('ttlChangeAmount', int),
('ownership', int),
('renewalType', int),
('commonRenewalType', int),
('mallRenewal30Days', int),
('mallRenewalOwnership', int),
('mallRenewalForever', int),
('noSell', int),
('noTrade', int),
('noDrop', int),
('noMail', int),
('noConsign', int),
('coinConsign', int),
('noBooth', int),
('noBoothBuy', int),
('noStorage', int),
('noRepair', int),
('noLatch', int),
('noReturn', int),
('rideItemType', int),
('spellTime', float),
('accordingType', int),
('ctrl', int),
('navigatorName', str),
('descTitle', str),
('funcDesc', str),
('desc', str),
('historyDesc', str)]
print 'ID.valueAttrs len:',len(ID.valueAttrs)

import skill_general_data as SGD
SGD.keyType = 2
SGD.valueAttrs = [('learnPoint', int),
('wsAdd1', int),
('describe', str),]

DataConverter().writeData([ID,SGD])

with open('test.data', 'wb') as f:
    f.writelines([struct.pack('3I', 1, 1, 2147483647)])
