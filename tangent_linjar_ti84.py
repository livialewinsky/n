# Program för TI-84 Plus CE-T Python Edition
# Beräknar tangentekvation, linjär approximation och Maclaurinpolynom.

import math


def normalisera_uttryck(expr):
    """Normaliserar vanlig TI-inmatning till Python-uttryck."""
    expr = expr.replace(" ", "")
    expr = expr.replace("X", "x")

    # Vanliga genvägar: cosx, sinx, tanx, lnx, logx, sqrtx
    expr = expr.replace("cosx", "cos(x)")
    expr = expr.replace("sinx", "sin(x)")
    expr = expr.replace("tanx", "tan(x)")
    expr = expr.replace("lnx", "ln(x)")
    expr = expr.replace("logx", "log(x)")
    expr = expr.replace("sqrtx", "sqrt(x)")

    ut = ""
    prev = ""
    for ch in expr:
        if prev != "":
            implicit = False
            if prev.isdigit() and (ch == "x" or ch == "("):
                implicit = True
            elif prev == ")" and (ch == "x" or ch == "(" or ch.isdigit()):
                implicit = True
            if implicit:
                ut += "*"
        ut += ch
        prev = ch

    return ut


def bygg_funktion(expr):
    expr = expr.strip()
    if "=" in expr:
        expr = expr.split("=", 1)[1].strip()
    expr = normalisera_uttryck(expr)
    expr = expr.replace("^", "**")

    def f(x):
        tillatet = {
            "x": x,
            "e": math.e,
            "pi": math.pi,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "asin": math.asin,
            "acos": math.acos,
            "atan": math.atan,
            "sqrt": math.sqrt,
            "ln": math.log,
            "log": lambda v: math.log(v) / math.log(10),
            "exp": math.exp,
            "abs": abs,
        }
        return eval(expr, {"__builtins__": {}}, tillatet)

    return f, expr


def numerisk_derivata(f, a, h=1e-5):
    return (f(a + h) - f(a - h)) / (2 * h)


def nte_derivata_i_0(f, n, h=1e-4):
    if n == 0:
        return f(0.0)

    def g(x):
        return (f(x + h) - f(x - h)) / (2 * h)

    return nte_derivata_i_0(g, n - 1, h)


def fakultet(n):
    r = 1
    i = 2
    while i <= n:
        r *= i
        i += 1
    return r


def las_funktion(prompt):
    expr_in = input(prompt).strip()
    if expr_in == "":
        print("Fel: Du måste skriva en funktion, t.ex. x^3-x eller y=x^3-x.")
        return None, None, None
    try:
        f, expr = bygg_funktion(expr_in)
        _ = f(1.0)
        return expr_in, f, expr
    except Exception:
        print("Fel i funktionsinmatningen.")
        print("Tips: använd X,T,θ,n-knappen för x och skriv t.ex. 2*x, inte 2x.")
        print("Exempel: y=x^3-x, cos(x), e^-x")
        return None, None, None


def las_punkt():
    raw = input("punkten (x) = ").strip().replace(",", ".")
    try:
        return float(raw)
    except Exception:
        print("Fel: punkten måste vara ett tal, t.ex. -1 eller 2.5")
        return None


def skriv_tangent():
    print("\n--- Bestäm ekvationen till tangenten ---")
    expr_in, f, _expr = las_funktion("y = ")
    if f is None:
        return
    a = las_punkt()
    if a is None:
        return
    try:
        fa = f(a)
        m = numerisk_derivata(f, a)
    except Exception:
        print("Fel: funktionen kunde inte beräknas i den punkten.")
        return

    print("\nFull beräkning:")
    print("f(x) =", expr_in)
    print("a =", a)
    print("f(a) = f({0}) = {1}".format(a, fa))
    print("f'(a) ≈ [f(a+h)-f(a-h)]/(2h), h=1e-5")
    print("f'({0}) ≈ {1}".format(a, m))
    print("y - f(a) = f'(a)(x - a)")
    print("y - ({0}) = ({1})(x - ({2}))".format(fa, m, a))

    k = m
    m0 = fa - k * a
    print("\nSvar: y = {0}x + ({1})".format(k, m0))


def skriv_linjar_approx():
    print("\n--- Bestäm linjär approximation ---")
    _expr_in, f, expr = las_funktion("f(x) = ")
    if f is None:
        return
    a = las_punkt()
    if a is None:
        return
    try:
        fa = f(a)
        fpa = numerisk_derivata(f, a)
    except Exception:
        print("Fel: funktionen kunde inte beräknas i den punkten.")
        return

    print("\nFull beräkning:")
    print("f(x) =", expr)
    print("a =", a)
    print("f(a) =", fa)
    print("f'({0}) ≈ {1}".format(a, fpa))
    print("L(x) = f(a) + f'(a)(x-a)")
    print("L(x) = ({0}) + ({1})(x-({2}))".format(fa, fpa, a))

    k = fpa
    m0 = fa - k * a
    print("\nSvar: L(x) = {0}x + ({1})".format(k, m0))


def skriv_maclaurin():
    print("\n--- Maclaurinpolynom ---")
    _expr_in, f, expr = las_funktion("f(x) = ")
    if f is None:
        return

    try:
        n = int(input("grad n = ").strip())
    except Exception:
        print("Fel: graden måste vara ett heltal.")
        return
    if n < 0:
        print("Fel: graden måste vara 0 eller större.")
        return

    print("\nFull beräkning (kring x=0):")
    print("p_n(x) = Σ (f^(k)(0)/k!) x^k, k=0..n")

    termer = []
    k = 0
    while k <= n:
        dk = nte_derivata_i_0(f, k)
        ak = dk / fakultet(k)
        print("k={0}: f^({0})(0) ≈ {1},  a_{0} = f^({0})(0)/{0}! ≈ {2}".format(k, dk, ak))
        if k == 0:
            termer.append("({0})".format(ak))
        elif k == 1:
            termer.append("({0})*x".format(ak))
        else:
            termer.append("({0})*x^{1}".format(ak, k))
        k += 1

    print("\nSvar:")
    print("p_{0}(x) ≈ ".format(n) + " + ".join(termer))


def meny():
    print("====================================")
    print(" Tangent / Linjär approx / Maclaurin")
    print(" TI-84 Plus CE-T Python Edition")
    print("====================================")
    print("1. Bestäm ekvationen till tangenten")
    print("2. Bestäm linjär approximation")
    print("3. Maclaurinpolynom")

    val = input("Välj 1, 2 eller 3: ").strip()

    if val == "1":
        skriv_tangent()
    elif val == "2":
        skriv_linjar_approx()
    elif val == "3":
        skriv_maclaurin()
    else:
        print("Ogiltigt val. Starta programmet igen.")


meny()
