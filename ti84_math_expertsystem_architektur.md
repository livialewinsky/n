# TI-84 Plus CE-T Python Edition: Arkitektur för menybaserat matte-expertsystem

## 1) Övergripande systemarkitektur

Målet är ett **metodbaserat expertsystem** utan fri texttolkning av matematik. All input sker via menyer och numeriska formulär.

### Designprinciper för TI-84
- Ingen parser för fria uttryck.
- Små, tydliga moduler (snabba att ladda och enklare att felsöka).
- Numerisk input i sekvens (en parameter per fråga).
- Gemensam stegmotor för pedagogisk visning.
- Återanvändbar intern funktionsrepresentation.
- Hårdkodade metoder där symbolik annars blir för tung.

### Föreslagen modulindelning (filer)

- `main.py`  
  Startpunkt, huvudloop och routing mellan menyer.

- `ui_menu.py`  
  Menyrendering, valhantering, tillbaka-logik.

- `ui_forms.py`  
  Formulär för numerisk inmatning: grad, koefficienter, x-värde, startvärde, tolerans osv.

- `state.py`  
  Enkel app-state (nuvarande meny, senaste resultat, inställningar).

- `models.py`  
  Datastrukturer för funktioner, parametrar, lösningssteg.

- `step_engine.py`  
  Lagrar/formatterar/visar steg-för-steg-lösningar.

- `math_poly.py`  
  Polynom-verktyg (värde, derivata-koefficienter, tangentlinje).

- `math_stdfunc.py`  
  Standardfunktioner (sin, cos, exp, log, rot, rationella standardfall).

- `engine_derivative.py`  
  Derivata/tangent-logik via intern representation.

- `engine_approx.py`  
  Linjär approximation och felanalys.

- `engine_taylor.py`  
  Maclaurin/Taylor med hårdkodade serier.

- `engine_newton.py`  
  Newton-Raphson-iterationer och tabellvisning.

- `engine_ode.py`  
  Differentialekvationer: separabla, integrerande faktor, tillämpningsmallar.

- `content_templates.py`  
  Textmallar för formler, stegbeskrivningar och pedagogisk output.

- `settings.py`  
  Precision, max iterationer, visningshastighet, detaljnivå.

## 2) Datastrukturer

Använd lätta dict-baserade strukturer (snålare än komplexa klasshierarkier på TI-84).

### 2.1 Funktionsobjekt (intern representation)

```python
# Exempel: polynom 2x^3 - 5x + 1
func = {
    "family": "poly",           # poly, trig, exp, log, root, rational_std
    "params": {
        "coeffs": [2, 0, -5, 1], # högst grad först
        "var": "x"
    },
    "meta": {
        "label": "f(x)",
        "domain_hint": "R"
    }
}
```

```python
# Exempel: trig a*sin(bx + c) + d
func = {
    "family": "trig",
    "params": {
        "kind": "sin",   # sin/cos
        "a": 1.0,
        "b": 2.0,
        "c": 0.0,
        "d": 0.0
    }
}
```

### 2.2 Problemdefinition

```python
problem = {
    "topic": "newton",          # derivative/approx/taylor/newton/ode
    "subtopic": "solve_one_root",
    "function": func,
    "inputs": {
        "x0": 1.5,
        "iterations": 6,
        "tol": 1e-5
    }
}
```

### 2.3 Lösningssteg

```python
step = {
    "id": 3,
    "title": "Beräkna derivata i x0",
    "expr": "f'(x0) = 3x0^2 - 5",
    "subs": "x0 = 1.5",
    "calc": "f'(1.5) = 1.75",
    "result": 1.75,
    "level": 1
}
```

Alla steg samlas i:

```python
solution = {
    "summary": "Rot approximerad med Newton-Raphson",
    "steps": [step1, step2, ...],
    "final": {"x": 1.70998, "residual": 0.00001}
}
```

## 3) Moduldesign per huvudområde

### 3.1 Derivata/Tangent

Ansvar:
- Bygga funktion via formulär.
- Derivera enligt vald familj.
- Beräkna tangent i punkt.
- Visa regel + substitution + resultat.

Exempel-API:
```python
def derive_function(func):
    # returnerar nytt func-objekt för f'(x)
    ...

def tangent_line(func, x0):
    # returnerar m, b samt steg
    ...
```

### 3.2 Approximationer

Ansvar:
- Linjär approximation: `L(x)=f(a)+f'(a)(x-a)`.
- Approximation i punkt `x`.
- Absolut/relativt fel mot exakt värde.
- Tangent som tolkning av approximation.

### 3.3 Maclaurin/Taylor

Ansvar:
- Välj standardfunktion ur meny.
- Generera truncerad serie till ordning `n`.
- Värdera serien i punkt.
- Jämför mot exakt värde (när tillgängligt).

Strategi:
- Hårdkodade koefficientregler för:
  - `sin(x)`, `cos(x)`, `e^x`, `ln(1+x)`, `1/(1+x)`, `sqrt(1+x)`.

### 3.4 Newton-Raphson

Ansvar:
- Välj funktionstyp + parametrar.
- Kör iterationer:
  `x_{k+1} = x_k - f(x_k)/f'(x_k)`.
- Visa tabellrad per iteration.
- Stoppa på max iteration eller tolerans.
- Varning om `f'(x_k)=0`.

### 3.5 Differentialekvationer

Ansvar:
- Klassificera via meny (separabel, linjär 1:a ordningen, tillämpningsmall).
- Samla nödvändiga parametrar.
- Lös via mallad metod, inte generell CAS.
- Tillämpa begynnelsevillkor.

Exempel delproblem:
- Newtons kylningslag: `T'=-k(T-T_omg)`.
- Läckande tank (förenklad modell).
- Enkel reaktionskinetik.

## 4) Menylogik och beslutsträd

## 4.1 Huvudmeny
1. Derivata/Tangent
2. Approximationer
3. Maclaurin/Taylor
4. Newton-Raphson
5. Differentialekvationer
6. Inställningar
7. Om/Minne

## 4.2 Beslutsträdsmönster (generiskt)

1. Välj metodområde.
2. Välj delmetod.
3. Välj funktionstyp/modell.
4. Formulär: samla parametrar en och en.
5. Validera intervall/domän.
6. Kör mattemotor.
7. Visa steg (bläddringsbart).
8. Visa slutsvar + nästa val:
   - ny punkt,
   - ändra parameter,
   - tillbaka till undermeny.

## 4.3 Exempel: Newton-träd

- Newton-Raphson
  - Lös ekvation
    - Funktionstyp?
      - Polynom
      - Trig
      - Exp/log
    - Samla parametrar
    - Startvärde `x0`
    - Iterationer / tolerans
    - Kör
    - Visa iterationstabell
    - Spara senaste rot

## 5) Intern funktionsrepresentation

Målet är att kunna använda samma pipeline i flera motorer:
- `eval_func(func, x)`
- `derive_func(func)`
- `pretty_func(func)`

### 5.1 Minimal dispatcher

```python
def eval_func(func, x):
    fam = func["family"]
    p = func["params"]
    if fam == "poly":
        return eval_poly(p["coeffs"], x)
    if fam == "trig":
        return eval_trig(p, x)
    if fam == "exp":
        return eval_exp(p, x)
    if fam == "log":
        return eval_log(p, x)
    if fam == "root":
        return eval_root(p, x)
    raise ValueError("Okänd funktionsfamilj")
```

### 5.2 Varför detta fungerar på TI-84
- Ingen tung parser.
- Snabba if/elif-grenar.
- Enkel serialisering/sparning i listor/dicts.
- Samma struktur för alla moduler.

## 6) Stegmotor (pedagogik + prestanda)

Stegmotorn ska vara frikopplad från själva beräkningen.
Motorerna returnerar både svar och en lista av strukturerade steg.

### 6.1 API-idé

```python
def new_solution(summary):
    return {"summary": summary, "steps": [], "final": None}

def add_step(sol, title, expr="", subs="", calc="", result=None, level=1):
    sol["steps"].append({
        "id": len(sol["steps"]) + 1,
        "title": title,
        "expr": expr,
        "subs": subs,
        "calc": calc,
        "result": result,
        "level": level,
    })

def set_final(sol, final_dict):
    sol["final"] = final_dict
```

### 6.2 Visningsläge på TI-84
- Ett steg per skärm.
- `LEFT/RIGHT` för föregående/nästa.
- `MODE` för att växla detaljnivå (kort/lång).
- Kort stränglängd (radbryt manuellt).

### 6.3 Minnesstrategi (3 MB + arkivminne)
- Förkorta nycklar i produktion (`"family" -> "f"`, etc.) om nödvändigt.
- Lagra endast senaste fulla lösning i RAM.
- Arkivera mallar/konstanter i separat modul (statisk data).
- Rensa steglistor vid menybyte om användaren inte valt “spara”.
- Återanvänd listor för iterationstabeller istället för att skapa många temporärer.

## 7) Praktisk mappning: metodbaserat istället för uppgiftsbaserat

Varje huvudmodul jobbar med:
1. **Identifiera metod** via meny.
2. **Samla minimala parametrar** via formulär.
3. **Bygga intern modell** (`func` + `inputs`).
4. **Köra generell metodmotor**.
5. **Visa steg och slutsvar**.

Detta gör att samma kod löser många uppgifter utan fri textinmatning.

## 8) Rekommenderad utvecklingsordning

1. Bygg `ui_menu.py` + `ui_forms.py` + `step_engine.py`.
2. Implementera polynom fullt ut (derivata, tangent, Newton).
3. Lägg till trig/exp/log som separata funktionsfamiljer.
4. Lägg till Taylor-standardfunktioner.
5. Lägg till ODE-mallar en i taget.
6. Optimera minne och stränglängder sist.

## 9) Minimal första leverans (MVP)

- Huvudmeny + navigering.
- Derivata/Tangent för polynom.
- Newton-Raphson för polynom.
- Linjär approximation för polynom.
- Stegvis visning med bläddring.
- Inställning för decimalprecision.

När MVP är stabil utökas med fler funktionsfamiljer och ODE-tillämpningar.
