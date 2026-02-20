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
 t=nmr=1
 for i in range(1,k+1):
  t*=n-k+i;nmr*=i
 return t//nmr

def komb():
 print("\n--- Kombinatorik ---")
 o=j("Viktig ordning? (t.ex. kod/plats/kö)")
 a=j("Ska ALLA användas? (t.ex. kasta om alla bokstäver)")
 u=j("Upprepning tillåten? (t.ex. 1-1-1/tärning)")
 i=j("Finns identiska objekt? (t.ex. bokstäver i \"mamma\")")
 print("\nIdentifierad modell:")
 if i and a:
  n=int(input("n: "));g=int(input("Antal grupper: "))
  if n<0 or g<=0:return print("Fel.")
  s=d=0;d=1
  for x in range(1,g+1):
   v=int(input("Grupp "+str(x)+": "))
   if v<0:return print("Fel.")
   s+=v;d*=fac(v)
  if s!=n:return print("Fel: summan måste vara n.")
  return print("Svar =",fac(n)//d)
 if o:
  if a and not u:
   n=int(input("n: "))
   if n<0:return print("Fel.")
   return print("n! =",fac(n))
  if u:
   n=int(input("n: "));k=int(input("k: "))
   if n<0 or k<0:return print("Fel.")
   return print("n^k =",n**k)
  n=int(input("n: "));k=int(input("k: "))
  if n<0 or k<0 or k>n:return print("Fel.")
  return print("nPr =",fac(n)//fac(n-k))
 if u:
  n=int(input("n: "));k=int(input("k: "))
  if n<=0 or k<0:return print("Fel.")
  return print("(n+k-1)Ck =",nCr(n+k-1,k))
 n=int(input("n: "));k=int(input("k: "))
 r=nCr(n,k)
 if r is None:return print("Fel.")
 print("nCr =",r)

def meny():
 while 1:
  print("\n=== Matematiskt expertsystem ===")
  print("1. Kombinatorik")
  print("2. Avsluta")
  v=input("Välj 1-2: ").strip()
  if v=="1":komb()
  elif v=="2":
   print("Avslutar programmet.")
   break
  else:print("Ogiltigt val.")

meny()
