# TI-84 Plus CE-T Python Edition
# Endast Maclaurinpolynom

import math


def norm(expr):
    expr = expr.replace(" ", "")
    expr = expr.replace("X", "x")
    expr = expr.replace("^", "**")
    expr = expr.replace("sinx", "sin(x)")
    expr = expr.replace("cosx", "cos(x)")
    expr = expr.replace("tanx", "tan(x)")
    expr = expr.replace("lnx", "ln(x)")
    expr = expr.replace("logx", "log(x)")
    expr = expr.replace("sqrtx", "sqrt(x)")

    out = ""
    p = ""
    for c in expr:
        if p:
            if (p.isdigit() and (c == "x" or c == "(")) or (p == ")" and (c == "x" or c == "(" or c.isdigit())):
                out += "*"
        out += c
        p = c
    return out


def bygg_f(expr):
    if "=" in expr:
        expr = expr.split("=", 1)[1]
    expr = norm(expr)

    def f(x):
        env = {
            "x": x,
            "e": math.e,
            "pi": math.pi,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "sqrt": math.sqrt,
            "ln": math.log,
            "log": lambda v: math.log(v) / math.log(10),
            "exp": math.exp,
            "abs": abs,
        }
        return eval(expr, {"__builtins__": {}}, env)

    return f


def fak(n):
    r = 1
    i = 2
    while i <= n:
        r *= i
        i += 1
    return r


def binom(n, k):
    if k < 0 or k > n:
        return 0
    if k > n - k:
        k = n - k
    r = 1
    i = 1
    while i <= k:
        r = r * (n - k + i) // i
        i += 1
    return r


def deriv0(f, n, h=1e-3):
    if n == 0:
        return f(0.0)
    s = 0.0
    j = 0
    while j <= n:
        t = -1 if ((n - j) % 2) else 1
        s += t * binom(n, j) * f(j * h)
        j += 1
    return s / (h ** n)




def fmt(v, d=4):
    return str(round(v, d))

def main():
    print("Maclaurinpolynom (TI-84)")
    ex = input("f(x) = ").strip()
    if ex == "":
        print("Fel: tom funktion")
        return
    try:
        f = bygg_f(ex)
        _ = f(0.0)
    except Exception:
        print("Fel i funktionen. Exempel: cos(x), e^-x, exp(-x)")
        return

    try:
        n = int(input("grad n (0..4) = ").strip())
    except Exception:
        print("Fel: grad måste vara heltal")
        return

    if n < 0 or n > 4:
        print("Välj grad 0..4 (för minne/stabilitet).")
        return

    print("\nFull beräkning:")
    terms = []
    formel_terms = []
    k = 0
    while k <= n:
        d = deriv0(f, k)
        a = d / fak(k)
        print("k=", k, " f^k(0)≈", fmt(d), " a_k≈", fmt(a))
        if k == 0:
            terms.append("(" + fmt(a) + ")")
            formel_terms.append("f(0)")
        elif k == 1:
            terms.append("(" + fmt(a) + ")*x")
            formel_terms.append("f'(0)x")
        else:
            terms.append("(" + fmt(a) + ")*x^" + str(k))
            formel_terms.append("f^(" + str(k) + ")(0)/" + str(k) + "!*x^" + str(k))
        k += 1

    print("\nSvar (avrundat):")
    print("p_" + str(n) + "(x) ≈ " + " + ".join(terms))
    print("Alternativ formel:")
    print("p(x) = " + " + ".join(formel_terms))


main()
