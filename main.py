import shutil
from colorama import init, Fore

from attack import LAND_flood_task, arp_spoof
from poc_scan import main_window
from sql_injection import get_form_value_ofinjection, union_sql_injection
from sql_injection_bool import get_form_value_ofbool, sql_injection_bool
from xss_attack.clone_html import clone_htmls

init(autoreset=True)  # 初始化colorama，设置autoreset=True以便在每次打印后自动重置颜色

import scan_dir
import scan_port
import file_upload


def print_centered(text):
    # 获取控制台的宽度
    terminal_width = shutil.get_terminal_size().columns
    # 计算左侧空格数量以实现居中
    left_padding = (terminal_width - len(text)) // 2
    # 打印左侧空格和文本
    print(" " * left_padding + text)

def select_function():
    print(Fore.MAGENTA + "-" * shutil.get_terminal_size().columns)
    print_centered(Fore.MAGENTA + "选择功能模块:")
    print_centered(Fore.MAGENTA + "1. SYN端口扫描")    #1
    print_centered(Fore.MAGENTA + "2. ACK端口扫描")    #2
    print_centered(Fore.MAGENTA + "3. UDP端口扫描")    #3
    print_centered(Fore.MAGENTA + "4. LAND泛红攻击")     #4
    print_centered(Fore.MAGENTA + "5. ARP欺骗")    #7
    print_centered(Fore.MAGENTA + "6. 目录爆破")      #8
    print_centered(Fore.MAGENTA + "7. sql注入检测")   #9
    print_centered(Fore.MAGENTA + "8. 文件上传漏洞检测")   #10
    print_centered(Fore.MAGENTA + "9. web漏洞扫描")
    print_centered(Fore.MAGENTA + "10. XSS攻击")
    print_centered(Fore.MAGENTA + "11. 结束")         #11
    print(Fore.MAGENTA + "-" * shutil.get_terminal_size().columns)


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    while 1:
        select_function()
        # 选择功能模块
        choice = input("请输入功能模块编号:")
        if choice == '1':
            src_ip = input("请输入源ip地址:")
            src_port = int(input("请输入源端口:"))
            dst_ip = input("请输入目标ip地址:")
            dst_port1 = int(input("请输入目标端口开始:"))
            dst_port2 = int(input("请输入目标端口结束:"))
            thread = int(input("请输入线程数:"))
            scan_port.portscan_of_syn(src_ip, src_port, dst_ip, dst_port1, dst_port2, thread)
            print(Fore.CYAN + "SYN端口扫描结束")
        elif choice == '2':
            src_ip = input("请输入源ip地址:")
            src_port = int(input("请输入源端口:"))
            dst_ip = input("请输入目标ip地址:")
            dst_port1 = int(input("请输入目标端口开始:"))
            dst_port2 = int(input("请输入目标端口结束:"))
            thread = int(input("请输入线程数:"))
            scan_port.portscan_of_ack(src_ip, src_port, dst_ip, dst_port1, dst_port2, thread)
            print(Fore.CYAN + "ACK端口扫描结束")
        elif choice == '3':
            src_ip = input("请输入源ip地址:")
            src_port = int(input("请输入源端口:"))
            dst_ip = input("请输入目标ip地址:")
            dst_port1 = int(input("请输入目标端口开始:"))
            dst_port2 = int(input("请输入目标端口结束:"))
            thread = int(input("请输入线程数:"))
            scan_port.portscan_of_udp(src_ip, src_port, dst_ip, dst_port1, dst_port2, thread)
            print(Fore.CYAN + "UDP端口扫描结束")
        elif choice == '4':
            dst_ip = input("请输入目标ip地址:")
            dst_port = input("请输入目标端口:").split()
            dst_port = [int(port) for port in dst_port]
            duration = int(input("请输入持续时间:"))
            max_workers = int(input("请输入最大线程数:"))
            LAND_flood_task(dst_ip, dst_port, duration, max_workers)
            print(Fore.CYAN + "LAND攻击完成")
        elif choice == '5':
            dst_ip = input("请输入目标ip地址:")
            gateway_ip = input("请输入网关ip地址:")
            arp_spoof(dst_ip, gateway_ip)
            print(Fore.CYAN + "arp欺骗结束")
        elif choice == '6':
            url = input("请输入url:")
            print("请选择字典:")
            print("1.自定义字典")
            print("2.默认字典")
            choice_dir = input("请输入:")
            state_codes = input('请输入状态码:').split()
            state_codes = [int(code) for code in state_codes]
            scan_dir.get_request(url, choice_dir, state_codes)
            print(Fore.CYAN + "目录爆破结束")
        elif choice == '7':
            choice_mode = input("请选择模式(1是字符和数字、搜索型注入, 2是盲注):")
            if choice_mode == '1':
                url = input("请输入url:")
                forms_info = get_form_value_ofinjection(url)
                union_sql_injection(url, forms_info)
            elif choice_mode == '2':
                url = input("请输入url:")
                form_info = get_form_value_ofbool(url)
                sql_injection_bool(url, form_info)
            else:
                print(Fore.CYAN + "输入错误")
            print(Fore.CYAN + "sql注入检测完成")
        elif choice == '8':
            url = input("请输入url:")
            file_upload.file_uploads(url)
            print(Fore.CYAN + "文件上传漏洞检测完成")
        elif choice == '9':
            main_window()
            print(Fore.CYAN + "web漏洞扫描结束")
            break
        elif choice == '10':
            url = input("请输入要克隆的url:")
            clone_htmls(url)
            print(Fore.CYAN + "xss攻击结束")
            break
        elif choice == '11':
            print(Fore.CYAN + "程序结束")
            break
        else:
            print(Fore.CYAN + "输入错误")

