class JackCompilationEngine():
    inputTokens = []
    outPutFile = ""
    curToken = ""
    i = 0
    def __init__(self, outPutFile):
        self.outPutFile = outPutFile
        self.inputTokens = []


        # Return True if there are more tokens left
    def hasMoreTokens(self):
        if self.i < len(self.inputTokens):
            return True
        else:
            self.i = 0
            False  
    
    # If hasMoreTokens is true, this grabs the next token
    def advance(self):
        self.curToken = self.inputTokens[self.i]
        #print(self.curToken, self.i)
        self.i += 1


    def compileClass(self):
        # 'class' className '{' classVarDec* subroutineDec* '}'
        self.advance()
        print("<class>")

        if self.curToken == "class":
            print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        print(f"<identifier> {self.curToken} </identifier>")
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        
        self.advance()
        # classVarDec*
        while self.curToken in ["static", "field"]:
            #print("<classVarDec>")
            self.compileClassVarDec()
            self.advance()
            #loop = True   
            #while (loop != False):
                #loop = self.compileClassVarDec()
        
        #subroutineDec*
        while self.curToken in ['constructor','function','method']:
            #print("<subroutineDec>")
            self.compileSubroutine()
            self.advance()

        print(f"<symbol> {self.curToken} </symbol>")

        print("</class>")
        #loop2 = self.compileSubroutine()


    def compileClassVarDec(self):
        # classVarDec : ('static' | 'field) type varName (',' varName)* ';'
        #self.advance()
        #if self.curToken in ["static", "field"]:
        print("<classVarDec>")

        print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        if self.curToken in ["int", "char", "boolean"]:
            print(f"<keyword> {self.curToken} </keyword>")
        else:
            print(f"<identifier> {self.curToken} </identifier>")
        self.advance()
        print(f"<identifier> {self.curToken} </identifier>")
        self.advance()
        while self.curToken != ";":
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
            print(f"<identifier> {self.curToken} </identifier>")
            self.advance()
        print(f"<symbol> {self.curToken} </symbol>")

        print("</classVarDec>")
        #else:
            #return False
        


    def compileSubroutine(self):
        # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        #self.advance()
        #if self.token in ['constructor','function','method']:
        print("<subroutineDec>")

        print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        if self.curToken == "void":
            print(f"<keyword> {self.curToken} </keyword>")
        else:
            if self.curToken in ["int", "char", "boolean"]:
                print(f"<keyword> {self.curToken} </keyword>")
            else:
                print(f"<identifier> {self.curToken} </identifier>")
        self.advance()
        print(f"<identifier> {self.curToken} </identifier>")
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        if self.curToken != ")":
            while self.curToken != ")":
                self.compileParameterList()
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
        else:
            print("<parameterList>")
            print("</parameterList>")
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
        self.compileSubroutineBody()

        print("</subroutineDec>")
        #else:
            #return False

    def compileParameterList(self):
        print("<parameterList>")

        if self.curToken in ["int", "char", "boolean"]:
            print(f"<keyword> {self.curToken} </keyword>")
        else:
            print(f"<identifier> {self.curToken} </identifier>")
        self.advance()
        print(f"<identifier> {self.curToken} </identifier>")
        self.advance()
        while self.curToken != ")":
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
            print(f"<identifier> {self.curToken} </identifier>")
            self.advance()

        print("</parameterList>")

    def compileSubroutineBody(self):
        print("</subroutineBody>")

        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        while self.curToken == "var":
            self.compileVarDec()
            self.advance()
        # Statements
        while self.curToken != "}":
            self.compileStatements()

        print(f"<symbol> {self.curToken} </symbol>")


        print("</subroutineBody>")


    def compileVarDec(self):
        print("<varDec>")

        print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        if self.curToken in ["int", "char", "boolean"]:
            print(f"<keyword> {self.curToken} </keyword>")
        else:
            print(f"<identifier> {self.curToken} </identifier>")
        self.advance()
        print(f"<identifier> {self.curToken} </identifier>")
        #self.advance()
        #print(f"<identifier> {self.curToken} </identifier>")
        self.advance()
        while self.curToken != ";":
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
            print(f"<identifier> {self.curToken} </identifier>")
            self.advance()
        print(f"<symbol> {self.curToken} </symbol>")

        print("</varDec>")

    def compileStatements(self):
        print("<statements>")

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

            
        
        print("</statements>")

    def compileLet(self): 
        print("<letStatement>")

        print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        print(f"<identifier> {self.curToken} </identifier>")
        self.advance()
        if self.curToken == "[":
            self.compilEexpression()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        self.compileExpression()
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()

        print("</letStatement>")

    def compileIf(self):
        print("<ifStatement>")
        
        print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        self.compileExpression()
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        self.compileStatements()
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        if self.curToken == "else":
            print(f"<keyword> {self.curToken} </keyword>")
            self.advance()
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
            self.compileStatements()
            self.advance()
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()

        print("</ifStatement>")

    def compileWhile(self):
        print("<whileStatement>")

        print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        self.compileExpression()
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        self.compileStatements()
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()

        print("</whileStatement>")

    def compileDo(self):
        print("<doStatement>")

        print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        while self.curToken != ";":
            #subroutineCall
            pass
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()

        print("<doStatement>")

    def compileReturn(self):
        print("<returnStatement>")

        print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        if self.curToken != ";":
            self.compileExpression()
            self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()

        print("</returnStatement>")

    def compileExpression(self):
        pass

    def compileTerm(self):
        pass

    def compileExpressionList(self):
        pass