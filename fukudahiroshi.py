"""
Code imported from
https://kilin.clas.kitasato-u.ac.jp/software/markov/markov.html

Usage:
markov(form.textin.value)
mpower(form.textin.value, form.textin2.value)
"""


def new_array(n):
    """
        Wrapper for matrix creation, to replace new Array(n) from JS
    :param n:
    :return:
    """
    return [None] * n


def mpower(c, v):
    p = to_matrix(c)
    n = p.length
    pp = new_array(n)
    summ = new_array(n)
    # i,j,k,l
    for i in range(n):
        pp[i] = new_array(n)
        summ[i] = new_array(n)
        for j in range(n):
            pp[i][j] = p[i][j]
            summ[i][j] = 0

    for l in range(1, v):
        for i in range(n):
            for j in range(n):
                summ[i][j] = 0

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    summ[i][j] += pp[i][k] * p[k][j]

        for i in range(n):
            for j in range(n):
                pp[i][j] = summ[i][j]

    return print2dmf(pp, 2)


def replaceall(st, c, cc):
    while st.index(c) > -1:
        st = st.replace(c, cc)


# def to_matrix(c):
#     # obtain array p[][] from strings c
#     # i,j
#     cin = c
#     replaceall(cin, "\t", " ")
#     replaceall(cin, ",", " ")
#     replaceall(cin, "  ", " ")
#
#     n = 0
#     cl = cin.split("\n")
#     for i in range(len(cl)):
#         while cl[i].index(" ") == 0:
#             cl[i] = cl[i].replace(" ", "")
#         if len(cl[i]) <= 1:
#             break
#         n += 1
#
#     p = new_array(n)
#     for i in range(n):
#         p[i] = new_array(n)
#         cc = cl[i].split(" ")
#         for j in range(n):
#             # p[i][j] = Number(cc[j])
#             p[i][j] = float(cc[j])
#
#     return p


# def markov(c):
#     p = to_matrix(c)
def markov(p):
    n = len(p)
    # print("p=\n"+print2dm(p,n,n))

    # add normalization condition
    m = n + 1
    a = new_array(m)
    for i in range(m):
        a[i] = new_array(m)
        for j in range(m):
            a[i][j] = 0

    for j in range(m):
        a[0][j] = 1

    # copy transverse of p-1 to a
    for i in range(n):
        for j in range(n):
            if i != j:
                a[i + 1][j] = p[j][i]
            else:
                a[i + 1][j] = p[j][i] - 1

    # print("a=\n"+print2dm(a,m,m))

    f = new_array(n)
    gaussj(a, n, f)

    # return print1dmf(f, 3)
    return f


def print1dm(a):
    return print1dmf(a, -1)


def print1dmf(a, l):
    res = ""
    for i in range(len(a)):
        res += str(i + 1) + ": " + pfmt(a[i], l) + "\n"
    return res


def print2dm(a):
    return print2dmf(a, -1)


def print2dmf(a, l):
    res = ""
    for i in range(len(a)):
        for j in range(len(a[i])):
            res += pfmt(a[i][j], l) + " "
        res += "\n"
    return res


def pfmt(v, l):
    if l < 0:
        return str(v)

    a = 1
    for i in range(l):
        a *= 10

    s = str(round(v * a) / a)
    for i in range(l + 2 - len(s)):
        s += " "

    return s


def gaussj(a, n, f):
    m = n + 1

    # implicit pivoting
    for i in range(m):
        amx = abs(a[i][0])
        for j in range(1, n):
            if amx < abs(a[i][j]):
                amx = abs(a[i][j])
        for j in range(m):
            a[i][j] /= amx

    for i in range(n):
        # print("i="+String(i))
        # select pivot
        if i > 0:
            r = i
            for k in range(i + 1, m):
                if abs(a[r][i]) < abs(a[k][i]):
                    r = k
            # print("pivot="+r)

            for j in range(m):
                t = a[i][j]
                a[i][j] = a[r][j]
                a[r][j] = t

        # normalize line i
        d = a[i][i]
        for j in range(i, m):
            a[i][j] /= d

        # subtract line i from k!=i.
        for k in range(m):
            if k != i:
                d = a[k][i]
                for j in range(i, m):
                    a[k][j] -= d * a[i][j]
        # print("ai3=\n"+print2dm(a))

    for i in range(n):
        f[i] = a[i][m - 1]
