"""TI-84 one-file MVP: menu + polynomial derivative/tangent.
ASCII-only and TI-friendly fallback I/O.
"""

# ---------- Helpers ----------
def safe_print(msg=""):
    try:
        print(msg)
    except Exception:
        pass


def safe_input(prompt):
    # TI Python app may behave differently than desktop Python.
    # Keep prompts short and numeric.
    return input(prompt)


# ---------- Step engine ----------
def new_solution(summary):
    return {"sum": summary, "steps": [], "final": None}


def add_step(sol, title, expr="", calc="", result=None):
    sol["steps"].append({
        "id": len(sol["steps"]) + 1,
        "title": title,
        "expr": expr,
        "calc": calc,
        "result": result,
    })


def set_final(sol, final):
    sol["final"] = final


def show_solution(sol):
    safe_print("")
    safe_print("--- " + str(sol["sum"]) + " ---")
    for s in sol["steps"]:
        safe_print("Step " + str(s["id"]) + ": " + str(s["title"]))
        if s.get("expr"):
            safe_print(" " + str(s["expr"]))
        if s.get("calc"):
            safe_print(" " + str(s["calc"]))
        if s.get("result") is not None:
            safe_print(" Result: " + str(s["result"]))
    safe_print("Final: " + str(sol["final"]))


# ---------- Polynomial math ----------
def eval_poly(coeffs, x):
    y = 0.0
    for c in coeffs:
        y = y * x + c
    return y


def derive_poly(coeffs):
    n = len(coeffs) - 1
    if n <= 0:
        return [0.0]
    out = []
    i = 0
    while i < n:
        out.append(coeffs[i] * (n - i))
        i += 1
    return out


def derive_polynomial(coeffs):
    sol = new_solution("Derivative of polynomial")
    d = derive_poly(coeffs)
    add_step(sol, "Apply power rule", expr="(a_n*x^n)' = n*a_n*x^(n-1)", calc="f'(x) coeffs = " + str(d))
    set_final(sol, {"d_coeffs": d})
    return d, sol


def tangent_at(coeffs, x0):
    d = derive_poly(coeffs)
    m = eval_poly(d, x0)
    y0 = eval_poly(coeffs, x0)
    b = y0 - m * x0
    sol = new_solution("Tangent at point")
    add_step(sol, "Derivative coeffs", calc="d = " + str(d))
    add_step(sol, "Slope", calc="m = f'(" + str(x0) + ") = " + str(m))
    add_step(sol, "Point value", calc="y0 = f(" + str(x0) + ") = " + str(y0))
    add_step(sol, "Line", expr="y = m*x + b", calc="b = " + str(b))
    set_final(sol, {"m": m, "b": b, "line": "y=" + str(m) + "*x+" + str(b)})
    return (m, b), sol


# ---------- Forms ----------
def ask_float(prompt):
    while True:
        try:
            return float(safe_input(prompt + ": "))
        except Exception:
            safe_print("Invalid number")


def ask_int(prompt, min_val=None):
    while True:
        try:
            v = int(safe_input(prompt + ": "))
            if min_val is None or v >= min_val:
                return v
            safe_print("Too small")
        except Exception:
            safe_print("Invalid integer")


def ask_poly_coeffs():
    deg = ask_int("Degree", 0)
    coeffs = []
    p = deg
    while p >= 0:
        coeffs.append(ask_float("Coeff x^" + str(p)))
        p -= 1
    return coeffs


# ---------- Menus ----------
def run_derivative_menu():
    safe_print("")
    safe_print("1 Derive polynomial")
    safe_print("2 Tangent at x0")
    safe_print("3 Back")
    c = safe_input("Choice: ").strip()

    if c == "1":
        coeffs = ask_poly_coeffs()
        _, sol = derive_polynomial(coeffs)
        show_solution(sol)
        safe_input("Enter=continue")
    elif c == "2":
        coeffs = ask_poly_coeffs()
        x0 = ask_float("x0")
        _, sol = tangent_at(coeffs, x0)
        show_solution(sol)
        safe_input("Enter=continue")


def run_main_menu():
    while True:
        safe_print("")
        safe_print("TI-84 Math Expert MVP")
        safe_print("1 Derivative/Tangent")
        safe_print("2 Exit")
        c = safe_input("Choice: ").strip()
        if c == "1":
            run_derivative_menu()
        elif c == "2":
            safe_print("Bye")
            break


def main():
    safe_print("Starting...")
    run_main_menu()


# On TI Python app, execute immediately when opened.
try:
    main()
except Exception as e:
    safe_print("ERROR: " + str(e))
    try:
        safe_input("Enter")
    except Exception:
        pass
