# Program för TI-84 Plus CE-T Python Edition
# Beräknar tangentekvation och linjär approximation.

import math


def bygg_funktion(expr):
    """Skapar en funktion f(x) från en textsträng."""
    # Vanliga inmatningar i gymnasiematte
    expr = expr.strip()
    if "=" in expr:
        expr = expr.split("=", 1)[1].strip()
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
            "log": math.log10,
            "exp": math.exp,
            "abs": abs,
        }
        return eval(expr, {"__builtins__": {}}, tillatet)

    return f, expr


def numerisk_derivata(f, a, h=1e-5):
    """Central differens: f'(a) ≈ (f(a+h)-f(a-h))/(2h)."""
    return (f(a + h) - f(a - h)) / (2 * h)


def skriv_tangent():
    print("\n--- Bestäm ekvationen till tangenten ---")
    expr_in = input("y = ")
    a = float(input("punkten (x) = "))

    f, expr = bygg_funktion(expr_in)
    fa = f(a)
    m = numerisk_derivata(f, a)

    print("\nFull beräkning:")
    print("f(x) =", expr_in)
    print("a =", a)
    print("f(a) = f({0}) = {1}".format(a, fa))
    print("f'(a) ≈ [f(a+h)-f(a-h)]/(2h), h=1e-5")
    print("f'({0}) ≈ {1}".format(a, m))
    print("Tangentformel: y - f(a) = f'(a)(x - a)")
    print("y - ({0}) = ({1})(x - ({2}))".format(fa, m, a))

    # k-form
    k = m
    m0 = fa - k * a
    print("\nSvar:")
    print("Tangentens ekvation:")
    print("y = {0}x + ({1})".format(k, m0))


def skriv_linjar_approx():
    print("\n--- Bestäm linjär approximation ---")
    expr_in = input("f(x) = ")
    a = float(input("punkten (x) = "))

    f, expr = bygg_funktion(expr_in)
    fa = f(a)
    fpa = numerisk_derivata(f, a)

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
