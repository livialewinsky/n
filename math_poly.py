"""Polynom-verktyg för MVP."""


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
