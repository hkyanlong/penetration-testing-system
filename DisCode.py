# 实现纵栏式移项密码
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


def Dis(choose, text, key):
    dict = {}
    lis = ''
    text = list(text)

    # 加密
    if choose == 1:
        while text != []:
            for i in key:
                [ele, flag] = switch(i)

                # 添加字典
                dict.setdefault(ele, '')
                if text == []:
                    break

                # 置换
                else:
                    temp = dict[ele] + text.pop(0)
                    dict[ele] = temp

        # 排序
        while dict != {}:
            minindex = min(dict.keys())
            lis += dict[minindex]
            dict.pop(minindex)

        return lis

    # 解密
    elif choose == 2:
        textNum = len(text)
        keyNum = len(key)

        # num用于计算每个数组的个数
        num = textNum // keyNum

        # re用于计算多余的字符
        re = textNum % keyNum

        while text != []:
            for i in key:
                [ele, flag] = switch(i)
                dict.setdefault(ele, '')

                # 置换
                if re != 0:
                    dict[ele] = text[0:num + 1]
                    re -= 1
                    for j in range(0, num + 1):
                        text.pop(0)
                else:
                    dict[ele] = text[0:num]
                    for j in range(0, num):
                        text.pop(0)

        # 排序
        tempList = sorted(dict.keys())
        tempLen = len(tempList)

        while tempLen > 0:
            for i in tempList:
                if dict[i] == []:
                    tempLen -= 1
                elif dict[i] != []:
                    lis += dict[i][0]
                    dict[i] = dict[i][1:]

        return lis