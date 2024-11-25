


from NonTerminalEnum import NonTerminalEnum
from TokenEnum import TokenEnum


class printTable: 

    def __init__(self):
        pass
    
    def printC(self, string):
       print(string, end="|")

    def printLine(self):
        for i in range(30):
            print("-"),
        
        
    def print(self, table):
        printC = self.printC
        
        for NoTerminal in NonTerminalEnum:
            self.printLine()
            printC(NoTerminal.name)

            for Terminal in TokenEnum:
                text = NoTerminal.name + " -> "
                celda = table[NoTerminal][Terminal]

                if celda == []:
                    text += "'' "

                for e in celda:
                    if isinstance(e, NonTerminalEnum):
                        text += e.name + " "
                    elif e == TokenEnum.IDENTIFIER:
                        text += "id "
                    elif e == TokenEnum.NUMERIC_CONSTANT:
                        text += "num "
                    elif e == TokenEnum.CHAR_LITERAL:
                        text += "word "
                    else:
                        s = e.value
                        s = s.rstrip("_") + ("'" if s.endswith("_") else "")
                        text += s

                printC(text)