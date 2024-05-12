class SymbolTable():
    classSymTable = {}
    subrSymTable = {}
    className = ""
    def __init__(self) -> None:
        self.classSymTable = {}
        self.subrSymTable = {}
        self.className = ""

    def startSubroutine(self):
        # Reset Symbol Table
        self.subrSymTable = {}

    def define(self, name, type, kind, keyword=""):
        if kind == "static":
            count = self.varCount(kind)
            self.classSymTable[name] = [name, type, kind, count]
        elif kind == "field":
            count = self.varCount("this")
            self.classSymTable[name] = [name, type, "this", count]
        else:
            if keyword != "method":
                count = self.varCount(kind)
                self.subrSymTable[name] = [name, type, kind, count]
            else:  
                if "this" not in self.subrSymTable:
                    self.subrSymTable["this"] = ["this", self.className, "argument", 0]
                if name == "this":
                     return
                count = self.varCount(kind)
                self.subrSymTable[name] = [name, type, kind, count]
                
            

    def varCount(self, kind):
        tot = 0
        if kind == "static" or kind == "field" or kind == "this":
            for value in self.classSymTable.values():
                if kind == value[2]:
                    tot += 1
        else:
            for value in self.subrSymTable.values():
                if kind == value[2]:
                    tot += 1
        return tot

    def kindOf(self, name):
        for value in self.subrSymTable.values():
                if name == value[0]:
                    return value[2]
        for value in self.classSymTable.values():
                if name == value[0]:
                    return value[2]
                
    def typeOf(self, name):
        for value in self.subrSymTable.values():
                if name == value[0]:
                    return value[1]
        for value in self.classSymTable.values():
                if name == value[0]:
                    return value[1]

    def indexOf(self, name):
        for value in self.subrSymTable.values():
                if name == value[0]:
                    return value[3]
        for value in self.classSymTable.values():
                if name == value[0]:
                    return value[3]

    def printClassDict(self):
        print(self.classSymTable)
    def printSubrDict(self):
        print(self.subrSymTable)