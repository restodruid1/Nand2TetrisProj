import SymbolTable
import VMWriter

class JackCompilationEngine():
    inputTokens = []
    outPutFile = ""
    curToken = ""
    i = 0
    args = 0
    isNeg = False
    funcName = ""
    funcType = ""
    funcKind = ""
    className = ""
    funcVari = 0
    uniqueLabel = 0

    def __init__(self, outPutFile):
        self.outPutFile = outPutFile
        self.inputTokens = []
        self.outFile = open(outPutFile, 'w')
        self.symbTbl = SymbolTable.SymbolTable()
        self.VmWriter = VMWriter.VMWriter(outPutFile.replace(".txt", ".vm"))
        self.args = 0 
        self.isNeg = False
        self.funcName = ""
        self.funcType = ""
        self.funcVari = 0
        self.uniqueLabel = 0
        self.funcKind = ""
        self.className = ""

        # Return True if there are more tokens left
    def hasMoreTokens(self):
        if self.i < len(self.inputTokens):
            return True
        else:
            #self.i = 0
            False  
    
    # If hasMoreTokens is true, this grabs the next token
    def advance(self):
        self.curToken = self.inputTokens[self.i]
        self.i += 1



    def compileClass(self):     
        # 'class' className '{' classVarDec* subroutineDec* '}'
        self.advance()
        self.outFile.write("<class>\n")
        print(self.inputTokens)
        if self.curToken == "class":
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        self.symbTbl.className = self.curToken
        self.className = self.curToken
        self.VmWriter.className = self.curToken
        self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        
        self.advance()
        # classVarDec*
        if self.curToken in ["static", "field"]:
            while self.curToken in ["static", "field"]:
                self.compileClassVarDec()
                self.advance()
        print(self.symbTbl.printClassDict())
        #subroutineDec*
        while self.curToken in ['constructor','function','method']:
            self.compileSubroutine()
            self.advance()
            #self.VmWriter.writeReturn()
        #print(self.symbTbl.printSubrDict())
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")

        self.outFile.write("</class>\n")
    


    def compileClassVarDec(self):
        # classVarDec : ('static' | 'field) type varName (',' varName)* ';'
        kind = ""
        type1 = ""
        self.outFile.write("<classVarDec>\n")

        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        kind = self.curToken
        self.advance()
        if self.curToken in ["int", "char", "boolean"]:
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        else:
            #self.symbTbl.define(f"{self.curToken}",)
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        type1 = self.inputTokens[self.i-2]
        self.symbTbl.define(f"{self.curToken}", type1, kind)
        self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        while self.curToken != ";":
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.symbTbl.define(f"{self.curToken}", type1, kind)
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")

        self.outFile.write("</classVarDec>\n")
        


    def compileSubroutine(self):
        # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        keyword = self.curToken
        self.funcKind = self.curToken
        self.outFile.write("<subroutineDec>\n")
        self.symbTbl.startSubroutine()
        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        
        
        if self.curToken == "void":
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        else:
            if self.curToken in ["int", "char", "boolean"]:
                self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
            else:
                self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.funcName = self.curToken
        self.advance()
        #self.VmWriter.writeFunction()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        if self.curToken != ")":
            while self.curToken != ")":
                
                self.compileParameterList()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
        else:
            if keyword == "method":
                self.symbTbl.define(f"this", self.symbTbl.className, "argument", keyword)
            #self.VmWriter.writeFunction(self.funcName, 0)
            self.outFile.write("<parameterList>\n </parameterList>\n")
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
        self.compileSubroutineBody()
        print(self.symbTbl.printSubrDict())
        self.outFile.write("</subroutineDec>\n")


    def compileParameterList(self):
        type1 = ""
        keyword = self.inputTokens[self.i - 5]
        self.funcType = keyword
        print(self.inputTokens[self.i - 4])
        print(keyword + "!!!!!!!")
        self.outFile.write("<parameterList>\n")

        if self.curToken in ["int", "char", "boolean"]:
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        else:
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        
        self.advance()
        type1 = self.inputTokens[self.i-2]
        print(keyword)
        print(type1)
        print(self.curToken + "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        self.symbTbl.define(f"{self.curToken}", type1, "argument", keyword)
        self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        #i = 1
        while self.curToken == ",":
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            if self.curToken in ["int", "char", "boolean"]:
                self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
            else:
                self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()
            type1 = self.inputTokens[self.i-2]
            self.symbTbl.define(f"{self.curToken}", type1, "argument", keyword)
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()
            #i += 1
        
        #self.VmWriter.writeFunction(self.funcName, i)
        self.outFile.write("</parameterList>\n")

    def compileSubroutineBody(self):
        self.outFile.write("<subroutineBody>\n")

        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        while self.curToken == "var":
            self.compileVarDec()
            self.advance()
        
        self.VmWriter.writeFunction(self.funcName, self.funcVari)
        if self.funcKind == "method":           
            self.VmWriter.writePush("argument", 0)
            self.VmWriter.writePop("pointer", 0)
        else:
            if self.funcKind == "constructor":
                self.VmWriter.writePush("constant", self.symbTbl.varCount("this"))
                self.VmWriter.writeCall("Memory.alloc", 1)
                self.VmWriter.writePop("pointer", 0)

        self.funcVari = 0
        # Statements
        if self.curToken != "}":
            self.compileStatements()

        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")

        self.outFile.write("</subroutineBody>\n")


    def compileVarDec(self):
        self.outFile.write("<varDec>\n")

        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        if self.curToken in ["int", "char", "boolean"]:
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        else:
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        type1 = self.inputTokens[self.i - 2]
        self.symbTbl.define(f"{self.curToken}", type1, "local")
        self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        self.funcVari += 1
        while self.curToken != ";":
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.symbTbl.define(f"{self.curToken}", type1, "local")
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()
            self.funcVari += 1
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        
        self.outFile.write("</varDec>\n")


    def compileStatements(self):
        if self.curToken not in ["let","if","while","do","return"]:
            self.outFile.write("<statements>\n </statements>\n")
        else:
            self.outFile.write("<statements>\n")
            while self.curToken in ["let","if","while","do","return"]:
                if self.curToken == "let":
                    self.compileLet()
                elif self.curToken == "if":
                    self.compileIf()
                elif self.curToken == "while":
                    self.compileWhile()
                elif self.curToken == "do":
                    self.compileDo()
                elif self.curToken == "return":
                    self.compileReturn()
            self.outFile.write("</statements>\n")
            
            

    def compileLet(self): 
        self.outFile.write("<letStatement>\n")
        
        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        
        var = self.symbTbl.kindOf(self.curToken), self.symbTbl.indexOf(self.curToken) 
        #print(self.curToken)
        #if self.symbTbl.subrSymTable.get(self.curToken):
            #self.VmWriter.writePush(self.symbTbl.subrSymTable[self.curToken][0],self.symbTbl.subrSymTable[self.curToken][3])
        #else:
            #self.VmWriter.writePush(self.symbTbl.classSymTable[self.curToken][0],self.symbTbl.classSymTable[self.curToken][3])
        self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        if self.curToken == "[":   
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.VmWriter.writePush(self.symbTbl.kindOf(self.inputTokens[self.i - 3]), self.symbTbl.indexOf(self.inputTokens[self.i - 3]))
            self.compileExpression()
            self.VmWriter.writeArithmetic("+")
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            tmp = self.inputTokens[self.i]
            print(tmp)
            print(tmp + "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if tmp != "[":
                self.VmWriter.writePop("pointer", 1)
                #self.VmWriter.writePop("temp", 0)
                self.compileExpression()
                #self.VmWriter.writePush("temp", 0)
                #self.VmWriter.writePop("pointer", 1)
                self.VmWriter.writePop("that", 0)
            else:
                self.compileExpression()
            """if tmp != "[":
                self.VmWriter.writePop("temp", 0)
                self.VmWriter.writePop("pointer", 1)
                self.VmWriter.writePush("temp", 0)
                self.VmWriter.writePop("that", 0)"""
            

            #self.VmWriter.writePop(var[0], var[1])
            #self.VmWriter.writePop("temp", 0)
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
        else:
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.compileExpression()
            self.VmWriter.writePop(var[0], var[1])
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()

        self.outFile.write("</letStatement>\n")

    def compileIf(self):
        self.outFile.write("<ifStatement>\n")
        l1 = f"if{self.uniqueLabel}"
        l2 = f"el{self.uniqueLabel}"
        self.uniqueLabel += 1
        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.compileExpression()
        self.VmWriter.outFile.write("not\n")
        self.VmWriter.writeIf(l2)
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.compileStatements()
        self.VmWriter.writeGoto(l1)
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        if self.curToken == "else":
            self.VmWriter.writeLabel(l2)
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
            self.advance()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.compileStatements()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.VmWriter.writeLabel(l1)
        else:
            self.VmWriter.writeLabel(l2)
            self.VmWriter.writeLabel(l1)

        
        self.outFile.write("</ifStatement>\n")

    def compileWhile(self):
        l1 = f"do{self.uniqueLabel}"
        l2 = f"wh{self.uniqueLabel}"
        self.uniqueLabel += 1
        self.outFile.write("<whileStatement>\n")
        self.VmWriter.writeLabel(l1)
        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.compileExpression()
        self.VmWriter.outFile.write("not\n")
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.VmWriter.writeIf(l2)
        self.advance()
        self.compileStatements()
        self.VmWriter.writeGoto(l1)
        self.VmWriter.writeLabel(l2)
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        
        
        self.outFile.write("</whileStatement>\n")

    def compileDo(self):
        self.outFile.write("<doStatement>\n")
        func = ""
        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        
        #print(className + "TJosc;lssanmme" + methodName)
        if self.curToken != ";":
            # SubroutineCall
            if self.inputTokens[self.i] in ["(","."]:

                if self.inputTokens[self.i] == "(":
                    func = self.curToken
                    self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
                    self.advance()
                    self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                    self.advance()
                    #if self.curToken != ")":
                    self.compileExpressionList()
                        #self.advance()
                    self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                    self.advance()
                    self.VmWriter.writePush("pointer", 0)
                    self.VmWriter.writeCall(self.className + "." + func, self.args + 1)

                elif self.inputTokens[self.i] == ".":                       
                    methodName = self.inputTokens[self.i] + self.inputTokens[self.i + 1]
                    className = self.curToken
                    self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
                    self.advance()
                    self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                    self.advance()
                    func = self.inputTokens[self.i-3] + self.inputTokens[self.i-2] + self.curToken
                    self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
                    self.advance()
                    self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                    self.advance()
                    #if self.curToken != ")":
                    self.compileExpressionList()
                        #self.advance()
                    self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                    self.advance()
                    if className in self.symbTbl.subrSymTable:
                        self.VmWriter.writePush(self.symbTbl.kindOf(className), self.symbTbl.indexOf(className))
                        self.VmWriter.writeCall(self.symbTbl.typeOf(className) + methodName, self.args + 1)
                    elif className in self.symbTbl.classSymTable:
                        self.VmWriter.writePush(self.symbTbl.kindOf(className), self.symbTbl.indexOf(className))
                        self.VmWriter.writeCall(self.symbTbl.typeOf(className) + methodName, self.args + 1)
                    else:
                        print("yoooooooaaaaaaaaaaaaaaaaaaaaaa")    
                        self.VmWriter.writeCall(func, self.args)
        #self.VmWriter.writeCall(func, self.args)
        self.VmWriter.writePop("temp", "0")
        self.args = 0        
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()

        self.outFile.write("</doStatement>\n")

    def compileReturn(self):
        self.outFile.write("<returnStatement>\n")

        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        
        if self.curToken != ";":
            self.compileExpression()
            self.VmWriter.outFile.write("return\n")
        else:
            self.VmWriter.writeReturn()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.outFile.write("</returnStatement>\n")

    
    def compileExpression(self):
        self.outFile.write("<expression>\n")
        
        self.compileTerm()
        
        while self.curToken in ['+','-','*','/','&','|','<','>','=','&lt;','&gt;','&amp;']:    
            if self.curToken in ['<', '&lt;']:
                self.outFile.write("<symbol> < </symbol>\n")
            elif self.curToken in ['>','&gt;']:
                self.outFile.write("<symbol> > </symbol>\n")
            elif self.curToken in ['&','&amp;']:
                self.outFile.write("<symbol> & </symbol>\n")
            else:
                self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            op = self.curToken
            self.advance()
            self.compileTerm()
            if op == "*":
                self.VmWriter.writeCall("Math.multiply", 2)
            elif op == "/":
                self.VmWriter.writeCall("Math.divide", 2)
            else:
                self.VmWriter.writeArithmetic(op)	

        self.outFile.write("</expression>\n")

    def compileTerm(self):
        self.outFile.write("<term>\n")
        if self.curToken in ['true','false','null','this']:
            # keywordConstant
            if self.curToken == "true":
                self.VmWriter.writePush("constant", "1")
                self.VmWriter.writeArithmetic("neg")
            elif self.curToken == "false":
                self.VmWriter.writePush("constant", "0")
            elif self.curToken == "null":
                self.VmWriter.writePush("constant", "0")
            elif self.curToken == "this":
                self.VmWriter.writePush("pointer", "0")
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
            self.advance()

        elif self.curToken in ['-','~']:
            # UnaryOp term
            print(self.inputTokens[self.i])
            print(self.curToken)
            if self.curToken == "-" and self.inputTokens[self.i].isdigit():
                self.isNeg = True
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            tildeTmp = self.curToken
            self.advance()
            self.compileTerm()
            if tildeTmp == "~":
                self.VmWriter.writeArithmetic("~")
    
        elif self.curToken[0] == '"':
            # StringConstant
            self.VmWriter.writePush("constant", len(self.curToken[1:-1]))
            self.VmWriter.writeCall("String.new", 1)
            for char in self.curToken[1:-1]:
                self.VmWriter.writePush("constant", ord(char))
                self.VmWriter.writeCall("String.appendChar", 2)
            self.outFile.write(f"<stringConstant> {self.curToken[1:-1]} </stringConstant>\n")
            self.advance()

        elif self.curToken.isdigit():
            # IntegerConstant
            self.outFile.write(f"<integerConstant> {self.curToken} </integerConstant>\n")
            if self.isNeg == True:
                self.VmWriter.writePush("constant", self.curToken)
                self.VmWriter.writeArithmetic("neg")
            else:
                self.VmWriter.writePush("constant", self.curToken)
            self.isNeg = False
            #print(self.curToken)
            #print(self.inputTokens)
            self.advance()
            #print(self.curToken)

        elif self.curToken == "(":
            # (expression)
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            if self.curToken != ")":
            #while self.curToken != ")":
                self.compileExpression()
                #self.advance()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()

        elif self.inputTokens[self.i] == "[":
            # varName[expression]
            tmp = self.inputTokens[self.i - 3]
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            if self.curToken != "]":
                if tmp == "]":
                    self.VmWriter.writePush(self.symbTbl.kindOf(self.inputTokens[self.i - 3]), self.symbTbl.indexOf(self.inputTokens[self.i - 3]))
                    self.compileExpression()
                    self.VmWriter.writeArithmetic("+")
                    self.VmWriter.writePop("pointer", 1)
                    self.VmWriter.writePush("that", 0)
                    self.VmWriter.writePop("temp", 0)
                    self.VmWriter.writePop("pointer", 1)
                    self.VmWriter.writePush("temp", 0)
                    self.VmWriter.writePop("that", 0)
                else:
                    self.VmWriter.writePush(self.symbTbl.kindOf(self.inputTokens[self.i - 3]), self.symbTbl.indexOf(self.inputTokens[self.i - 3]))
                    self.compileExpression()
                    self.VmWriter.writeArithmetic("+")
                    self.VmWriter.writePop("pointer", 1)
                    self.VmWriter.writePush("that", 0)
                #self.advance()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()

        elif self.inputTokens[self.i] in ["(","."]:
            # subroutineCall
            if self.inputTokens[self.i] == "(":
                self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
                self.advance()
                self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                self.advance()
                #if self.curToken != ")":
                self.compileExpressionList()
                    #self.advance()
                self.VmWriter.writeCall(func, self.args)
                self.args = 0
                self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                self.advance()

            elif self.inputTokens[self.i] == ".":
                func = self.curToken + self.inputTokens[self.i] + self.inputTokens[self.i + 1]
                methodName = self.inputTokens[self.i] + self.inputTokens[self.i + 1]
                className = self.curToken    
                print(methodName, className)                
                self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
                self.advance()
                self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                self.advance()
                self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
                self.advance()
                self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                self.advance()
                #if self.curToken != ")":
                self.compileExpressionList()
                    #self.advance()
                print(self.symbTbl.typeOf(className))
                if self.symbTbl.typeOf(className):
                    print("yoooooooooooooooooooooooooooooooooooooooooooo")
                    self.VmWriter.writeCall(self.symbTbl.typeOf(className) + methodName, self.args + 1)
                else:
                    print("yoooooooaaaaaaaaaaaaaaaaaaaaaa")    
                    self.VmWriter.writeCall(func, self.args)
                self.args = 0
                self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                self.advance()

        else:
            # varName
            #if self.symbTbl.subrSymTable.get(self.curToken):
                #self.VmWriter.writePush(self.symbTbl.subrSymTable[self.curToken][0],self.symbTbl.subrSymTable[self.curToken][3])
            #else:
                #self.VmWriter.writePush(self.symbTbl.classSymTable[self.curToken][0],self.symbTbl.classSymTable[self.curToken][3])
            self.VmWriter.writePush(self.symbTbl.kindOf(self.curToken), self.symbTbl.indexOf(self.curToken))
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()

        self.outFile.write("</term>\n")


    def compileExpressionList(self):
        if self.curToken != ")":
            self.outFile.write("<expressionList>\n")
            self.compileExpression()
            self.args += 1
            while self.curToken != ")":
                if self.curToken == ",":
                    self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                    self.advance()
                    self.compileExpression()
                self.args += 1
            self.outFile.write("</expressionList>\n")
        else:
            self.outFile.write("<expressionList>\n </expressionList>\n")