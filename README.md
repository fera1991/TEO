
# Grupo 8 - Estudiantes

- **Jonathan Ariel Cabrera Galdamez** - 00003120
- **Fernando José Galdamez Mendoza** - 00120520
- **Kevin Bryan Hernández López** - 00057720
- **Manuel Alejandro Madriz López** - 0002220
- **Samuel Adonay Ortiz Carballo** - 00023020

# Gramatica 
## Regla principal (inicio de programa)
S → FN S

## Definición de funciones
FN   → TR id ( P ) FN’
TR  → T | void

## Parámetros de función
P  → T id P’ | ε
P’ → , T id P’ | ε

FN’ → ; | { B’ }

B’ → B B' | ε


## Bloque de instrucciones
B → D | ID | R | I | WH | SW 

## Declaración de Variables
D  → T V ; 
T  → int | char | float
V  → id A’ V′
V′ →, id A’ V′ | ε
A’ → = E | ε

## Asignación de Variables
ID → id ID’
ID’ → A | C 

A → = E ;


## Expresiones Aritméticas
E  → TE E'
E’ → + TE E' | - TE E' | ε
TE  → F TE'
TE’ → * F TE' | / F TE' | ε
F  → ( E ) | id F’ | numero | char 
F’ → ε | C

## Expresiones Lógicas
L  → E OP E
OP → == | > | <

## Llamada a función
C →  ( APL ); 

## Lista de Argumentos en la llamada a función
APL →  E APL’ | ε
APL’→  , E APL’ | ε

## Return (sentencia de retorno)
R → return R’ ; 
R’ → E | ε

## Condición if-else
I → if ( L ) { B' } I’
I’ →  ELSE | ε
ELSE → else ELSE’ 
ELSE’ → if ( L ) { B' } I’ | { B' } 

## Condición While
WH → while ( L ) { B' } 

## Palabras claves adicionales y sus funcionalidades (switch, case, default, break)
SWITCH → switch ( E ) { CS } 

CS → CA_LIST CA_LIST ’ | DT 
CA_LIST ‘ → DT | ε 
CA_LIST → CA CA’
CA’→CA_LIST | ε 	

CA → case E : B' BK 
DT → default : B' BK
BK → break; | ε 
