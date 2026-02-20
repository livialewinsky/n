# Matematiskt expertsystem för kombinatorik
# Anpassat för TI-84 Plus CE-T Python Edition


def ja_nej(fraga):
    while True:
        svar = input(fraga + " (1=ja, 2=nej): ").strip()
        if svar == "1":
            return True
        if svar == "2":
            return False
        print("Skriv 1 för ja eller 2 för nej.")


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
    ja_nej("Är det ett räkneproblem om arrangemang eller val")
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
            namnare *= factorial(ni)
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
            print("Svar = n! =", factorial(n))
            return

        if upprepning:
            print("Permutation med upprepning")
            n = int(input("Ange antal valbara objekt n: "))
            k = int(input("Ange antal positioner/val k: "))
            if n < 0 or k < 0:
                print("Fel: n och k måste vara >= 0.")
                return
            print("Svar = n^k =", n ** k)
            return

        print("Permutation (k av n, utan upprepning)")
        n = int(input("Ange n: "))
        k = int(input("Ange k: "))
        if n < 0 or k < 0 or k > n:
            print("Fel: kräver 0 <= k <= n.")
            return
        print("Svar = n!/(n-k)! =", factorial(n) // factorial(n - k))
        return

    if upprepning:
        print("Kombination med upprepning")
        n = int(input("Ange n: "))
        k = int(input("Ange k: "))
        if n <= 0 or k < 0:
            print("Fel: kräver n > 0 och k >= 0.")
            return
        print("Svar = (n+k-1)Ck =", nCr(n + k - 1, k))
        return

    print("Kombination utan upprepning")
    n = int(input("Ange n: "))
    k = int(input("Ange k: "))
    svar = nCr(n, k)
    if svar is None:
        print("Fel: kräver 0 <= k <= n.")
        return
    print("Svar = nCk =", svar)


def huvudmeny():
    while True:
        print("\n=== Matematiskt expertsystem ===")
        print("1. Kombinatorik (automatisk formelidentifiering)")
        print("2. Avsluta")

        val = input("Välj 1-2: ").strip()

        if val == "1":
            kombinatorik()
        elif val == "2":
            print("Avslutar programmet.")
            break
        else:
            print("Ogiltigt val, försök igen.")


huvudmeny()
