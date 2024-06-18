# 实现Base64编码
# A - Z: 65 - 90  a - z: 97 - 122

# Base64索引表 + '='
Base64 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
          'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
          'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/', '=']


def Base(choose, text):
    if choose == 1:
        tru = ''
        # 二进制形式
        binary = []

        # 将文本转换成对应的ASCII编码，再转换成二进制位
        for i in text:
            num = ord(i)
            # div: 除数  re: 余数  ele: 单个字母二进制元素
            div = 1
            ele = []

            while div != 0:
                div = num // 2
                re = num % 2
                num = div
                ele.append(re)

            # 单个字节补齐8位
            while len(ele) < 8:
                ele.append(0)
            ele.reverse()
            binary += ele

        # 每3个字节补齐24位
        while len(binary) % 24 != 0:
            binary.append(0)

        # 每6位二进制数为一个Base64编码索引
        while binary != []:
            flag = 0
            num = ''
            while flag < 6:
                num += str(binary.pop(0))
                flag += 1
            index = int(num, 2)

            # 判断全0索引是'A'还是'='
            if index == 0 and 1 not in binary:
                index = 64
            tru += Base64[index]
            tru += ''

        return tru

    # 解码
    elif choose == 2:
        tru = ''
        coding = text
        binary = []

        for i in coding:
            index = Base64.index(i)
            if index != 64:
                div = 1
                ele = []

                while div != 0:
                    div = index // 2
                    re = index % 2
                    index = div
                    ele.append(re)

                # 单个字节补齐6位
                while len(ele) < 6:
                    ele.append(0)
                ele.reverse()

            else:
                ele = [0, 0, 0, 0, 0, 0]
            binary += ele

        while binary != []:
            flag = 0
            num = ''
            while flag < 8:
                num += str(binary.pop(0))
                flag += 1
            index = int(num, 2)

            # 判断全0索引是'A'还是'='
            if index == 0 and 1 not in binary:
                break
            tru += chr(index)
            tru += ''

        return tru