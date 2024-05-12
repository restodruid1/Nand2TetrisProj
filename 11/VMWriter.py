class VMWriter():
    outFile = ""
    className = ""

    def __init__(self, outPutFile) -> None:
        self.outFile = open(outPutFile, 'w')
        self.className = ""

    def writePush(self, segment, index): 
        self.outFile.write(f"push {segment} {index}\n")

    def writePop(self, segment, index):
        self.outFile.write(f"pop {segment} {index}\n")

    def writeArithmetic(self, command):
        # TODO: handle neg numbers and not
        if command == "+":
            self.outFile.write("add\n")
        elif command == "-":
            self.outFile.write("sub\n")
        elif command == "&":
            self.outFile.write("and\n")
        elif command == "|":
            self.outFile.write("or\n")
        elif command == "<":
            self.outFile.write("lt\n")
        elif command == ">":
            self.outFile.write("gt\n")
        elif command == "~":
            self.outFile.write("not\n")
        elif command == "=":
            self.outFile.write("eq\n")
        elif command == "neg":
            self.outFile.write("neg\n")
        #self.outFile.write(f"{command}\n")

    def writeLabel(self, label):
        self.outFile.write(f"label {label}\n")

    def writeGoto(self, label):
        self.outFile.write(f"goto {label}\n")

    def writeIf(self, label):
        self.outFile.write(f"if-goto {label}\n")

    def writeCall(self, label, args):
        self.outFile.write(f"call {label} {args}\n")

    def writeFunction(self, name, num):
        self.outFile.write(f"function {self.className}.{name} {num}\n")

    def writeReturn(self):
        self.outFile.write("push constant 0\n"
                           "return\n")

    def close(self):
        self.outFile.close()