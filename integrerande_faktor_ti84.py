# TI-84 Plus CE-T Python Edition
# Integrerande faktor for linjara diffekvationer: yp + g(x)*y = h(x)


def norm(s):
    s = s.replace(" ", "").replace("X", "x").replace("Y", "y")
    s = s.replace("^", "**")
    s = s.replace("y'", "yp")
    return s


def hamta_g_h(vl, hl):
    # Forvantad form: yp + g(x)*y = h(x)
    if "yp" not in vl and "yp" not in hl:
        return None, None

    if "yp" in vl:
        sida = vl
        h = hl
    else:
        sida = hl
        h = vl

    expr = sida.replace("yp", "")
    expr = expr.replace("-", "+-")
    delar = [d for d in expr.split("+") if d != ""]
    g = None
    for d in delar:
        if "y" in d:
            g = d.replace("*y", "").replace("y*", "").replace("y", "")
            g = g.replace("(", "").replace(")", "")
            if g == "" or g == "+":
                g = "1"
            if g == "-":
                g = "-1"
            break
    return g, h


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


def los_allman(g, h, G):
    # Specialfall enligt bilagan: yp + x*y = x
    if g == "x" and h == "x":
        return [
            "Multiplicera med I.F.=e^(x^2/2)",
            "yp*e^(x^2/2) + x*y*e^(x^2/2) = x*e^(x^2/2)",
            "d/dx(y*e^(x^2/2)) = x*e^(x^2/2)",
            "∫ d/dx(y*e^(x^2/2)) dx = ∫ x*e^(x^2/2) dx",
            "y*e^(x^2/2) = e^(x^2/2) + C",
            "y = 1 + C*e^(-x^2/2)"
        ]

    return [
        "Allman form med I.F.:",
        "μ(x)=e^(" + G + ")",
        "d/dx(μy) = μ*h(x)",
        "μy = ∫μ*h(x)dx + C",
        "y = (∫μ*h(x)dx + C)/μ"
    ]


def los_med_villkor(g, h, y0):
    if g == "x" and h == "x":
        c = y0 - 1
        return [
            "Allman losning: y = 1 + C*e^(-x^2/2)",
            "Satt x=0: y(0)=1 + C*e^0 = 1 + C",
            "y(0)=" + str(y0) + " => C=" + str(c),
            "Svar: y = 1 + " + str(c) + "*e^(-x^2/2)"
        ]
    return ["For denna form: satt in x=0 och y(0) i allmanna losningen for att bestamma C."]


def main():
    print("Integrerande faktor (I.F.)")
    print("1. Ange integrerande faktor")
    print("2. Bestam allman losning")
    print("3. Los med begynnelsevillkor y(0)=...")

    val = input("Val 1/2/3: ").strip()
    vl = norm(input("VL = ").strip())
    hl = norm(input("HL = ").strip())

    g, h = hamta_g_h(vl, hl)
    if g is None:
        print("Kunde inte identifiera g(x). Skriv pa formen yp + g(x)*y = h(x).")
        return

    G = integral_enkel(g)
    print("\nSteg A (I.F.):")
    print("1) g(x) =", g)
    print("2) G(x) = ∫g(x)dx =", G)
    print("3) I.F. = e^(" + G + ")")

    if val == "1":
        return
    if val == "2":
        print("\nSteg B (allman losning):")
        for r in los_allman(g, h, G):
            print(r)
        return
    if val == "3":
        try:
            y0 = float(input("y(0) = ").strip().replace(",", "."))
        except Exception:
            print("Fel i y(0)")
            return
        print("\nSteg B (allman losning):")
        for r in los_allman(g, h, G):
            print(r)
        print("\nSteg C (begynnelsevillkor):")
        for r in los_med_villkor(g, h, y0):
            print(r)
        return

    print("Ogiltigt val")


main()
