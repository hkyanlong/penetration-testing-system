# 实现仿射密码
import math

# 小写字典
lowDict = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
           'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
# 大写字典
capDict = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def switch(ele):  # 将字母转换成数字
    flag = 0
    if ele.isalpha():
        if ele in lowDict:
            ele = lowDict.index(ele)
        elif ele in capDict:
            ele = capDict.index(ele)
            flag = 1
    return [int(ele), flag]


# beState 处理前  afState 处理后
def algo(choose, beState, a, b):  # 加解密算法
    afState = ''
    [a, flag] = switch(a)
    [b, flag] = switch(b)
    if math.gcd(a, 26) != 1 or b < 0 or b >= 26:  # 判断输入的密钥格式
        print('你输入的密钥不符合算法格式')
        return False
    else:
        for i in beState:
            [be, flag] = switch(i)

            # 加密
            if choose == 1:
                af = (a * be + b) % 26

            # 解密
            elif choose == 2:
                inva = int(math.pow(a, 11))
                af = inva * (be - b) % 26
            if flag == 0:
                afState += lowDict[af]
            else:
                afState += capDict[af]
        return afState


def Aff(choose, text, a, b):
    if choose == 1:
        plai = text
        ciph = algo(choose, plai, a, b)
        if ciph is False:
            return '你输入的密钥不符合算法格式（a应与26互素）'
        else:
            return ciph

    elif choose == 2:
        ciph = text
        plai = algo(choose, ciph, a, b)
        if plai is False:
            return '你输入的密钥不符合算法格式（a应与26互素）'
        else:
            return plai