# TI-84 Plus CE-T Python Edition
# Newton-Raphsons metod för f(x)=0

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
        expr = expr.split("=", 1)[0]
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

    return f, expr


def deriv(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)


def r4(v):
    return round(v, 4)


def main():
    print("Newton-Raphsons metod (TI-84)")
    print("Loser ekvationer på formen f(x)=0")
    print("Formel: x_(n+1) = x_n - f(x_n)/f'(x_n)")

    expr_in = input("Skriv vänsterledet i f(x)=0 (t.ex. x^3-x^2-3): ").strip()
    if expr_in == "":
        print("Fel: tom funktion")
        return

    try:
        f, expr = bygg_f(expr_in)
        _ = f(1.0)
    except Exception:
        print("Fel i funktionen. Exempel: x^3-x^2-3")
        return

    print("\nValfri kontroll av tecken (heltal):")
    try:
        a = int(input("Start heltal a (t.ex. 1): ").strip())
        b = int(input("Slut heltal b (t.ex. 2): ").strip())
        fa = f(a)
        fb = f(b)
        print("f({0})={1}, f({2})={3}".format(a, r4(fa), b, r4(fb)))
        if fa * fb < 0:
            print("Teckenbyte hittat -> nollställe mellan", a, "och", b)
    except Exception:
        print("Hoppar över teckenkontroll.")

    try:
        x = float(input("Välj startvärde x0: ").strip().replace(",", "."))
    except Exception:
        print("Fel: ogiltigt startvärde")
        return

    max_iter = 10
    tol = 0.0005  # för 3 korrekta decimaler

    print("\nBeräkning steg för steg:")
    print("f(x)=", expr)
    n = 0
    while n < max_iter:
        fx = f(x)
        dfx = deriv(f, x)
        if abs(dfx) < 1e-12:
            print("Avbryter: f'(x_n) blev nära 0.")
            return

        x_next = x - fx / dfx
        print("Iteration", n + 1)
        print("x_n =", r4(x))
        print("f(x_n) =", r4(fx))
        print("f'(x_n) ~", r4(dfx))
        print("x_(n+1) = x_n - f(x_n)/f'(x_n)")
        print("x_(n+1) ~", r4(x_next))
        print("---")

        if abs(x_next - x) < tol:
            x = x_next
            break
        x = x_next
        n += 1

    print("Svar:")
    print("x ~", round(x, 3), "(tre korrekta decimaler)")


main()
