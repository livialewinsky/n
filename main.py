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

def multi(v=0):
 if not v:v=int(input("Steg: "))
 if v<=0:return print("Fel.")
 p=1;a=[]
 for i in range(1,v+1):
  x=int(input("Val "+str(i)+": "))
  if x<0:return print("Fel.")
  p*=x;a.append(str(x))
 print("Lösning:"," * ".join(a),"=",p)

def dir():
 while 1:
  print("\nDirektval")
  print("1.P(n,k) 2.C(n,k) 3.n! 4.n^k 5.*-steg 6.Sum C 7.Tillbaka")
  v=input("Val 1-7: ").strip()
  if v=="1":
   n=int(input("n: "));k=int(input("k: "))
   r=nPr(n,k)
   if r is None:print("Fel.")
   else:print("nPr:",str(n)+"! / "+str(n-k)+"! =",r)
  elif v=="2":
   n=int(input("n: "));k=int(input("k: "))
   r=nCr(n,k)
   if r is None:print("Fel.")
   else:print("nCr:",str(n)+"! / ("+str(k)+"! * "+str(n-k)+"!) =",r)
  elif v=="3":
   n=int(input("n: "))
   r=fac(n)
   if r is None:print("Fel.")
   else:print("n!=",n,"!=",r)
  elif v=="4":
   n=int(input("n: "));k=int(input("k: "))
   if n<0 or k<0:print("Fel.")
   else:print("Lösning:",str(n)+"^"+str(k),"=",n**k)
  elif v=="5":multi()
  elif v=="6":
   n=int(input("n: "));a=int(input("från k: "));b=int(input("till k: "))
   if n<0 or a<0 or b<a or b>n:print("Fel.")
   else:
    s=0
    for k in range(a,b+1):s+=nCr(n,k)
    print("Sum C=",s)
  elif v=="7":return
  else:print("Ogiltigt val.")

def h():
 print("Tips 1=ja,2=nej")
 print("ordning: kod/kö->1, val av lag->2")
 print("alla: alla objekt används->1")
 print("upprepning: samma kan väljas igen->1")
 print("identiska: lika tecken/personer->1")

def kombinatorik():
 print("\n--- Kombinatorik ---")
 if j("Direkt formel? (t.ex. P(9,2)/C(7,3))"):
  dir();return
 if j("Är det val i flera olika steg? (t.ex. tårta/kläder/meny)"):
  multi();return
 h()
 o=j("Viktig ordning? (t.ex. kod/plats/kö, annars 2)")
 a=j("Ska ALLA användas? (t.ex. kasta om bokstäver, annars 2)")
 u=j("Upprepning? (t.ex. 1-1-1/tärning, annars 2)")
 i=j('Finns identiska objekt? (t.ex. bokstäver i "mamma", annars 2)')
 if i and a:
  n=int(input("n: "));g=int(input("Grupper: "))
  if n<0 or g<=0:return print("Fel.")
  s=0;d=1;t=[]
  for x in range(1,g+1):
   v=int(input("g"+str(x)+": "))
   if v<0:return print("Fel.")
   s+=v;d*=fac(v);t.append(str(v)+"!")
  if s!=n:return print("Fel: summa!=n")
  print(str(n)+"!/("," * ".join(t),") =",fac(n)//d);return
 if o:
  if a and not u:
   n=int(input("n: "))
   if n<0:return print("Fel.")
   return print("n!=",n,"!=",fac(n))
  if u:
   n=int(input("n: "));k=int(input("k: "))
   if n<0 or k<0:return print("Fel.")
   return print("Lösning:",str(n)+"^"+str(k),"=",n**k)
  n=int(input("n: "));k=int(input("k: "))
  r=nPr(n,k)
  if r is None:return print("Fel.")
  return print("nPr:",str(n)+"! / "+str(n-k)+"! =",r)
 if u:
  n=int(input("n: "));k=int(input("k: "))
  if n<=0 or k<0:return print("Fel.")
  N=n+k-1
  return print("nCr:",str(N)+"! / ("+str(k)+"! * "+str(N-k)+"!) =",nCr(N,k))
 n=int(input("n: "));k=int(input("k: "))
 r=nCr(n,k)
 if r is None:return print("Fel.")
 print("nCr:",str(n)+"! / ("+str(k)+"! * "+str(n-k)+"!) =",r)

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
