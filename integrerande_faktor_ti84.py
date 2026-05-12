# TI-84 Plus CE-T Python Edition
# Integrerande faktor for linjara diffekvationer: yp + g(x)*y = h(x)


def norm(s):
    s = s.replace(" ", "").replace("X", "x").replace("Y", "y")
    s = s.replace("^", "**")
    s = s.replace("y'", "yp")
    return s


def hamta_g(vl, hl):
    # Forvantad form: yp + g(x)*y = h(x)
    sida = vl if "yp" in vl else hl if "yp" in hl else None
    if sida is None:
        return None

    expr = sida.replace("yp", "")
    expr = expr.replace("-", "+-")
    delar = [d for d in expr.split("+") if d != ""]
    for d in delar:
        if "y" in d:
            g = d.replace("*y", "").replace("y*", "").replace("y", "")
            g = g.replace("(", "").replace(")", "")
            if g == "" or g == "+":
                g = "1"
            if g == "-":
                g = "-1"
            return g
    return None


def integral_enkel(g):
    if g == "x":
        return "x^2/2"
    if g == "-x":
        return "-x^2/2"
    if g == "1/x":
        return "ln|x|"
    if g == "2*x":
        return "x^2"
    if g == "3*x**2" or g == "3*x^2":
        return "x^3"
    return "∫(" + g + ")dx"


def main():
    print("Integrerande faktor (I.F.)")
    print("Form: yp + g(x)*y = h(x)")
    vl = norm(input("VL = ").strip())
    hl = norm(input("HL = ").strip())

    g = hamta_g(vl, hl)
    if g is None:
        print("Kunde inte identifiera g(x).")
        print("Skriv pa formen yp + g(x)*y = h(x).")
        return

    G = integral_enkel(g)

    print("\nHela utrakningen:")
    print("1) Skriv om i formen yp + g(x)*y = h(x)")
    print("   ", vl, "=", hl)
    print("2) Identifiera g(x):")
    print("   g(x) =", g)
    print("3) Berakna G(x):")
    print("   G(x) = ∫g(x)dx =", G)
    print("4) Integrerande faktor:")
    print("   I.F. = e^(G(x))")
    print("   I.F. = e^(" + G + ")")


main()
