from enum import StrEnum


class NonTerminalEnum(StrEnum):
    S = 'Start' # Initial symbol: FN S | e

    FN = 'Function' # Production for functions: TR id ( P ) FN_
    FN_ = 'Function derived' # ; | { B_ }

    TR = 'Type return' # Type return for function: void | T
    T = 'Type' # int | float | char
    P = 'Parameter' # Production for a function Parameters: T id P_ | e
    P_ = 'Parameter derived' # , T id P_ | e

    B_ = 'Block derived' # B B_ | e
    B = 'Block' # Production for Blocks: D | ID | E; | R | I | WH | SW
    
    D = 'Declaration' # T V
    V = 'Variable initialization' # id A_ V_
    V_ = 'Variable initialization derived' #, id A_ V_ | e

    A = 'Assignment' # = E
    A_ = 'Assignment derived' # = E | e

    ID = 'Assignment instruction' #Asignar valor a una varible depues de declararla: id ID_
    ID_ = "Assignment instruction derived" # A | C

#Revisar estas despues, pues tengo dudas que no permiten operar en cualquier orden
    E = 'Aritmetic Expression' # TE E_
    E_ = 'Aritmetic Expression derived' # Operación suma o resta: + TE E_ | - TE E_ | e
    TE = 'T Expression' # F TE_
    TE_ = 'T Expression derived' # Operación suma o resta: F TE_ | /F TE_ | w
    F = 'Factor' # ( E ) | id | numero | char | C

    C = 'Call' #LLamada a funcion: id (APL)
    APL = 'Argument parameters list' # E APL_ | e
    APL_ = 'Argument parameters list  derived' # , E APL_ | e
    R = 'Return' # return E;

    I = 'If' # if ( L ) { B } I_
    I_ = 'If derived' # ELSE | e
    ELSE = 'Else' # else ELSE_
    ELSE_ = 'Else derived' # if ( L ) { B } I_ | { B } 

    L = 'Logical expresion' # E OP E
    OP = "Logical operator" # == | > | <

    WH = 'While' # while ( L ) { B }

    SW = 'Switch' # switch ( E ) { CS}
    CS = 'Cases' # CA_LIST CA_LIST_ | DT
    CA_LIST = 'Cases List' # CA CA_
    CA_LIST_ = 'Cases List derived' # DT | e
    DT = 'Default' # default : B BK
    CA = 'Case' # case E : B BK
    CA_ = 'Case derived' # CA_LIST | e
    BK = 'Break' # break; | e
