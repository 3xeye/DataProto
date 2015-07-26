# -*- coding: gbk -*-

'''
Created on 2015年7月26日

@author: ml
'''
import skill_general_data as s
keys = set([])
keys1 = set([])
for k,v in s.data.iteritems():
    if type(v) !=dict:
        print k,'-',v
    for k1,v1 in v.iteritems():
        if type(v1) != int:
            keys1.add((k1,type(v1)))
            #print k, k1, type(v1)
print keys
for k in keys1:
    print k
