**S:**

![S](imagenes/S.png)

```
S        ::= FN* empty
```

**FN:**

![FN](imagenes/FN.png)

```
FN       ::= TR id '(' P ')' FNp
```

referenced by:

* S

**TR:**

![TR](imagenes/TR.png)

```
TR       ::= 'void'
           | T
```

referenced by:

* FN

**P:**

![P](imagenes/P.png)

```
P        ::= ( T id ( ',' T id )* )? empty
```

referenced by:

* FN

**FNp:**

![FNp](imagenes/FNp.png)

```
FNp      ::= ';'
           | '{' Bp '}'
```

referenced by:

* FN

**Bp:**

![Bp](imagenes/Bp.png)

```
Bp       ::= B* empty
```

referenced by:

* CA
* DT
* ELSEP
* FNp
* I
* WH

**B:**

![B](imagenes/B.png)

```
B        ::= D
           | ID
           | R
           | I
           | WH
           | SW
```

referenced by:

* Bp

**D:**

![D](imagenes/D.png)

```
D        ::= T V ';'
```

referenced by:

* B

**T:**

![T](imagenes/T.png)

```
T        ::= int
           | char
           | float
```

referenced by:

* D
* P
* TR

**V:**

![V](imagenes/V.png)

```
V        ::= id Ap ( ',' id Ap )* empty
```

referenced by:

* D

**Ap:**

![Ap](imagenes/Ap.png)

```
Ap       ::= '=' E
           | empty
```

referenced by:

* V

**ID:**

![ID](imagenes/ID.png)

```
ID       ::= id IDp
```

referenced by:

* B

**IDp:**

![IDp](imagenes/IDp.png)

```
IDp      ::= A
           | C ';'
```

referenced by:

* ID

**A:**

![A](imagenes/A.png)

```
A        ::= '=' E ';'
```

referenced by:

* IDp

**E:**

![E](imagenes/E.png)

```
E        ::= TE ( ( '+' | '-' ) TE )* empty
```

referenced by:

* A
* APL
* Ap
* CA
* F
* L
* Rp
* SW

**TE:**

![TE](imagenes/TE.png)

```
TE       ::= F ( ( '*' | '/' ) F )* empty
```

referenced by:

* E

**F:**

![F](imagenes/F.png)

```
F        ::= '(' E ')'
           | 'id' FP
           | 'numero'
           | 'char'
```

referenced by:

* TE

**FP:**

![FP](imagenes/FP.png)

```
FP       ::= empty
           | C
```

referenced by:

* F

**C:**

![C](imagenes/C.png)

```
C        ::= '(' APL ')'
```

referenced by:

* FP
* IDp

**APL:**

![APL](imagenes/APL.png)

```
APL      ::= ( E ( ',' E )* )? empty
```

referenced by:

* C

**L:**

![L](imagenes/L.png)

```
L        ::= E OP E
```

referenced by:

* ELSEP
* I
* WH

**OP:**

![OP](imagenes/OP.png)

```
OP       ::= '=='
           | '>'
           | '<'
```

referenced by:

* L

**R:**

![R](imagenes/R.png)

```
R        ::= 'return' Rp ';'
```

referenced by:

* B

**Rp:**

![Rp](imagenes/Rp.png)

```
Rp       ::= E
           | empty
```

referenced by:

* R

**I:**

![I](imagenes/I.png)

```
I        ::= 'if' '(' L ')' '{' Bp '}' Ip
```

referenced by:

* B

**Ip:**

![Ip](imagenes/Ip.png)

```
Ip       ::= ELSE
           | empty
```

referenced by:

* ELSEP
* I

**ELSE:**

![ELSE](imagenes/ELSE.png)

```
ELSE     ::= 'else' ELSEp
```

referenced by:

* Ip

**ELSEP:**

![ELSEP](imagenes/ELSEP.png)

```
ELSEP    ::= 'if' '(' L ')' '{' Bp '}' Ip
           | '{' Bp '}'
```

**WH:**

![WH](imagenes/WH.png)

```
WH       ::= 'while' '(' L ')' '{' Bp '}'
```

referenced by:

* B

**SW:**

![SW](imagenes/SW.png)

```
SW       ::= 'switch' '(' E ')' '{' CS '}'
```

referenced by:

* B

**CS:**

![CS](imagenes/CS.png)

```
CS       ::= CA_LIST CA_LISTp
           | DT
```

referenced by:

* SW

**CA_LISTp:**

![CA_LISTp](imagenes/CA_LISTp.png)

```
CA_LISTp ::= DT
           | empty
```

referenced by:

* CS

**CA_LIST:**

![CA_LIST](imagenes/CA_LIST.png)

```
CA_LIST  ::= CA CAp
```

referenced by:

* CAp
* CS

**CAp:**

![CAp](imagenes/CAp.png)

```
CAp      ::= CA_LIST
           | empty
```

referenced by:

* CA_LIST

**CA:**

![CA](imagenes/CA.png)

```
CA       ::= 'case' E ':' Bp BK
```

referenced by:

* CA_LIST

**DT:**

![DT](imagenes/DT.png)

```
DT       ::= 'default' ':' Bp BK
```

referenced by:

* CA_LISTp
* CS

## 
![BK](imagenes/BK.png)