# -*- coding: gbk -*-

'''
Created on 2015��7��26��

@author: ml
'''
import pbjson
from data_pb2 import Item_Data

def converToPb(data):
    reData = {}
    for k, v in data.iteritems():
        pb = pbjson.dict2pb(Item_Data, v)
        reData[k] = pb
    return reData