import math


def norm(expr):
    expr = expr.replace(" ", "").replace("X", "x").replace("^", "**")
    expr = expr.replace("sinx", "sin(x)").replace("cosx", "cos(x)")
    expr = expr.replace("tanx", "tan(x)").replace("lnx", "ln(x)")
    expr = expr.replace("logx", "log(x)").replace("sqrtx", "sqrt(x)")
    out = ""
    p = ""
    for c in expr:
        if p and ((p.isdigit() and (c == "x" or c == "(")) or (p == ")" and (c == "x" or c == "(" or c.isdigit()))):
            out += "*"
        out += c
        p = c
    return out


def bygg_f(expr):
    if "=" in expr:
        expr = expr.split("=", 1)[1]
    expr = norm(expr)

    def f(x):
        env = {"x": x, "e": math.e, "pi": math.pi, "sin": math.sin, "cos": math.cos,
               "tan": math.tan, "sqrt": math.sqrt, "ln": math.log,
               "log": lambda v: math.log(v) / math.log(10), "exp": math.exp, "abs": abs}
        return eval(expr, {"__builtins__": {}}, env)

    return f, expr


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


def snygg(v):
    return str(int(round(v)))


def derivata_rad(expr, k, val):
    if expr == "ln(x+1)" or expr == "ln(1+x)":
        if k == 0:
            return "f(0)=ln(0+1)=ln(1)=" + snygg(val)
        if k == 1:
            return "f'(x)=1/(x+1), f'(0)=1/(0+1)=" + snygg(val)
        if k == 2:
            return "f''(x)=-1/(x+1)^2, f''(0)=-1/(0+1)^2=" + snygg(val)
        if k == 3:
            return "f'''(x)=2/(x+1)^3, f'''(0)=2/(0+1)^3=" + snygg(val)

    if expr == "cos(x)":
        m = k % 4
        if m == 0:
            return "f^({0})(0)=cos(0)={1}".format(k, snygg(val))
        if m == 1:
            return "f^({0})(0)=-sin(0)={1}".format(k, snygg(val))
        if m == 2:
            return "f^({0})(0)=-cos(0)={1}".format(k, snygg(val))
        return "f^({0})(0)=sin(0)={1}".format(k, snygg(val))

    if expr == "exp(-x)" or expr == "e**-x" or expr == "e**(-x)":
        tecken = "" if (k % 2 == 0) else "-"
        return "f^({0})(0)={1}e^-0={2}".format(k, tecken, snygg(val))

    return "f^({0})(0)≈{1}".format(k, snygg(val))


def main():
    print("Maclaurinpolynom (TI-84)")
    ex = input("f(x) = ").strip()
    if ex == "":
        print("Fel: tom funktion")
        return
    try:
        f, expr_norm = bygg_f(ex)
        _ = f(0.0)
    except Exception:
        print("Fel i funktionen. Exempel: ln(x+1), cos(x), e^-x")
        return

    try:
        n = int(input("grad n (0..4) = ").strip())
    except Exception:
        print("Fel: grad måste vara heltal")
        return

    if n < 0 or n > 4:
        print("Välj grad 0..4")
        return

    print("\nFull beräkning:")
    terms = []
    formel_terms = []
    k = 0
    while k <= n:
        d = deriv0(f, k)
        a = d / fak(k)
        print(derivata_rad(expr_norm, k, d))
        print("a_{0}=f^({0})(0)/{0}!= {1}".format(k, snygg(a)))
        if k == 0:
            terms.append("(" + snygg(a) + ")")
            formel_terms.append("f(0)")
        elif k == 1:
            terms.append("(" + snygg(a) + ")*x")
            formel_terms.append("f'(0)x")
        else:
            terms.append("(" + snygg(a) + ")*x^" + str(k))
            formel_terms.append("f^(" + str(k) + ")(0)/" + str(k) + "!*x^" + str(k))
        k += 1

    print("\nSvar (heltal):")
    print("p_" + str(n) + "(x) ≈ " + " + ".join(terms))
    print("Alternativ formel:")
    print("p(x) = " + " + ".join(formel_terms))


main()
