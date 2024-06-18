# 实现url编码
# 保留字符的编码字典
endict = {'!': '%21', '#': '%23', '$': '%24', '&': '%26', "'": '%27', '(': '%28',
          ')': '%29', '*': '%2A', '+': '%2B', ',': '%2C', '/': '%2F', ':': '%3A',
          ';': '%3B', '=': '%3D', '?': '%3F', '@': '%40', '[': '%5B', ']': '%5D'}

# 反编码字典
dedict = {'21': '!', '23': '#', '24': '$', '26': '&', '27': "'", '28': '(',
          '29': ')', '2A': '*', '2B': '+', '2C': ',', '2F': '/', '3A': ':',
          '3B': ';', '3D': '=', '3F': '?', '40': '@', '5B': '[', '5D': ']'}


def url(choose, text):
    list = ''
    # 编码
    if choose == 1:
        for i in text:
            word = i
            if i in endict.keys():
                word = endict[i]
            list += word
        return list

    # 反编码
    elif choose == 2:
        text = text.split('%')
        for i in text:
            if i in dedict.keys():
                list += dedict[i]
            elif text.index(i) == 0:
                list += i
            else:
                list += '%'
                list += i
        return list