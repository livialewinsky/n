"""Formulär för numerisk inmatning."""


def ask_float(prompt):
    return float(input(prompt + ": "))


def ask_int(prompt, min_val=None):
    while True:
        v = int(input(prompt + ": "))
        if min_val is None or v >= min_val:
            return v
        print("För lågt värde.")


def ask_poly_coeffs():
    deg = ask_int("Grad", 0)
    coeffs = []
    for p in range(deg, -1, -1):
        coeffs.append(ask_float(f"Koefficient för x^{p}"))
    return coeffs
