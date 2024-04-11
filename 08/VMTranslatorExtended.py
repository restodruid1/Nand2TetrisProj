# To use via windows command prompt - \path\to\the\VmTranslator\ "\path\to\desired\vm\file" True if bootstrap, False if not
import sys
import os

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
        otherSet = {"push": "C_PUSH", "pop": "C_POP", "label":"C_LABEL", "goto":"C_GOTO", "if-goto":"C_IF", "function":"C_FUNCTION", "call":"C_CALL", "return":"C_RETURN"}
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
        self.cwFilePath = None
        self.file = None
        self.counter = 0
        self.bootstrap = False
        self.iD = 0

    def openFile(self):
        self.file = open(self.cwFilePath, 'w')
        
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
                    self.file.write(f"@{programName}.{index}\n"
                                    "D=M\n"
                                    "@SP\n"
                                    "A=M\n"
                                    "M=D\n"
                                    "@SP\n"
                                    "M=M+1\n\n")    
                    
                if segment == 'pointer':
                    self.file.write(f"@R{3+int(index)}\n"
                            "D=M\n"
                            "@SP\n"
                            "A=M\n"
                            "M=D\n"
                            "@SP\n"
                            "M=M+1\n\n")
                if segment == "temp":
                    self.file.write(f"@{5+int(index)}\n"
                                "D=M\n" 
                                "@SP\n" 
                                "A=M\n" 
                                "M=D\n"   
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
                self.file.write("@SP\n"
                                "AM=M-1\n"
                                "D=M\n"
                                f"@{programName}.{index}\n"
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
                    self.file.write("@SP\n"                                   
                                "AM=M-1\n"
                                "D=M\n"
                                f"@{3+int(index)}\n"
                                "M=D\n\n")
                elif segment == "temp":
                    self.file.write("@SP\n"
                                "AM=M-1\n"
                                "D=M\n"
                                f"@{5+int(index)}\n"
                                "M=D\n\n")
        
    def writeLable(self, labelStr):
        self.file.write(f"({labelStr})\n\n")
    
    def writeGoto(self, labelStr):
        self.file.write(f"@{labelStr}\n"
                        "0;JMP\n\n")
    
    def writeIf(self, labelStr):
        self.file.write("@SP\n"
                        "AM=M-1\n"
                        "D=M\n"
                        f"@{labelStr}\n"
                        "D;JNE\n\n")
    
    def writeFunction(self, functionName, nVars):
        #nVars = int(nVars)
        self.file.write(f"({functionName})\n\n"
                        f"@{nVars}\n"
                        "D=A\n"
                        "@R13\n"
                        "M=D\n"
                        f"({functionName}LOOP)\n"
                        f"@{functionName}LOOPEND\n"
                        "D;JEQ\n"
                        "@0\n"
                        "D=A\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "M=M+1\n"
                        "@R13\n"
                        "MD=M-1\n"
                        f"@{functionName}LOOP\n"
                        "0;JMP\n"
                        f"({functionName}LOOPEND)\n") 

    
    def writeCall(self, functionName, nArgs):
        self.iD += 1
        self.file.write(f"@{functionName}_RETURN_{self.iD}\n"
                        "D=A\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "M=M+1\n\n"

                        "@LCL\n"
                        "D=M\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "M=M+1\n\n"
                        
                        "@ARG\n"
                        "D=M\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "M=M+1\n\n"
                        
                        "@THIS\n"
                        "D=M\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "M=M+1\n\n"
                        
                        "@THAT\n"
                        "D=M\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "M=M+1\n\n"

                        f"@{nArgs}\n" 
                        "D=A\n"
                        "@5\n"
                        "D=D+A\n"
                        "@SP\n"
                        "D=M-D\n"
                        "@ARG\n"
                        "M=D\n\n"
                        
                        "@SP\n"
                        "D=M\n"
                        "@LCL\n"
                        "M=D\n\n"

                        f"@{functionName}\n"
                        "0;JMP\n\n"

                        f"({functionName}_RETURN_{self.iD})\n\n")
                        
    
    def writeReturn(self):
        self.file.write("@LCL\n"
                        "D=M\n"
                        "@R13\n"
                        "M=D\n"

                        "@5\n"
                        "A=D-A\n"
                        "D=M\n"
                        "@R14\n"
                        "M=D\n"

                        "@SP\n"
                        "AM=M-1\n"
                        "D=M\n"
                        "@ARG\n"
                        "A=M\n"
                        "M=D\n"

                        "D=A\n"
                        "@SP\n"
                        "M=D+1\n"

                        "@R13\n"
                        "AM=M-1\n"
                        "D=M\n"
                        "@THAT\n"
                        "M=D\n"

                        "@R13\n"
                        "AM=M-1\n"
                        "D=M\n"
                        "@THIS\n"
                        "M=D\n"

                        "@R13\n"
                        "AM=M-1\n"
                        "D=M\n"
                        "@ARG\n"
                        "M=D\n"

                        "@R13\n"
                        "AM=M-1\n"
                        "D=M\n"
                        "@LCL\n"
                        "M=D\n"

                        "@R14\n"
                        "A=M\n"
                        "0;JMP\n")
        
         
    
    def bootStrap(self):
        self.file.write("@256\n"
                        "D=A\n"
                        "@SP\n"
                        "M=D\n")
        self.writeCall("Sys.init", 0)
        self.file.write(f"(BOOTSTRAP_{programName})\n"
                        f"@BOOTSTRAP_{programName}\n"
                        "0;JMP\n\n")
    
    def close(self):
        self.file.close()



def process_file(file_path):
    while parser.hasMoreLines() == True:
        if codeWriter.bootstrap == False:
            if bStrap == "True":
                codeWriter.bootStrap()
                codeWriter.bootstrap = True
            
        if parser.allow == False:
            continue
        
        instrType = parser.commandType()   
        if instrType == "C_RETURN":
            codeWriter.writeReturn()
            continue
        arg1 = parser.arg1()
        print(instrType, arg1)
        print(parser.currentCommand)
        
        #if instrType == "C_RETURN":
            #codeWriter.writeReturn()
        if instrType == "C_ARITHMETIC":
            codeWriter.writeArithmetic(parser.currentCommand[0])
        elif instrType == "C_LABEL":
            codeWriter.writeLable(parser.currentCommand[1])
        elif instrType == "C_IF":
            codeWriter.writeIf(parser.currentCommand[1])
        elif instrType == "C_GOTO":
            codeWriter.writeGoto(parser.currentCommand[1])
        elif instrType == "C_FUNCTION":
            codeWriter.writeFunction(parser.currentCommand[1],parser.currentCommand[2])
        elif instrType == "C_CALL":
            codeWriter.writeCall(parser.currentCommand[1],parser.currentCommand[2])
        elif instrType == "C_PUSH" or instrType == "C_POP":
            codeWriter.writePushPop(parser.currentCommand[0],parser.currentCommand[1],parser.currentCommand[2])

    



root = sys.argv[1]      # Input VM file
bStrap = sys.argv[2]    # True if bootstrap is needed, else False
programName = ""



parser = Parser(root)
# Check if the provided path is a directory
if os.path.isdir(parser.fileName):
    name = parser.fileName + ".vm"
    codeWriter = CodeWriter(name)
    name = name.replace(".vm", ".asm")
    name = name.split("\\")
    name = name[-1]
    codeWriter.cwFilePath = os.path.join(root, name)    # '\path\to\your\desired\directory\' + file.asm
    codeWriter.openFile()
    
    # List all files in the directory
    files = os.listdir(parser.fileName)
    print(files)
    tmpDir = []
    for file in files:
        # Store only .vm files
        if ".vm" in file:
            if "Sys" in file:
                tmpDir.insert(0,file)
            else:
                tmpDir.append(file)
    # Parse through .vm files and translate them  
    for file in tmpDir:
        programName = file
        file_path = os.path.join(root, file)
        parser.fileName = file_path
        parser.openFile()
        process_file(file)
    codeWriter.close()
else:
# Translate if file, not directory/folder
    programName = root
    parser.openFile()
    codeWriter = CodeWriter(parser.fileName)
    codeWriter.cwFilePath = root
    codeWriter.openFile()
    process_file(parser.fileName)
    codeWriter.close()

