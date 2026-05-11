"""TI-84 Plus CE-T Python Edition: en-fils MVP (meny + formulär + matemotor + stegmotor)."""

# ======== MODELLER ========
def new_func(family, params, label="f(x)"):
    return {"f": family, "p": params, "m": {"l": label}}


def new_problem(topic, subtopic, func, inputs):
    return {"t": topic, "s": subtopic, "fn": func, "in": inputs}


# ======== STEGMOTOR ========
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
    print("\n---", sol["sum"], "---")
    for s in sol["steps"]:
        print("Steg", s["id"], ":", s["title"])
        if s.get("expr"):
            print(" ", s["expr"])
        if s.get("calc"):
            print(" ", s["calc"])
        if s.get("result") is not None:
            print(" Resultat:", s["result"])
    print("Slut:", sol["final"])


# ======== POLYNOM ========
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
    for i, c in enumerate(coeffs[:-1]):
        out.append(c * (n - i))
    return out


# ======== DERIVATA/TANGENT-MOTOR ========
def derive_polynomial(coeffs):
    sol = new_solution("Derivera polynom")
    d = derive_poly(coeffs)
    add_step(sol, "Använd derivataregel", expr="(a_n*x^n)' = n*a_n*x^(n-1)", calc="f'(x)-koeff = " + str(d))
    set_final(sol, {"d_coeffs": d})
    return d, sol


def tangent_at(coeffs, x0):
    d = derive_poly(coeffs)
    m = eval_poly(d, x0)
    y0 = eval_poly(coeffs, x0)
    b = y0 - m * x0
    sol = new_solution("Tangent i punkt")
    add_step(sol, "Beräkna derivatan", calc="d_coeffs = " + str(d))
    add_step(sol, "Beräkna lutning", calc="m = f'(" + str(x0) + ") = " + str(m))
    add_step(sol, "Beräkna punktvärde", calc="y0 = f(" + str(x0) + ") = " + str(y0))
    add_step(sol, "Bygg tangent", expr="y = m*x + b", calc="b = y0 - m*x0 = " + str(b))
    set_final(sol, {"m": m, "b": b, "line": "y=" + str(m) + "*x+" + str(b)})
    return (m, b), sol


# ======== FORMULÄR ========
def ask_float(prompt):
    return float(input(prompt + ": "))


def ask_int(prompt, min_val=None):
    while True:
        v = int(input(prompt + ": "))
        if min_val is None or v >= min_val:
            return v
        print("För lågt värde")


def ask_poly_coeffs():
    deg = ask_int("Grad", 0)
    coeffs = []
    p = deg
    while p >= 0:
        coeffs.append(ask_float("Koefficient för x^" + str(p)))
        p -= 1
    return coeffs


# ======== MENYER ========
def run_derivative_menu():
    print("\n1 Derivera polynom")
    print("2 Tangent i punkt")
    print("3 Tillbaka")
    c = input("Val: ").strip()

    if c == "1":
        coeffs = ask_poly_coeffs()
        _, sol = derive_polynomial(coeffs)
        show_solution(sol)
    elif c == "2":
        coeffs = ask_poly_coeffs()
        x0 = ask_float("x0")
        _, sol = tangent_at(coeffs, x0)
        show_solution(sol)


def run_main_menu():
    while True:
        print("\n=== TI-84 Matteexpertsystem (MVP) ===")
        print("1 Derivata/Tangent")
        print("2 Avsluta")
        c = input("Val: ").strip()
        if c == "1":
            run_derivative_menu()
        elif c == "2":
            print("Avslutar...")
            break


def main():
    run_main_menu()


if __name__ == "__main__":
    main()
