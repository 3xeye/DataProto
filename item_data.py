# -*- coding: gbk -*-
#
#道具_数据表.csv
# 数据序列 : id
# 任务发布服 : publishTag
# 物品名 : name
# ICON : icon
# 掉落地面模型 : modelId
# 掉落物模型大小比例 : modelScale
# 掉落地面音效 : dropItemSound
# 右键或装备音效 : useItemSound
# 拖拽音效 : dragItemSound
# 道具父ID : parentId
# 是否在数据库显示 : isDisplayInDb
# 物品品质 : quality
# 是否为贵重物品 : valuable
# 物品类型 : type
# 显示大类 : category
# 显示小类 : subcategory
# 神格喂养经验 : runeEquipExp
# 物品头顶名字显示高度 : heightOffset
# 是否为商城道具 : mallItem
# 是否为任务道具 : questItem
# 物品对应广播特效 : itemClientEffs
# 是否每次只能捡一个 : pickOneOnSingleTry
# 拾取时是否不进队伍包裹 : freePickFlag
# 质地值 : identifyQuality
# 未鉴定分类 : identifyType
# 物品自身冷却组 : cdgroup
# 自身冷却组时长 : cd
# 买价 : bPrice
# 买价类型 : bPriceType
# 卖价 : sPrice
# 卖价类型 : sPriceType
# 竞拍价 : auctionPrice
# 修理价 : fPrice
# 兑换用货币价格 : famePrice
# 是否允许回购 : noBuyBack
# 和声望等级相关的回购价格 : buybackFamePrice
# 普通商店境界购买限制 : shopJingJieRequire
# 物品绑定类型 : bindType
# 使用等级下限 : lvReq
# 使用等级上限 : maxLvReq
# 使用/装备性別限制 : sexReq
# 装备体型限制 : allowBodyType
# 装备职业限制 : schReq
# 角色境界限制 : needJingJie
# 战斗状态使用限制 : combatReq
# 战斗状态装备限制 : combatEquReq
# 载具状态使用限制 : zaijuReq
# 是否有归属权概念 : needOwner
# 允许使用的地图类型 : allowUseMapTypes
# 不允许使用的地图 : forbidInMaps
# 堆叠上限 : mwrap
# 持有数量限制 : holdMax
# 目标类型 : tgtType
# 使用者和对象的最大距离限制 : tgtDist
# 允许存在的地图类型 : allowExistMapTypes
# 允许存在的地图 : allowExistMaps
# 时间限制类型 : ttlType
# 时间限制时长参数 : ttl
# 是否时间到后消失 : ttlExpireType
# 过期后变成的物品ID : ttlChangeId
# 过期变成的物品数目 : ttlChangeAmount
# 冻结时间 : freezeUseTime
# 是否可续期 : canRenewal
# 初始拥有度 : ownership
# 外观指定续期类型 : renewalType
# 外观公共续期类型 : commonRenewalType
# 商城30天续期价格 : mallRenewal30Days
# 商城30天续期增加拥有度 : mallRenewalOwnership
# 商城永久价格 : mallRenewalForever
# 物品标记 : rideItemType
# 使用道具的吟唱时间 : spellTime
# 装备模型读取参照 : accordingType
# CTRL点击提示 : ctrl
# 是否跑商特产 : businessItem
# 右键寻路位置 : navigatorName
# 右键寻路ID : navigatorTarget
# 类别描述 : descTitle
# 功能描述 : funcDesc
# 补充描述 : desc
# 世界观描述 : historyDesc
# 在数据库中显示 : DisplayInDB
# itemFlags : itemFlags
# conditionsList : conditionsList

keyType = 1
data = {
    2147483647:{'timestamp': 1437631829},
    200:{'name': '经验', 'icon': 70003, 'modelId': 30001, 'modelScale': 1.0, 'dropItemSound': 251, 'dragItemSound': 300, 'quality': 1, 'type': 0, 'category': 99, 'subcategory': 1, 'heightOffset': 0.8, 'bPrice': 1, 'sPrice': 1, 'auctionPrice': 1, 'bindType': 0, 'itemFlags': 176, 'descTitle': '经验', 'funcDesc': '人物经验，可提升人物等级。', },
    711211:{'name': '空之晶·陆[绑]', 'icon': 30360, 'modelId': 30008, 'modelScale': 0.5, 'dropItemSound': 256, 'dragItemSound': 300, 'parentId': 701211, 'isDisplayInDb': 1, 'quality': 4, 'valuable': 1, 'type': 9, 'category': 11, 'subcategory': 2, 'heightOffset': 1.1, 'bPrice': 729000, 'bPriceType': 1, 'sPrice': 9600, 'auctionPrice': 960, 'bindType': 1, 'lvReq': 64, 'combatReq': 0, 'combatEquReq': 0, 'mwrap': 99, 'itemFlags': 1424, 'descTitle': '神格道具', 'funcDesc': '6级空之晶。\n嵌入神格盘可用于神格觉醒和神力激发\n3个同等级的神格结晶合成可获得更高等级的神格结晶', },
    9240103:{'name': '青麟魄', 'icon': 40910, 'modelId': 10232, 'modelScale': 0.4, 'dropItemSound': 259, 'useItemSound': 203, 'dragItemSound': 109, 'quality': 4, 'type': 13, 'category': 6, 'subcategory': 2, 'precious': 1, 'heightOffset': 1.2, 'mallItem': 1, 'bPrice': 192000, 'sPrice': 19200, 'auctionPrice': 16000, 'noBuyBack': 1, 'bindType': 1, 'combatReq': 0, 'combatEquReq': 0, 'mwrap': 99, 'itemFlags': 155, 'descTitle': '灵魄', 'funcDesc': '聚集了灵兽【青麟】力量的灵魄，可用于12-15级的装备精炼。', 'desc': '可在高等级弑神难度副本中获得，或在商城购买。', },
    9240105:{'name': '青麟魄1', 'icon': 40910, 'modelId': 10232, 'modelScale': 0.4, 'dropItemSound': 259, 'useItemSound': 203, 'dragItemSound': 109, 'quality': 4, 'type': 13, 'category': 6, 'subcategory': 2, 'precious': 1, 'heightOffset': 1.2, 'mallItem': 1, 'bPrice': 192000, 'sPrice': 19200, 'auctionPrice': 16000, 'noBuyBack': 1, 'bindType': 1, 'combatReq': 0, 'combatEquReq': 0, 'mwrap': 99, 'itemFlags': 155, 'descTitle': '灵魄', 'funcDesc': '聚集了灵兽【青麟】力量的灵魄，可用于12-15级的装备精炼。', 'desc': '可在高等级弑神难度副本中获得，或在商城购买。', },
}

# import utils
# data = utils.converToPb(data)
