import sys

class Parser():
    def __init__(self, inpFile):
        self.fileName = inpFile
        self.file = None
        self.currentCommand = None
        self.allow = False
        self.command = True
        #self.arg2 = None

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
        self.file = outFile

    def writeArithmetic(self, command):
        pass

    def writePushPop(self, command, segment, index):
        pass

    def close():
        pass



root = sys.argv[1]  # Input VM file

parser = Parser(root)
parser.openFile()


while parser.hasMoreLines() == True:
    if parser.allow == False:
        continue
    
    instrType = parser.commandType()   
    arg1 = parser.arg1()

    if parser.command == False:
        arg2 = parser.arg2()
        print(instrType,arg1,arg2)
    else:
        print(instrType,arg1)


