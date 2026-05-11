# Program för TI-84 Plus CE-T Python Edition
# Beräknar tangentekvation och linjär approximation.

import math


def normalisera_uttryck(expr):
    """Normaliserar vanlig TI-inmatning till Python-uttryck."""
    expr = expr.replace(" ", "")
    # Acceptera både x och X från olika TI-inmatningslägen
    expr = expr.replace("X", "x")

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
    """Skapar en funktion f(x) från en textsträng."""
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
            # TI-Python kan sakna math.log10, använd basbytesformel
            "log": lambda v: math.log(v) / math.log(10),
            "exp": math.exp,
            "abs": abs,
        }
        return eval(expr, {"__builtins__": {}}, tillatet)

    return f, expr


def numerisk_derivata(f, a, h=1e-5):
    """Central differens: f'(a) ≈ (f(a+h)-f(a-h))/(2h)."""
    return (f(a + h) - f(a - h)) / (2 * h)


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
        print("Exempel på giltig inmatning: y=x^3-x")
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
    print("Tangentformel: y - f(a) = f'(a)(x - a)")
    print("y - ({0}) = ({1})(x - ({2}))".format(fa, m, a))

    k = m
    m0 = fa - k * a
    print("\nSvar:")
    print("Tangentens ekvation:")
    print("y = {0}x + ({1})".format(k, m0))


def skriv_linjar_approx():
    print("\n--- Bestäm linjär approximation ---")
    expr_in, f, expr = las_funktion("f(x) = ")
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
    print("f'(a) ≈ [f(a+h)-f(a-h)]/(2h), h=1e-5")
    print("f'({0}) ≈ {1}".format(a, fpa))
    print("Linjär approximation:")
    print("L(x) = f(a) + f'(a)(x-a)")
    print("L(x) = ({0}) + ({1})(x-({2}))".format(fa, fpa, a))

    k = fpa
    m0 = fa - k * a
    print("\nSvar:")
    print("L(x) = {0}x + ({1})".format(k, m0))


def meny():
    print("====================================")
    print(" Tangent & Linjär approximation")
    print(" TI-84 Plus CE-T Python Edition")
    print("====================================")
    print("1. Bestäm ekvationen till tangenten")
    print("2. Bestäm linjär approximation")

    val = input("Välj 1 eller 2: ").strip()

    if val == "1":
        skriv_tangent()
    elif val == "2":
        skriv_linjar_approx()
    else:
        print("Ogiltigt val. Starta programmet igen.")


meny()
