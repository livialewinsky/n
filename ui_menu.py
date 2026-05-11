"""Enkel menybaserad navigation (MVP)."""
from engine_derivative import derive_polynomial, tangent_at
from ui_forms import ask_float, ask_poly_coeffs


def _show_solution(sol):
    print("\n---", sol["sum"], "---")
    for s in sol["steps"]:
        print(f"Steg {s['id']}: {s['title']}")
        if s.get("expr"):
            print("  ", s["expr"])
        if s.get("calc"):
            print("  ", s["calc"])
    print("Slut:", sol["final"])


def run_main_menu():
    while True:
        print("\n1 Derivata/Tangent")
        print("2 Avsluta")
        c = input("Val: ").strip()
        if c == "1":
            run_derivative_menu()
        elif c == "2":
            break


def run_derivative_menu():
    print("\n1 Derivera polynom")
    print("2 Tangent i punkt")
    c = input("Val: ").strip()
    coeffs = ask_poly_coeffs()
    if c == "1":
        _, sol = derive_polynomial(coeffs)
        _show_solution(sol)
    elif c == "2":
        x0 = ask_float("x0")
        _, sol = tangent_at(coeffs, x0)
        _show_solution(sol)
