# Matematiskt expertsystem för kombinatorik och närliggande områden
# Anpassat för TI-84 Plus CE-T Python Edition


def ja_nej(fraga):
    while True:
        svar = input(fraga + " (ja/nej): ").strip().lower()
        if svar == "ja":
            return True
        if svar == "nej":
            return False
        print("Skriv 'ja' eller 'nej'.")


def factorial(n):
    if n < 0:
        return None
    resultat = 1
    i = 2
    while i <= n:
        resultat *= i
        i += 1
    return resultat


def nCr(n, k):
    if n < 0 or k < 0 or k > n:
        return None
    # Symmetri för färre multiplikationer
    if k > n - k:
        k = n - k
    taljare = 1
    namnare = 1
    i = 1
    while i <= k:
        taljare *= (n - k + i)
        namnare *= i
        i += 1
    return taljare // namnare


def kombinatorik():
    print("\n--- Kombinatorik: automatisk formelidentifiering ---")
    arrangemang = ja_nej("Är det ett räkneproblem om arrangemang (snarare än val)")
    ordning = ja_nej("Spelar ordningen roll")
    alla_objekt = ja_nej("Används alla objekt")
    identiska = ja_nej("Finns identiska objekt")
    upprepning = ja_nej("Är upprepning tillåten")

    print("\nIdentifierad modell:")

    if alla_objekt and identiska:
        print("Permutation med identiska objekt")
        n = int(input("Ange totalt antal objekt n: "))
        antal_grupper = int(input("Ange antal grupper av identiska objekt: "))

        if n < 0 or antal_grupper <= 0:
            print("Fel: ogiltiga värden.")
            return

        summa = 0
        namnare = 1
        i = 1
        while i <= antal_grupper:
            ni = int(input("Ange storlek för grupp " + str(i) + ": "))
            if ni < 0:
                print("Fel: gruppstorlek kan inte vara negativ.")
                return
            summa += ni
            f = factorial(ni)
            namnare *= f
            i += 1

        if summa != n:
            print("Fel: summan av gruppstorlekarna måste vara n.")
            return

        svar = factorial(n) // namnare
        print("Svar = n!/(n1!*n2!*...) =", svar)
        return

    if ordning:
        if alla_objekt and not upprepning:
            print("Permutation (alla objekt används)")
            n = int(input("Ange n: "))
            if n < 0:
                print("Fel: n måste vara >= 0.")
                return
            svar = factorial(n)
            print("Svar = n! =", svar)
            return

        if upprepning:
            print("Permutation med upprepning")
            n = int(input("Ange antal valbara objekt n: "))
            k = int(input("Ange antal positioner/val k: "))
            if n < 0 or k < 0:
                print("Fel: n och k måste vara >= 0.")
                return
            svar = n ** k
            print("Svar = n^k =", svar)
            return

        print("Permutation (k av n, utan upprepning)")
        n = int(input("Ange n: "))
        k = int(input("Ange k: "))
        if n < 0 or k < 0 or k > n:
            print("Fel: kräver 0 <= k <= n.")
            return
        svar = factorial(n) // factorial(n - k)
        print("Svar = n!/(n-k)! =", svar)
        return

    else:
        if upprepning:
            print("Kombination med upprepning")
            n = int(input("Ange n: "))
            k = int(input("Ange k: "))
            if n <= 0 or k < 0:
                print("Fel: kräver n > 0 och k >= 0.")
                return
            svar = nCr(n + k - 1, k)
            print("Svar = (n+k-1)Ck =", svar)
            return

        print("Kombination utan upprepning")
        n = int(input("Ange n: "))
        k = int(input("Ange k: "))
        svar = nCr(n, k)
        if svar is None:
            print("Fel: kräver 0 <= k <= n.")
            return
        print("Svar = nCk =", svar)
        return

    # Om frågorna skulle ge en ovanlig kombination
    if arrangemang:
        print("Ingen standardformel kunde avgöras med givna svar.")
    else:
        print("Ingen standardformel kunde avgöras med givna svar.")


def binomial():
    print("\n--- Binomialsatsen ---")
    print("1. Utveckla hela (a+b)^n")
    print("2. Beräkna en specifik term")
    print("3. Beräkna endast binomialkoefficienten nCk")

    val = input("Välj 1-3: ").strip()

    if val == "1":
        a = int(input("Ange a: "))
        b = int(input("Ange b: "))
        n = int(input("Ange n: "))
        if n < 0:
            print("Fel: n måste vara >= 0.")
            return

        print("Termer i utvecklingen av (a+b)^n:")
        k = 0
        while k <= n:
            koeff = nCr(n, k)
            term = koeff * (a ** (n - k)) * (b ** k)
            print("k=", k, ":", koeff, "*", a, "^", (n - k), "*", b, "^", k, "=", term)
            k += 1
        return

    if val == "2":
        a = int(input("Ange a: "))
        b = int(input("Ange b: "))
        n = int(input("Ange n: "))
        k = int(input("Ange k för termen: "))
        koeff = nCr(n, k)
        if koeff is None:
            print("Fel: kräver 0 <= k <= n och n >= 0.")
            return
        term = koeff * (a ** (n - k)) * (b ** k)
        print("Specifik term = nCk * a^(n-k) * b^k =", term)
        return

    if val == "3":
        n = int(input("Ange n: "))
        k = int(input("Ange k: "))
        svar = nCr(n, k)
        if svar is None:
            print("Fel: kräver 0 <= k <= n och n >= 0.")
            return
        print("Binomialkoefficient nCk =", svar)
        return

    print("Ogiltigt val.")


def ladprincip():
    print("\n--- Lådprincipen ---")
    n = int(input("Hur många objekt? "))
    k = int(input("Hur många lådor? "))

    if n < 0 or k <= 0:
        print("Fel: objekt >= 0 och lådor > 0 krävs.")
        return

    # ceil(n/k) utan math-modul
    svar = (n + k - 1) // k
    print("Minsta antal objekt i minst en låda =", svar)


def mangdlara():
    print("\n--- Mängdlära ---")
    print("1. Union av två mängder")
    print("2. Union av tre mängder")
    print("3. Antal delmängder")
    print("4. Antal äkta delmängder")
    print("5. Antal k-delmängder")
    print("6. Kartesisk produkt")

    val = input("Välj 1-6: ").strip()

    if val == "1":
        a = int(input("Ange |A|: "))
        b = int(input("Ange |B|: "))
        ab = int(input("Ange |A ∩ B|: "))
        svar = a + b - ab
        print("|A ∪ B| =", svar)
        return

    if val == "2":
        a = int(input("Ange |A|: "))
        b = int(input("Ange |B|: "))
        c = int(input("Ange |C|: "))
        ab = int(input("Ange |A ∩ B|: "))
        ac = int(input("Ange |A ∩ C|: "))
        bc = int(input("Ange |B ∩ C|: "))
        abc = int(input("Ange |A ∩ B ∩ C|: "))
        svar = a + b + c - ab - ac - bc + abc
        print("|A ∪ B ∪ C| =", svar)
        return

    if val == "3":
        n = int(input("Ange n (antal element): "))
        if n < 0:
            print("Fel: n måste vara >= 0.")
            return
        print("Antal delmängder = 2^n =", 2 ** n)
        return

    if val == "4":
        n = int(input("Ange n (antal element): "))
        if n < 0:
            print("Fel: n måste vara >= 0.")
            return
        print("Antal äkta delmängder = 2^n - 1 =", (2 ** n) - 1)
        return

    if val == "5":
        n = int(input("Ange n: "))
        k = int(input("Ange k: "))
        svar = nCr(n, k)
        if svar is None:
            print("Fel: kräver 0 <= k <= n och n >= 0.")
            return
        print("Antal k-delmängder = nCk =", svar)
        return

    if val == "6":
        a = int(input("Ange |A|: "))
        b = int(input("Ange |B|: "))
        print("|A × B| =", a * b)
        return

    print("Ogiltigt val.")


def huvudmeny():
    while True:
        print("\n=== Matematiskt expertsystem ===")
        print("1. Kombinatorik (automatisk formelidentifiering)")
        print("2. Binomialsatsen")
        print("3. Lådprincipen")
        print("4. Mängdlära")
        print("5. Avsluta")

        val = input("Välj 1-5: ").strip()

        if val == "1":
            kombinatorik()
        elif val == "2":
            binomial()
        elif val == "3":
            ladprincip()
        elif val == "4":
            mangdlara()
        elif val == "5":
            print("Avslutar programmet.")
            break
        else:
            print("Ogiltigt val, försök igen.")


huvudmeny()
