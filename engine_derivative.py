"""Derivata/Tangent-motor (polynom i MVP)."""
from math_poly import derive_poly, eval_poly
from step_engine import add_step, new_solution, set_final


def derive_polynomial(coeffs):
    sol = new_solution("Derivera polynom")
    d = derive_poly(coeffs)
    add_step(sol, "Använd derivataregel", expr="(a_n x^n)' = n*a_n x^(n-1)", calc=f"f'(x) koeff = {d}")
    set_final(sol, {"d_coeffs": d})
    return d, sol


def tangent_at(coeffs, x0):
    d = derive_poly(coeffs)
    m = eval_poly(d, x0)
    y0 = eval_poly(coeffs, x0)
    b = y0 - m * x0
    sol = new_solution("Tangent i punkt")
    add_step(sol, "Beräkna f'(x)", calc=f"d_coeffs = {d}")
    add_step(sol, "Sätt in x0", calc=f"m = f'({x0}) = {m}")
    add_step(sol, "Beräkna y0", calc=f"y0 = f({x0}) = {y0}")
    add_step(sol, "Bygg linje", expr="y = m*x + b", calc=f"b = {b}")
    set_final(sol, {"m": m, "b": b})
    return (m, b), sol
