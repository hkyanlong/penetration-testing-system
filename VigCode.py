# 实现维吉尼亚密码
# 小写字典
lowDict = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# 大写字典
capDict = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


# 将字母转换成数字
def switch(ele):
    flag = 0
    if ele in lowDict:
        ele = lowDict.index(ele)
    elif ele in capDict:
        ele = capDict.index(ele)
        flag = 1
    return [int(ele), flag]


# beState 处理前  afState 处理后
# 加解密算法
def algo(choose, beState, key):
    # 判断密钥格式
    for i in key:
        if not i.isalpha():
            print('密钥格式应为英文字母')
            return False

    afState = ''

    # 用来补齐key和遍历ciph
    i = 0

    # 用来遍历key
    j = 0

    # 补齐key
    lenBeState = len(beState)
    lenKey = len(key)

    while lenKey < lenBeState:
        key += key[i]
        lenKey = len(key)
        i += 1

    # 加解密算法
    for i in beState:
        # 遍历key
        [k, flag] = switch(key[j])
        j += 1
        [be, flag] = switch(i)

        # 加密
        if choose == 1:
            af = (be + k) % 26

        # 解密
        elif choose == 2:
            af = (be - k) % 26

        if flag == 0:
            afState += lowDict[af]
        else:
            afState += capDict[af]

    return afState


# 主函数
def Vig(choose, text, key):
    # 加密
    if choose == 1:
        plai = text
        ciph = algo(choose, plai, key)
        if ciph is False:
            return '你输入的密钥不符合算法格式（密钥格式应为英文字母）'
        else:
            return ciph

    # 解密
    elif choose == 2:
        ciph = text
        plai = algo(choose, ciph, key)
        if plai is False:
            return '你输入的密钥不符合算法格式（密钥格式应为英文字母）'
        else:
            return plai