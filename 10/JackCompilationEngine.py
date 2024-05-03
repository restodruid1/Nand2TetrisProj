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
            #self.i = 0
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
            print("<parameterList> </parameterList>")
            #print("</parameterList>")
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
        while self.curToken == ",":
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
            if self.curToken in ["int", "char", "boolean"]:
                print(f"<keyword> {self.curToken} </keyword>")
            else:
                print(f"<identifier> {self.curToken} </identifier>")
            self.advance()
            print(f"<identifier> {self.curToken} </identifier>")
            self.advance()

        print("</parameterList>")

    def compileSubroutineBody(self):
        print("<subroutineBody>")

        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        while self.curToken == "var":
            self.compileVarDec()
            self.advance()
        # Statements
        if self.curToken != "}":
            self.compileStatements()
        #while self.curToken != "}":
            #self.compileStatements()

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
        if self.curToken not in ["let","if","while","do","return"]:
            print("<statements> </statements>")
        else:
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
            
            #self.advance()
            

    def compileLet(self): 
        print("<letStatement>")

        print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        print(f"<identifier> {self.curToken} </identifier>")
        self.advance()
        if self.curToken == "[":
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
            self.compileExpression()
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        self.compileExpression()
        #self.advance()
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
        #self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        self.compileStatements()
        #self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        #print(f"<symbol> {self.curToken} </symbol>")
        #self.advance()
        if self.curToken == "else":
            
            print(f"<keyword> {self.curToken} </keyword>")
            self.advance()
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
            self.compileStatements()
            #self.advance()
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
        #self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()
        self.compileStatements()
        #self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()

        print("</whileStatement>")

    def compileDo(self):
        print("<doStatement>")

        print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        if self.curToken != ";":
            # SubroutineCall
            #print(self.curToken, self.inputTokens[self.i],self.inputTokens[self.i+1])
            if self.inputTokens[self.i] in ["(","."]:
                #print("<subroutineCall>")
                if self.inputTokens[self.i] == "(":
                    print(f"<identifier> {self.curToken} </identifier>")
                    self.advance()
                    print(f"<symbol> {self.curToken} </symbol>")
                    self.advance()
                    if self.curToken != ")":
                        self.compileExpressionList()
                        #self.advance()
                    print(f"<symbol> {self.curToken} </symbol>")
                    self.advance()
                elif self.inputTokens[self.i] == ".":                       
                    print(f"<identifier> {self.curToken} </identifier>")
                    self.advance()
                    print(f"<symbol> {self.curToken} </symbol>")
                    self.advance()
                    print(f"<identifier> {self.curToken} </identifier>")
                    self.advance()
                    print(f"<symbol> {self.curToken} </symbol>")
                    self.advance()
                    if self.curToken != ")":
                        self.compileExpressionList()
                        #self.advance()
                    print(f"<symbol> {self.curToken} </symbol>")
                    self.advance()

                #print("</subroutineCall>")
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()

        print("</doStatement>")

    def compileReturn(self):
        print("<returnStatement>")

        print(f"<keyword> {self.curToken} </keyword>")
        self.advance()
        if self.curToken != ";":
            self.compileExpression()
            #self.advance()
        print(f"<symbol> {self.curToken} </symbol>")
        self.advance()

        print("</returnStatement>")

    
    def compileExpression(self):
        print("<expression>")
        self.compileTerm()
        while self.curToken in ['+','-','*','/','&','|','<','>','=']:    
            print("<op>")
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
            self.compileTerm()	
            print("</op>")

        print("</expression>")

    def compileTerm(self):
        print("<term>")
        if self.curToken in ['true','false','null','this']:
            # keywordConstant
            #print("<keywordConstant>")
            print(f"<keyword> {self.curToken} </keyword>")
            #print("<keywordConstant>")
            self.advance()
        elif self.curToken in ['-','~']:
            # UnaryOp term
            print("<unaryOp>")
            print(f"<keyword> {self.curToken} </keyword>")
            self.advance()
            self.compileTerm()
            print("</unaryOp>")
            self.advance()
        elif self.curToken == '"':
            # StringConstant
            print(f"<stringConstant> {self.curToken} </stringConstant>")
            self.advance()
        elif self.curToken.isdigit():
            # IntegerConstant
            print(f"<integerConstant> {self.curToken} <integerConstant>")
            self.advance()
        elif self.curToken == "(":
            # (expression)
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
            while self.curToken != ")":
                self.compileExpression()
                #self.advance()
        elif self.inputTokens[self.i] == "[":
            # varName[expression]
            print(f"<identifier> {self.curToken} </identifier>")
            self.advance()
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
            while self.curToken != "]":
                self.compileExpression()
                #self.advance()
            print(f"<symbol> {self.curToken} </symbol>")
            self.advance()
        elif self.inputTokens[self.i] in ["(","."]:
            # subroutineCall
            print("<subroutineCall>")
            if self.inputTokens[self.i] == "(":
                print(f"<identifier> {self.curToken} </identifier>")
                self.advance()
                print(f"<symbol> {self.curToken} </symbol>")
                self.advance()
                if self.curToken != ")":
                    self.compileExpressionList()
                    #self.advance()
                print(f"<symbol> {self.curToken} </symbol>")
                self.advance()
            elif self.inputTokens[self.i] == ".":
                    
                    
                print(f"<identifier> {self.curToken} </identifier>")
                self.advance()
                print(f"<symbol> {self.curToken} </symbol>")
                self.advance()
                print(f"<identifier> {self.curToken} </identifier>")
                self.advance()
                print(f"<symbol> {self.curToken} </symbol>")
                self.advance()
                if self.curToken != ")":
                    self.compileExpressionList()
                    #self.advance()
                print(f"<symbol> {self.curToken} </symbol>")
                self.advance()

            print("</subroutineCall>")

        else:
            # varName
            print(f"<identifier> {self.curToken} </identifier>")
            self.advance()
        print("</term>")


    def compileExpressionList(self):
        print("<expressionList>")
        if self.curToken != ")":
            self.compileExpression()
            #self.advance()
            while self.curToken != ")":
                if self.curToken == ",":
                    print(f"<symbol> {self.curToken} </symbol>")
                    self.advance()
                    self.compileExpression()
                    #self.advance()
        print("</expressionList>")