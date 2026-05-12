# TI-84 Plus CE-T Python Edition
# Separerbara differentialekvationer


def norm(s):
    s = s.replace(" ", "").replace("X", "x").replace("Y", "y")
    s = s.replace("^", "**")
    s = s.replace("y'", "yp")
    return s


def isolera_yp(vl, hl):
    # Enkel isolering för vanliga former
    if vl == "yp":
        return hl
    if hl == "yp":
        return vl

    if "yp" in vl:
        faktor = vl.replace("*yp", "").replace("yp*", "").replace("yp", "")
        if faktor == "":
            faktor = "1"
        return "(" + hl + ")/(" + faktor + ")"

    if "yp" in hl:
        faktor = hl.replace("*yp", "").replace("yp*", "").replace("yp", "")
        if faktor == "":
            faktor = "1"
        return "(" + vl + ")/(" + faktor + ")"

    return None


def analys_separabel(rhs):
    # Regelbaserad analys för vanliga skoluppgifter
    r = rhs

    if r == "x/y" or r == "x*(1/y)" or r == "x/y":
        return True, "y dy = x dx", "y^2 = x^2 + C", "y = ±sqrt(x^2 + C)", None

    if "x**2*y**2" in r or "x**2*(y**2)" in r:
        return True, "(1/y^2) dy = x^2 dx", "-1/y = x^3/3 + C", "y = -1/(x^3/3 + C)", None

    if "-3*x**2*y" in r or "(-3*x**2)*y" in r:
        return True, "(1/y) dy = -3x^2 dx", "ln|y| = -x^3 + C", "y = C*e^(-x^3)", None

    if "1/(x*y-y)" in r or "1/(y*(x-1))" in r or "1/((x-1)*y)" in r:
        return True, "y dy = (1/(x-1)) dx", "y^2/2 = ln|x-1| + C", "y = ±sqrt(2ln|x-1| + C)", None

    if "exp(x-y)" in r or "e**(x-y)" in r:
        return True, "e^y dy = e^x dx", "e^y = e^x + C", "y = ln(e^x + C)", None

    if "x/(y**4)" in r or "x/y**4" in r:
        return True, "y^4 dy = x dx", "y^5/5 = x^2/2 + C", "y = (5x^2/2 + C)^(1/5)", "pow5"

    if "-y**2*(4*x**3+1)" in r or "-(4*x**3+1)*y**2" in r:
        return True, "(1/y^2)dy = -(4x^3+1)dx", "-1/y = -x^4 - x + C", "y = 1/(x^4 + x + C)", "invpoly"

    return False, "", "", "", None


def los_med_begynnelse(tag, y0):
    if tag == "pow5":
        c = y0**5
        return "y = (5x^2/2 + " + str(c) + ")^(1/5)"
    if tag == "invpoly":
        if y0 == 0:
            return "Ogiltigt begynnelsevillkor: y(0)=0 ger division med 0"
        c = 1 / y0
        return "y = 1/(x^4 + x + " + str(c) + ")"
    return "För detta exempel: sätt in y(0) i den allmänna lösningen för att få C."


def main():
    print("Separerbara differentialekvationer")
    print("Skriv y' som yp i programmet.")
    print("1. Separera variabler")
    print("2. Allmän lösning")
    print("3. Lös med begynnelsevillkor y(0)=...")

    val = input("Välj 1, 2 eller 3: ").strip()
    vl = norm(input("VL = ").strip())
    hl = norm(input("HL = ").strip())

    rhs = isolera_yp(vl, hl)
    if rhs is None:
        print("Ej separabel: kunde inte isolera yp.")
        return

    sep, steg1, steg2, steg3, tag = analys_separabel(rhs)
    if not sep:
        print("Ej separabel (eller ej igenkänd av programmets mallar).")
        print("Isolerad form: yp =", rhs)
        return

    if val == "1":
        print("Separerad form:")
        print(steg1)
    elif val == "2":
        print("Steg:")
        print(steg1)
        print("Allmän lösning:")
        print(steg2)
        print(steg3)
    elif val == "3":
        try:
            y0 = float(input("y(0) = ").strip().replace(",", "."))
        except Exception:
            print("Fel i begynnelsevillkoret")
            return
        print("Steg:")
        print(steg1)
        print(steg2)
        print("Lösning som uppfyller y(0)=", y0)
        print(los_med_begynnelse(tag, y0))
    else:
        print("Ogiltigt val")


main()
