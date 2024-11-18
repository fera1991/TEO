
# Grupo 8 - Estudiantes

- **Jonathan Ariel Cabrera Galdamez** - 00003120
- **Fernando José Galdamez Mendoza** - 00120520
- **Kevin Bryan Hernández López** - 00057720
- **Manuel Alejandro Madriz López** - 0002220
- **Samuel Adonay Ortiz Carballo** - 00023020

# Gramatica 
## Regla principal (inicio de programa)
S => F S | B S | ε

## Bloque de instrucciones
B => D | A | E; | C | R | I | WH | ε

## Declaración de Variables
D => T V ;  
T => int | char | float  
V => id | V , id | V , id = E | id = E

## Asignación de Variables
A => id = E | id = C;

## Expresiones Aritméticas
E =>  
    * E + E  
    * E - E  
    * E * E  
    * E / E  
    * ( E )  
    * id  
    * número

## Expresiones Lógicas
L =>  
    * E == E  
    * E > E  
    * E < E  

## Definición de funciones
F =>  
    * T id ( P )  
    * void id ( P )  
    * T id ( P ) { B }  
    * void id ( P ) { B }

## Parámetros de función
P =>  
    * T id  
    * P , T id  
    * ε

## Llamada a función
C => id ( APL ); 

## Lista de Argumentos en la llamada a función
APL =>  
    * E  
    * E , APL  
    * ε

## Return (sentencia de retorno)
R => return E ; 

## Condición if-else
I =>  
    * if ( L ) { B } ELSEIF  
    * if ( E ) { B }

ELSEIF =>  
    * else if ( L ) { B } ELSEIF  
    * else { B }  
    * ε

## Condición While
WH =>  
    * while ( L ) { B } ;  
    * while ( E ) { B } ;

## Declaración de arreglos
ARR =>  
    * T id [ numero ] ;  
    * T id [ numero ] = { EM } ;

## Acceso a valor en arreglo
ARR => id [ E ]

EM =>  
    * { E , Elementos }  
    * { E }

Elementos =>  
    * E , Elementos  
    * E

## SW => switch ( E ) { CS DF } S
### Caso de switch
CS =>  
    * case id : B break ; CS  
    * ε

### Caso default
DF =>  
    * default : B  
    * ε
