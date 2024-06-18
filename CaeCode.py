# 实现凯撒密码
# 小写字典
lowDict = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# 大写字典
capDict = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


# 将字母转换成数字
def switch(ele):
    flag = 0
    if ele.isalpha():
        if ele in lowDict:
            ele = lowDict.index(ele)
        elif ele in capDict:
            ele = capDict.index(ele)
            flag = 1

    return [int(ele), flag]


# beState 处理前  afState 处理后
# 加解密算法
def algo(choose, beState, key):
    afState = ''

    # key返回的flag值是没用的
    [k, flag] = switch(key)

    for i in beState:
        [be, flag] = switch(i)

        # 加密
        if choose == 1:
            af = (be + k) % 26

        # 解密
        if choose == 2:
            af = (be - k) % 26

        if flag == 0:
            afState += lowDict[af]
        else:
            afState += capDict[af]

    return afState


def Cae(choose, text, key):
    # 加密
    if choose == 1:
        plai = text

        return algo(choose, plai, key)

    # 解密
    elif choose == 2:
        ciph = text

        return algo(choose, ciph, key)