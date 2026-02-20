def j(f):
 while 1:
  s=input(f+" (1=ja, 2=nej): ").strip()
  if s=="1":return 1
  if s=="2":return 0
  print("Skriv 1 eller 2.")

def fac(n):
 if n<0:return None
 r=1
 for i in range(2,n+1):r*=i
 return r

def nCr(n,k):
 if n<0 or k<0 or k>n:return None
 if k>n-k:k=n-k
 t=d=1
 for i in range(1,k+1):t*=n-k+i;d*=i
 return t//d

def nPr(n,k):
 if n<0 or k<0 or k>n:return None
 return fac(n)//fac(n-k)

def multi():
 m=int(input("Steg: "))
 if m<=0:return print("Fel.")
 p=1;a=[]
 for i in range(1,m+1):
  x=int(input("Val "+str(i)+": "))
  if x<0:return print("Fel.")
  p*=x;a.append(str(x))
 print("Lösning:"," * ".join(a),"=",p)

def kombinatorik():
 print("\n--- Kombinatorik ---")
 if j("Är det val i flera steg? (t.ex. först bröd, sen fyllning)"):
  return multi()
 if j("Är det en Prispall/Kö? (dvs. skillnad på 1:a, 2:a, 3:a)"):
  n=int(input("n: "));k=int(input("k: "))
  r=nPr(n,k)
  if r is None:return print("Fel.")
  return print("nPr:",str(n)+"! / "+str(n-k)+"! =",r)
 if j("Är det ett Kombinationslås? (dvs. ordning spelar roll OCH man får ha samma siffra igen)"):
  n=int(input("n: "));k=int(input("k: "))
  if n<0 or k<0:return print("Fel.")
  return print("Lösning:",str(n)+"^"+str(k),"=",n**k)
 if j("Är det en Kommitté/Lag? (dvs. bara en grupp där ordning INTE spelar roll)"):
  n=int(input("n: "));k=int(input("k: "))
  r=nCr(n,k)
  if r is None:return print("Fel.")
  return print("nCr:",str(n)+"! / ("+str(k)+"! * "+str(n-k)+"!) =",r)
 if j("Ska du välja från två grupper? (t.ex. 2 killar OCH 3 tjejer)"):
  print("Grupp 1")
  n1=int(input("n1: "));k1=int(input("k1: "))
  r1=nCr(n1,k1)
  if r1 is None:return print("Fel.")
  print("Grupp 2")
  n2=int(input("n2: "));k2=int(input("k2: "))
  r2=nCr(n2,k2)
  if r2 is None:return print("Fel.")
  print("nCr1:",str(n1)+"! / ("+str(k1)+"! * "+str(n1-k1)+"!) =",r1)
  print("nCr2:",str(n2)+"! / ("+str(k2)+"! * "+str(n2-k2)+"!) =",r2)
  return print("Lösning:",r1,"*",r2,"=",r1*r2)
 if j('Står det "Minst en" i frågan?'):
  print('Tips: Räkna ut: Totala sätt - Sättet där ingen väljs')
  return
 print("Ingen träff. Välj formel manuellt (nPr/nCr/n^k).")

def meny():
 while 1:
  print("\n=== Matematiskt expertsystem ===")
  print("1. Kombinatorik")
  print("2. Avsluta")
  v=input("Välj 1-2: ").strip()
  if v=="1":kombinatorik()
  elif v=="2":print("Avslutar programmet.");break
  else:print("Ogiltigt val.")

meny()
