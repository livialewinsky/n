# TI-84 Plus CE-T Python Edition
# Separerbara differentialekvationer - visar hela losningen steg for steg


def norm(s):
    s = s.replace(" ", "").replace("X", "x").replace("Y", "y")
    s = s.replace("^", "**")
    s = s.replace("y'", "yp")
    return s


def isolera_yp(vl, hl):
    if vl == "yp":
        return hl
    if hl == "yp":
        return vl
    if "yp" in vl:
        faktor = vl.replace("*yp", "").replace("yp*", "").replace("yp", "") or "1"
        return "(" + hl + ")/(" + faktor + ")"
    if "yp" in hl:
        faktor = hl.replace("*yp", "").replace("yp*", "").replace("yp", "") or "1"
        return "(" + vl + ")/(" + faktor + ")"
    return None


def mall(rhs):
    r = rhs
    if r == "x/y":
        return {
            "sep": ["yp = x/y", "dy/dx = x/y", "y dy = x dx"],
            "allm": ["∫ y dy = ∫ x dx", "y^2/2 = x^2/2 + C", "y^2 = x^2 + C", "y = ±sqrt(x^2 + C)"],
            "tag": "xy"
        }
    if "-3*x**2*y" in r or "(-3*x**2)*y" in r:
        return {
            "sep": ["yp = -3x^2*y", "dy/dx = -3x^2*y", "(1/y)dy = -3x^2 dx"],
            "allm": ["∫(1/y)dy = ∫-3x^2 dx", "ln|y| = -x^3 + C", "y = C*e^(-x^3)"],
            "tag": "expneg"
        }
    if "x/(y**4)" in r or "x/y**4" in r:
        return {
            "sep": ["yp = x/y^4", "dy/dx = x/y^4", "y^4 dy = x dx"],
            "allm": ["∫ y^4 dy = ∫ x dx", "y^5/5 = x^2/2 + C", "y = (5x^2/2 + C)^(1/5)"],
            "tag": "pow5"
        }
    if "-y**2*(4*x**3+1)" in r or "-(4*x**3+1)*y**2" in r:
        return {
            "sep": ["yp = -y^2(4x^3+1)", "dy/dx = -(4x^3+1)y^2", "(1/y^2)dy = -(4x^3+1)dx"],
            "allm": ["∫y^-2 dy = ∫-(4x^3+1)dx", "-1/y = -x^4 - x + C", "1/y = x^4 + x + C", "y = 1/(x^4 + x + C)"],
            "tag": "invpoly"
        }
    if "exp(x-y)" in r or "e**(x-y)" in r:
        return {
            "sep": ["yp = e^(x-y)", "dy/dx = e^x*e^-y", "e^y dy = e^x dx"],
            "allm": ["∫e^y dy = ∫e^x dx", "e^y = e^x + C", "y = ln(e^x + C)"],
            "tag": "expln"
        }
    return None


def los_med_y0(tag, y0):
    if tag == "pow5":
        c = y0**5
        return ["y(0)=" + str(y0), str(y0) + "^5 = C", "C=" + str(c), "y=(5x^2/2 + " + str(c) + ")^(1/5)"]
    if tag == "invpoly":
        if y0 == 0:
            return ["Ogiltigt: y(0)=0 ger division med 0"]
        c = 1 / y0
        return ["y(0)=" + str(y0), "1/" + str(y0) + " = C", "C=" + str(c), "y=1/(x^4+x+" + str(c) + ")"]
    if tag == "expln":
        c = pow(2.718281828, y0) - 1
        return ["e^y = e^x + C", "y(0)=" + str(y0) + " => e^" + str(y0) + " = 1 + C", "C=e^" + str(y0) + "-1", "y=ln(e^x + e^" + str(y0) + " - 1)"]
    return ["Satt in y(0) i den allmanna losningen for att bestamma C."]


def skriv_lista(rader):
    i = 1
    for rad in rader:
        print(str(i) + ")", rad)
        i += 1




def hamta_g_for_if(vl, hl):
    # Forvantad form: yp + g(x)*y = h(x)
    sida = None
    if "yp" in vl:
        sida = vl
    elif "yp" in hl:
        sida = hl
    else:
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
    g = g.strip()
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
    print("Separerbara differentialekvationer")
    print("Skriv y' som yp")
    print("1. Separera variabler")
    print("2. Bestam allman losning")
    print("3. Los med begynnelsevillkor y(0)=...")
    print("4. Ange integrerande faktor (I.F.)")

    val = input("Val 1/2/3/4: ").strip()
    vl = norm(input("VL = ").strip())
    hl = norm(input("HL = ").strip())

    if val == "4":
        g = hamta_g_for_if(vl, hl)
        if g is None:
            print("Kunde inte identifiera g(x) i formen yp + g(x)*y = h(x).")
            return
        G = integral_enkel(g)
        print("Steg for integrerande faktor:")
        print("1) Skriv om pa formen yp + g(x)*y = h(x)")
        print("2) g(x) =", g)
        print("3) G(x) = ∫g(x)dx =", G)
        print("4) I.F. = e^(G(x))")
        print("5) I.F. = e^(" + G + ")")
        return

    rhs = isolera_yp(vl, hl)
    if rhs is None:
        print("Ej separabel: kunde inte isolera yp.")
        return

    m = mall(rhs)
    if m is None:
        print("Ej separabel (eller ej igenkand mall).")
        print("Isolerad form: yp =", rhs)
        return

    if val == "1":
        print("Steg for separering:")
        skriv_lista(m["sep"])
    elif val == "2":
        print("Steg for separering:")
        skriv_lista(m["sep"])
        print("Steg for losning:")
        skriv_lista(m["allm"])
    elif val == "3":
        try:
            y0 = float(input("y(0) = ").strip().replace(",", "."))
        except Exception:
            print("Fel i y(0)")
            return
        print("Steg for separering:")
        skriv_lista(m["sep"])
        print("Steg for allman losning:")
        skriv_lista(m["allm"])
        print("Steg med begynnelsevillkor:")
        skriv_lista(los_med_y0(m["tag"], y0))
    else:
        print("Ogiltigt val")


main()
