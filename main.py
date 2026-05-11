"""TI-84 matteexpertsystem (en fil, svenska menyer, metodbaserat)."""

# ---------- Bas I/O ----------
def skriv(msg=""):
    try:
        print(msg)
    except Exception:
        pass


def las(prompt):
    return input(prompt)


def las_float(prompt):
    while True:
        try:
            return float(las(prompt + ": "))
        except Exception:
            skriv("Ogiltigt tal")


def las_int(prompt, minv=None):
    while True:
        try:
            v = int(las(prompt + ": "))
            if minv is None or v >= minv:
                return v
            skriv("For litet")
        except Exception:
            skriv("Ogiltigt heltal")


# ---------- Stegmotor ----------
def ny_losning(sammanfattning):
    return {"sum": sammanfattning, "steg": [], "slut": None}


def lagg_till_steg(sol, titel, uttryck="", ber="", res=None):
    sol["steg"].append({
        "id": len(sol["steg"]) + 1,
        "titel": titel,
        "uttryck": uttryck,
        "ber": ber,
        "res": res,
    })


def satt_slut(sol, slut):
    sol["slut"] = slut


def visa_losning(sol):
    skriv("\n--- " + str(sol["sum"]) + " ---")
    for s in sol["steg"]:
        skriv("Steg " + str(s["id"]) + ": " + str(s["titel"]))
        if s.get("uttryck"):
            skriv(" " + str(s["uttryck"]))
        if s.get("ber"):
            skriv(" " + str(s["ber"]))
        if s.get("res") is not None:
            skriv(" Resultat: " + str(s["res"]))
    skriv("Slut: " + str(sol["slut"]))


# ---------- Funktioner ----------
def las_polynom_koeff():
    grad = las_int("Grad", 0)
    c = []
    p = grad
    while p >= 0:
        c.append(las_float("Koefficient for x^" + str(p)))
        p -= 1
    return c


def poly_varde(coeffs, x):
    y = 0.0
    for a in coeffs:
        y = y * x + a
    return y


def poly_derivata(coeffs):
    n = len(coeffs) - 1
    if n <= 0:
        return [0.0]
    out = []
    i = 0
    while i < n:
        out.append(coeffs[i] * (n - i))
        i += 1
    return out


# ---------- 1 Derivata/Tangent ----------
def derivera_polynom():
    coeffs = las_polynom_koeff()
    d = poly_derivata(coeffs)
    sol = ny_losning("Derivera polynom")
    lagg_till_steg(sol, "Anvand derivataregel", uttryck="(a_n*x^n)' = n*a_n*x^(n-1)", ber="f'(x)-koeff = " + str(d))
    satt_slut(sol, {"derivata_koeff": d})
    visa_losning(sol)


def tangent_i_punkt():
    coeffs = las_polynom_koeff()
    x0 = las_float("x0")
    d = poly_derivata(coeffs)
    m = poly_varde(d, x0)
    y0 = poly_varde(coeffs, x0)
    b = y0 - m * x0
    sol = ny_losning("Tangent i punkt")
    lagg_till_steg(sol, "Derivera", ber="d = " + str(d))
    lagg_till_steg(sol, "Berakna lutning", ber="m=f'(" + str(x0) + ")=" + str(m))
    lagg_till_steg(sol, "Berakna punkt", ber="y0=f(" + str(x0) + ")=" + str(y0))
    lagg_till_steg(sol, "Bygg tangent", uttryck="y = m*x + b", ber="b=" + str(b))
    satt_slut(sol, {"m": m, "b": b, "linje": "y=" + str(m) + "*x+" + str(b)})
    visa_losning(sol)


def meny_derivata_tangent():
    while True:
        skriv("\n1 Derivera funktion")
        skriv("2 Tangentekvation")
        skriv("3 Tangent i punkt")
        skriv("4 Visa derivatasteg")
        skriv("5 Tillbaka")
        v = las("Val: ").strip()
        if v == "1" or v == "4":
            derivera_polynom()
        elif v == "2" or v == "3":
            tangent_i_punkt()
        elif v == "5":
            return


# ---------- 2 Approximationer ----------
def linjar_approximation():
    coeffs = las_polynom_koeff()
    a = las_float("Approxpunkt a")
    x = las_float("Punkt x")
    fa = poly_varde(coeffs, a)
    fpa = poly_varde(poly_derivata(coeffs), a)
    lx = fa + fpa * (x - a)
    fx = poly_varde(coeffs, x)
    fel = abs(fx - lx)
    sol = ny_losning("Linjär approximation")
    lagg_till_steg(sol, "Formel", uttryck="L(x)=f(a)+f'(a)(x-a)")
    lagg_till_steg(sol, "Substitution", ber="f(a)=" + str(fa) + ", f'(a)=" + str(fpa))
    lagg_till_steg(sol, "Approximation", ber="L(" + str(x) + ")=" + str(lx))
    lagg_till_steg(sol, "Fel", ber="|f(x)-L(x)|=" + str(fel), res=fel)
    satt_slut(sol, {"Lx": lx, "fx": fx, "absolutfel": fel})
    visa_losning(sol)


def meny_approx():
    while True:
        skriv("\n1 Linjar approximation")
        skriv("2 Approximation i punkt")
        skriv("3 Approximationsfel")
        skriv("4 Tangent som approximation")
        skriv("5 Tillbaka")
        v = las("Val: ").strip()
        if v in ("1", "2", "3", "4"):
            linjar_approximation()
        elif v == "5":
            return


# ---------- 3 Maclaurin/Taylor ----------
def taylor_standard():
    skriv("Valj funktion: 1 sin(x), 2 cos(x), 3 e^x")
    f = las("Val: ").strip()
    x = las_float("x")
    n = las_int("Antal termer", 1)
    sol = ny_losning("Maclaurin/Taylor")
    if f == "1":
        # sin x = x - x^3/3! + x^5/5! ...
        s = 0.0
        k = 0
        fact = 1.0
        while k < n:
            p = 2 * k + 1
            if k == 0:
                fact = 1.0
            else:
                fact *= (p - 1) * p
            term = ((-1) ** k) * (x ** p) / fact
            s += term
            lagg_till_steg(sol, "Term " + str(k + 1), ber="+" + str(term))
            k += 1
        satt_slut(sol, {"approx": s, "funktion": "sin"})
    elif f == "2":
        s = 0.0
        k = 0
        fact = 1.0
        while k < n:
            p = 2 * k
            if k > 0:
                fact *= (p - 1) * p
            term = ((-1) ** k) * (x ** p) / fact
            s += term
            lagg_till_steg(sol, "Term " + str(k + 1), ber="+" + str(term))
            k += 1
        satt_slut(sol, {"approx": s, "funktion": "cos"})
    else:
        s = 1.0
        k = 1
        fact = 1.0
        lagg_till_steg(sol, "Term 1", ber="+1")
        while k < n:
            fact *= k
            term = (x ** k) / fact
            s += term
            lagg_till_steg(sol, "Term " + str(k + 1), ber="+" + str(term))
            k += 1
        satt_slut(sol, {"approx": s, "funktion": "exp"})
    visa_losning(sol)


def meny_taylor():
    while True:
        skriv("\n1 Skapa polynom")
        skriv("2 Approximation")
        skriv("3 Jamfor med exakt varde")
        skriv("4 Berakna fel")
        skriv("5 Serie for gransvarde")
        skriv("6 Tillbaka")
        v = las("Val: ").strip()
        if v in ("1", "2", "3", "4", "5"):
            taylor_standard()
        elif v == "6":
            return


# ---------- 4 Newton-Raphson ----------
def newton_raphson_polynom():
    coeffs = las_polynom_koeff()
    x = las_float("Startvarde x0")
    it = las_int("Antal iterationer", 1)
    d = poly_derivata(coeffs)
    sol = ny_losning("Newton-Raphson")
    i = 0
    while i < it:
        fx = poly_varde(coeffs, x)
        dfx = poly_varde(d, x)
        if dfx == 0:
            lagg_till_steg(sol, "Stopp", ber="f'(x)=0 vid x=" + str(x))
            break
        xn = x - fx / dfx
        lagg_till_steg(sol, "Iteration " + str(i), ber="x=" + str(x) + " -> " + str(xn))
        x = xn
        i += 1
    satt_slut(sol, {"rot": x})
    visa_losning(sol)


def meny_newton():
    while True:
        skriv("\n1 Los ekvation")
        skriv("2 Visa iterationer")
        skriv("3 Tva losningar")
        skriv("4 Analysera startvarde")
        skriv("5 Tillbaka")
        v = las("Val: ").strip()
        if v in ("1", "2", "3", "4"):
            newton_raphson_polynom()
        elif v == "5":
            return


# ---------- 5 Differentialekvationer ----------
def ode_kylningslag():
    T0 = las_float("Starttemp T0")
    Tomg = las_float("Omgivning Tomg")
    k = las_float("k")
    t = las_float("t")
    T = Tomg + (T0 - Tomg) * (2.718281828 ** (-k * t))
    sol = ny_losning("Newtons kylningslag")
    lagg_till_steg(sol, "Modell", uttryck="T'=-k(T-Tomg)")
    lagg_till_steg(sol, "Losning", uttryck="T(t)=Tomg+(T0-Tomg)e^(-kt)")
    lagg_till_steg(sol, "Substitution", ber="T(" + str(t) + ")=" + str(T), res=T)
    satt_slut(sol, {"T": T})
    visa_losning(sol)


def meny_ode():
    while True:
        skriv("\n1 Separabla differentialekvationer")
        skriv("2 Integrerande faktor")
        skriv("3 Begynnelsevarden")
        skriv("4 Klassificering")
        skriv("5 Tillämpningar")
        skriv("6 Tillbaka")
        v = las("Val: ").strip()
        if v == "5":
            ode_kylningslag()
        elif v in ("1", "2", "3", "4"):
            skriv("Denna undermeny ar planerad, valj 5 for aktiv demo.")
        elif v == "6":
            return


# ---------- 6 Installningar ----------
APP = {"dec": 6}


def meny_installningar():
    while True:
        skriv("\n1 Decimaler")
        skriv("2 Visa nuvarande")
        skriv("3 Tillbaka")
        v = las("Val: ").strip()
        if v == "1":
            APP["dec"] = las_int("Antal decimaler", 0)
        elif v == "2":
            skriv("Decimaler: " + str(APP["dec"]))
        elif v == "3":
            return


# ---------- Huvudmeny ----------
def huvudmeny():
    while True:
        skriv("\n=== Matteexpertsystem TI-84 ===")
        skriv("1 Derivata/Tangent")
        skriv("2 Approximationer")
        skriv("3 Maclaurin/Taylor")
        skriv("4 Newton-Raphson")
        skriv("5 Differentialekvationer")
        skriv("6 Installningar")
        skriv("7 Avsluta")
        v = las("Val: ").strip()
        if v == "1":
            meny_derivata_tangent()
        elif v == "2":
            meny_approx()
        elif v == "3":
            meny_taylor()
        elif v == "4":
            meny_newton()
        elif v == "5":
            meny_ode()
        elif v == "6":
            meny_installningar()
        elif v == "7":
            skriv("Avslutar")
            return


def main():
    skriv("Startar program...")
    huvudmeny()


try:
    main()
except Exception as e:
    skriv("FEL: " + str(e))
    try:
        las("Enter")
    except Exception:
        pass
