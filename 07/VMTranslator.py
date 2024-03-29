import sys

class Parser():
    def __init__(self, inpFile):
        self.fileName = inpFile
        self.file = None
        self.currentCommand = None
        self.allow = False
        self.command = True
        

    def openFile(self):
        try:
            self.file = open(self.fileName, 'r')
        except FileNotFoundError:
            print(f"Error: File '{self.fileName}' not found.")
    
    def hasMoreLines(self):
        if self.file:
            next_line = self.file.readline()  # Read the next line
            
            # Check if end of file has been reached
            if next_line == "":     # Check for the EOF which is blank line without '\n'
                print("EOF")
                return False
            if next_line.strip() == "":     # Checks if its an empty line 
                self.allow = False  
                return True
            if next_line[0] == "/":     # Check if line is a comment line
                self.allow = False
                return True
            
            self.allow = True
            self.currentCommand = next_line     # Sets current command to the current line in the file
            return True

        else:
            print("Error: File is not open.")

    
    def commandType(self):
        logicSet = ["add", "sub", "neg", "eq", "gt", "lt","and", "or", "not"]
        otherSet = {"push": "C_PUSH", "pop": "C_POP"}
        self.currentCommand = self.currentCommand.split()       # Splits command into 3 parts. 'Push Constant 17' becomes ['push','constant','17']
         
        # Checks if its arithmetic-logical 
        if self.currentCommand[0] in logicSet:
            self.command = True
            return "C_ARITHMETIC"
        
        if self.currentCommand[0] in otherSet:
            self.command = False
            return otherSet[self.currentCommand[0]]
         
    
    def arg1(self):
        if self.command == True:
            return self.currentCommand[0]
        else:
            return self.currentCommand[1]
    
    def arg2(self):
        return int(self.currentCommand[2])


class CodeWriter():
    def __init__(self, outFile):
        self.fileName = outFile.replace("vm", "asm")
        self.file = None
        self.counter = 0

    def openFile(self):
        self.file = open(self.fileName, 'w')
        
    def writeArithmetic(self, command):
        self.file.write(f"// {command}\n")
        if command == "add":
            self.file.write("@SP\n"
                            "AM=M-1\n"
                            "D=M\n"
                            "A=A-1\n"
                            "M=D+M\n\n")
        elif command == "sub":
            self.file.write("@SP\n"
                            "AM=M-1\n"
                            "D=M\n"
                            "A=A-1\n"
                            "M=M-D\n\n")
        elif command == "neg":
            self.file.write("@SP\n"
                            "A=M\n"
                            "A=A-1\n"
                            "M=-M\n\n")
        elif command == "eq":
            self.file.write("@SP\n"
                            "AM=M-1\n"
                            "D=M\n"
                            "@SP\n"
                            "AM=M-1\n"
                            "D=M-D\n"
                            f"@JEQ_TRUE_{self.counter}\n"
                            "D;JEQ\n"
                            "D=0\n"
                            f"@JEQ_FALSE_{self.counter}\n"
                            "0;JMP\n"
                            f"(JEQ_TRUE_{self.counter})\n"
                            "D=-1\n"
                            f"(JEQ_FALSE_{self.counter})\n"
                            "@SP\n"
                            "A=M\n"
                            "M=D\n"
                            "@SP\n"
                            "M=M+1\n\n")
            self.counter += 1
        elif command == "gt":
            self.file.write("@SP\n"
                            "AM=M-1\n"
                            "D=M\n"
                            "@SP\n"
                            "AM=M-1\n"
                            "D=M-D\n"
                            f"@JGT_TRUE_{self.counter}\n"
                            "D;JGT\n"
                            "D=0\n"
                            f"@JGT_FALSE_{self.counter}\n"
                            "0;JMP\n"
                            f"(JGT_TRUE_{self.counter})\n"
                            "D=-1\n"
                            f"(JGT_FALSE_{self.counter})\n"
                            "@SP\n"
                            "A=M\n"
                            "M=D\n"
                            "@SP\n"
                            "M=M+1\n\n") 
            self.counter += 1
        elif command == "lt":
            self.file.write("@SP\n"
                            "AM=M-1\n"
                            "D=M\n"
                            "@SP\n"
                            "AM=M-1\n"
                            "D=M-D\n"
                            f"@JLT_TRUE_{self.counter}\n"
                            "D;JLT\n"
                            "D=0\n"
                            f"@JLT_FALSE_{self.counter}\n"
                            "0;JMP\n"
                            f"(JLT_TRUE_{self.counter})\n"
                            "D=-1\n"
                            f"(JLT_FALSE_{self.counter})\n"
                            "@SP\n"
                            "A=M\n"
                            "M=D\n"
                            "@SP\n"
                            "M=M+1\n\n")
            self.counter += 1
        elif command == "and":
            self.file.write("@SP\n"
                            "AM=M-1\n"
                            "D=M\n"
                            "A=A-1\n"
                            "M=D&M\n\n")
        elif command == "or":
            self.file.write("@SP\n"
                            "AM=M-1\n"
                            "D=M\n"
                            "A=A-1\n"
                            "M=D|M\n\n")
        elif command == "not":
            self.file.write("@SP\n"
                            "A=M\n"
                            "A=A-1\n"
                            "M=!M\n\n")
        elif command == "end":
            self.file.write("(END)"
                            "@END"
                            "0;JMP")       

    def writePushPop(self, command, segment, index):
        self.file.write(f"// {command} {segment} {index}\n")
        tmp = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT" }
        
        if command == "push":
            if segment == "constant":
                self.file.write(f"@{index}\n"
                            "D=A\n"
                            "@SP\n"
                            "A=M\n"
                            "M=D\n"
                            "@SP\n"
                            "M=M+1\n\n")
            elif segment in ['static','temp','pointer']:                   
                if segment == 'static':
                    self.file.write(f"@16\n"
                            "D=A\n"
                            f"@{index}\n"
                            "A=D+A\n"       
                            "D=M\n"
                            "@SP\n"
                            "A=M\n"
                            "M=D\n"
                            "@SP\n"
                            "M=M+1\n\n")
                if segment == 'pointer':
                    self.file.write(f"@R{3+int(index)}\n"
                            "D=A\n"
                            f"@{3+int(index)}\n"
                            #"A=D+A\n"          
                            "D=M\n"
                            "@SP\n"
                            "A=M\n"
                            "M=D\n"
                            "@SP\n"
                            "M=M+1\n\n")
                if segment == "temp":
                    self.file.write(f"@{5+int(index)}\n"
                                "D=A\n"
                                f"@{5+int(index)}\n" #
                                #"A=D+A\n"   #
                                "D=M\n" #
                                "@SP\n" #
                                "A=M\n" #
                                "M=D\n" #   
                                "@SP\n"
                                "M=M+1\n\n")
            elif segment in tmp:
                self.file.write(f"@{tmp[segment]}\n"
                                "D=M\n"
                                f"@{index}\n"
                                "A=D+A\n"
                                "D=M\n"
                                "@SP\n"
                                "A=M\n"
                                "M=D\n"
                                "@SP\n"
                                "M=M+1\n\n")
        else: # command == "pop"
            if segment == "static":
                self.file.write(f"@16\n"
                                "D=A\n" 
                                f"@{index}\n"
                                "D=D+A\n"
                                "@R13\n"
                                "M=D\n"
                                "@SP\n"
                                "AM=M-1\n"
                                "D=M\n"
                                "@R13\n"
                                "A=M\n"
                                "M=D\n\n")
            else:
                if segment in tmp:
                    self.file.write(f"@{tmp[segment]}\n"
                                "D=M\n" 
                                f"@{index}\n"
                                "D=D+A\n"
                                "@R13\n"
                                "M=D\n"
                                "@SP\n"
                                "AM=M-1\n"
                                "D=M\n"
                                "@R13\n"
                                "A=M\n"
                                "M=D\n\n")
                elif segment == "pointer":
                    self.file.write(f"@R{3+int(index)}\n"
                                "D=M\n" 
                                f"@{3+int(index)}\n"
                                "D=D+A\n"
                                "@R13\n"
                                "M=D\n"
                                "@SP\n"
                                "AM=M-1\n"
                                "D=M\n"
                                "@R13\n"
                                "A=M\n"
                                "M=D\n\n")
                elif segment == "temp":
                    self.file.write(f"@R{5+int(index)}\n"
                                "D=M\n" 
                                f"@{5+int(index)}\n"
                                "D=D+A\n"
                                "@R13\n"
                                "M=D\n"
                                "@SP\n"
                                "AM=M-1\n"
                                "D=M\n"
                                "@R13\n"
                                "A=M\n"
                                "M=D\n\n")
        
        
    def close(self):
        self.file.close()



root = sys.argv[1]  # Input VM file

parser = Parser(root)
parser.openFile()
codeWriter = CodeWriter(root)
codeWriter.openFile()


while parser.hasMoreLines() == True:
    if parser.allow == False:
        continue
    
    instrType = parser.commandType()   
    arg1 = parser.arg1()

    if parser.command == False:
        arg2 = parser.arg2()
        print(instrType,arg1,arg2)
        codeWriter.writePushPop(parser.currentCommand[0],parser.currentCommand[1],parser.currentCommand[2])
    else:
        print(instrType,arg1)
        codeWriter.writeArithmetic(parser.currentCommand[0])

codeWriter.close()