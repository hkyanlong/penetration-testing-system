# 实现RSA密码
import math


# 判断是否为素数
def isPrime(num):
    for i in range(2, num):
        if num % i == 0:
            return False

    return True


def RSA(choose, text, p, q, e):
    text = int(text)
    p = int(p)
    q = int(q)
    e = int(e)

    # 加密
    if choose == 1:
        if not isPrime(p):
            return '你输入的p不是素数'

        if not isPrime(q):
            return '你输入的q不是素数'

        n = p * q
        phiN = (p - 1) * (q - 1)

        # 判断e与φ(n)是否互素
        if math.gcd(e, phiN) != 1:
            falE = '你输入的e与φ(n)不互素\n' \
                   + 'n = ' + str(n) + '\n' \
                   + 'φ(n) = ' + str(phiN)

            return falE

        # 计算e的逆元d
        k = 1
        while (k * phiN + 1) % e != 0:
            k += 1
        d = int((k * phiN + 1) / e)

        plai = text
        ciph = pow(plai, e, n)
        tru = 'n = ' + str(n) + '\n' \
              + 'φ(n) = ' + str(phiN) + '\n' \
              + 'd = ' + str(d) + '\n' \
              + '密文是' + str(ciph)

        return tru

    # 解密
    elif choose == 2:
        if not isPrime(p):
            return '你输入的p不是素数'

        if not isPrime(q):
            return '你输入的q不是素数'

        n = p * q
        phiN = (p - 1) * (q - 1)

        # 判断e与φ(n)是否互素
        if math.gcd(e, phiN) != 1:
            falE = '你输入的e与φ(n)不互素\n' \
                   + 'n = ' + str(n) + '\n' \
                   + 'φ(n) = ' + str(phiN)

            return falE

        # 计算e的逆元d
        k = 1
        while (k * phiN + 1) % e != 0:
            k += 1
        d = int((k * phiN + 1) / e)

        ciph = text
        plai = pow(ciph, d, n)
        tru = 'n = ' + str(n) + '\n' \
              + 'φ(n) = ' + str(phiN) + '\n' \
              + 'd = ' + str(d) + '\n' \
              + '明文是' + str(plai)

        return tru