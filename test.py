# 实现图形化，用户的输入口
import tkinter as tk
import tkinter.messagebox
import CaeCode
import AffiCode
import VigCode
import RSACode
import Base64
import DisCode
import URL


def coChoose():
    # 凯撒加密
    if codeVar.get() == 0:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        key = enKey.get('1.0', tk.END)
        key = key.strip()

        prin = CaeCode.Cae(1, text, key)
        buT.config(text=prin)

    # 仿射加密
    elif codeVar.get() == 1:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        a = enKey.get('1.0', '1.0 lineend')
        a = a.strip()

        b = enKey.get('2.0', '2.0 lineend')
        b = b.strip()

        prin = AffiCode.Aff(1, text, a, b)
        buT.config(text=prin)

    # 维吉尼亚加密
    elif codeVar.get() == 2:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        key = enKey.get('1.0', tk.END)
        key = key.strip()

        prin = VigCode.Vig(1, text, key)
        buT.config(text=prin)

    # RSA加密
    elif codeVar.get() == 3:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        p = enKey.get('1.0', '1.0 lineend')
        p = p.strip()

        q = enKey.get('2.0', '2.0 lineend')
        q = q.strip()

        e = enKey.get('3.0', '3.0 lineend')
        e = e.strip()

        prin = RSACode.RSA(1, text, p, q, e)
        buT.config(text=prin)

    # Base64编码
    elif codeVar.get() == 4:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        prin = Base64.Base(1, text)
        buT.config(text=prin)

    # 纵栏式移项加密
    elif codeVar.get() == 5:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        key = enKey.get('1.0', tk.END)
        key = key.strip()

        prin = DisCode.Dis(1, text, key)
        buT.config(text=prin)

    # url编码
    elif codeVar.get() == 6:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        prin = URL.url(1, text)
        buT.config(text=prin)


def deChoose():
    # 凯撒解密
    if codeVar.get() == 0:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        key = enKey.get('1.0', tk.END)
        key = key.strip()

        prin = CaeCode.Cae(2, text, key)
        buT.config(text=prin)

    # 仿射解密
    elif codeVar.get() == 1:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        a = enKey.get('1.0', '1.0 lineend')
        a = a.strip()

        b = enKey.get('2.0', '2.0 lineend')
        b = b.strip()

        prin = AffiCode.Aff(2, text, a, b)
        buT.config(text=prin)

    # 维吉尼亚解密
    elif codeVar.get() == 2:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        key = enKey.get('1.0', tk.END)
        key = key.strip()

        prin = VigCode.Vig(2, text, key)
        buT.config(text=prin)

    # RSA解密
    elif codeVar.get() == 3:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        p = enKey.get('1.0', '1.0 lineend')
        p = p.strip()

        q = enKey.get('2.0', '2.0 lineend')
        q = q.strip()

        e = enKey.get('3.0', '3.0 lineend')
        e = e.strip()

        prin = RSACode.RSA(2, text, p, q, e)
        buT.config(text=prin)

    # Base64编码
    elif codeVar.get() == 4:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        prin = Base64.Base(2, text)
        buT.config(text=prin)

    # 纵栏式移项解密
    elif codeVar.get() == 5:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        key = enKey.get('1.0', tk.END)
        key = key.strip()

        prin = DisCode.Dis(2, text, key)
        buT.config(text=prin)

    # url解码
    elif codeVar.get() == 6:
        text = enText.get('1.0', tk.END)
        text = text.strip()

        prin = URL.url(2, text)
        buT.config(text=prin)


def helpCommand():
    tk.messagebox.showinfo('帮助(H)', '使用仿射密码时，密钥从上往下分别输入a，b\n'
                           + '使用RSA密码时，从上往下分别为p，q，e')


# 主窗口及格式
window = tk.Tk()
window.title('加解密工具')
window.configure(background='White')

width = 800
height = 600
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
window.geometry(size_geo)

window.resizable(width=False, height=False)

# 密码编码选项框架
coFrame = tk.Frame(window, bg='white')
coFrame.grid(padx=15, pady=10, row=0, column=0, rowspan=3)

codeVar = tk.IntVar()

code1 = tk.Radiobutton(coFrame, text="凯撒密码", bg='white', variable=codeVar, value=0)
code1.grid(ipadx=20, ipady=15, row=0, column=0)

code2 = tk.Radiobutton(coFrame, text="仿射密码", bg='white', variable=codeVar, value=1)
code2.grid(ipadx=20, ipady=15, row=1, column=0)

code3 = tk.Radiobutton(coFrame, text="维吉尼亚密码", bg='white', variable=codeVar, value=2)
code3.grid(ipadx=20, ipady=15, row=2, column=0)

code4 = tk.Radiobutton(coFrame, text="RSA密码", bg='white', variable=codeVar, value=3)
code4.grid(ipadx=20, ipady=15, row=3, column=0)

code5 = tk.Radiobutton(coFrame, text="Base64", bg='white', variable=codeVar, value=4)
code5.grid(ipadx=20, ipady=15, row=4, column=0)

code6 = tk.Radiobutton(coFrame, text="纵栏式移项密码", bg='white', variable=codeVar, value=5)
code6.grid(ipadx=20, ipady=15, row=5, column=0)

code7 = tk.Radiobutton(coFrame, text="url编码", bg='white', variable=codeVar, value=6)
code7.grid(ipadx=20, ipady=15, row=6, column=0)

# 输入输出框架
entry = tk.Frame(window, bg='white')
entry.grid(padx=15, pady=10, row=0, column=3)

enLabel = tk.Label(entry, text='请输入文本：', bg='white')
enLabel.grid(ipadx=20, ipady=15, row=0, column=0)

enText = tk.Text(entry, width=30, height=7)
enText.grid(ipadx=20, ipady=15, row=1, column=0)

enLabel = tk.Label(entry, text='请输入密钥：', bg='white')
enLabel.grid(ipadx=20, ipady=15, row=2, column=0)

enKey = tk.Text(entry, width=30, height=7)
enKey.grid(ipadx=20, ipady=15, row=3, column=0)

# 加密解密选项
edVar = tk.IntVar()
en = tk.Button(window, text='加密（编码）', bg='white', command=coChoose)
en.grid(padx=10, pady=5, row=0, column=4)

de = tk.Button(window, text='解密（解码）', bg='white', command=deChoose)
de.grid(padx=10, pady=5, row=1, column=4)

# 输出结果
buT = tk.Label(window, text='')
buT.grid(row=5, column=3)

# 菜单
mainmenu = tk.Menu(window)

mainmenu.add_command(label="文件")
mainmenu.add_command(label="编辑")
mainmenu.add_command(label="格式")
mainmenu.add_command(label="查看")
mainmenu.add_command(label="帮助", command=helpCommand)

# 显示菜单
window.config(menu=mainmenu)

window.mainloop()