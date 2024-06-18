import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse

# 要克隆的网页URL
url = 'http://localhost:8083/vul/xss/xss_reflected_get.php'

# 发送HTTP GET请求
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 获取网页内容
    html_content = response.text

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 创建资源目录
    os.makedirs('local_resources', exist_ok=True)


    # 修正资源路径并下载资源
    def download_resource(resource_url, folder):
        try:
            response = requests.get(resource_url)
            if response.status_code == 200:
                # 获取文件名
                parsed_url = urlparse(resource_url)
                file_name = os.path.basename(parsed_url.path)
                # 保存文件
                file_path = os.path.join(folder, file_name)
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f'资源已下载：{file_path}')
                return os.path.join(folder, file_name)
            else:
                print(f'无法下载资源：{resource_url}')
                return resource_url
        except Exception as e:
            print(f'下载资源时出错：{e}')
            return resource_url


    # 下载CSS、JS、图片资源并修正路径
    for tag in soup.find_all(['link', 'script', 'img']):
        if tag.has_attr('href'):
            resource_url = urljoin(url, tag['href'])
            local_path = download_resource(resource_url, 'local_resources')
            tag['href'] = local_path
        if tag.has_attr('src'):
            resource_url = urljoin(url, tag['src'])
            local_path = download_resource(resource_url, 'local_resources')
            tag['src'] = local_path

    # 将修改后的HTML内容保存到本地文件
    with open('cloned_page.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print('网页已成功克隆并保存为 cloned_page.html')
else:
    print(f'请求失败，状态码：{response.status_code}')
