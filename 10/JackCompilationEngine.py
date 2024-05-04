class JackCompilationEngine():
    inputTokens = []
    outPutFile = ""
    curToken = ""
    i = 0
    def __init__(self, outPutFile):
        self.outPutFile = outPutFile
        self.inputTokens = []
        self.outFile = open(outPutFile, 'w')

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
        #print(self.inputTokens)
        if self.curToken == "class":
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        
        self.advance()
        # classVarDec*
        while self.curToken in ["static", "field"]:
            self.compileClassVarDec()
            self.advance()
        
        #subroutineDec*
        while self.curToken in ['constructor','function','method']:
            self.compileSubroutine()
            self.advance()

        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")

        self.outFile.write("</class>\n")
    


    def compileClassVarDec(self):
        # classVarDec : ('static' | 'field) type varName (',' varName)* ';'
        self.outFile.write("<classVarDec>\n")

        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        if self.curToken in ["int", "char", "boolean"]:
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        else:
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        while self.curToken != ";":
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")

        self.outFile.write("</classVarDec>\n")
        


    def compileSubroutine(self):
        # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
        self.outFile.write("<subroutineDec>\n")

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
        self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        if self.curToken != ")":
            while self.curToken != ")":
                self.compileParameterList()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
        else:
            self.outFile.write("<parameterList>\n </parameterList>\n")
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
        self.compileSubroutineBody()

        self.outFile.write("</subroutineDec>\n")


    def compileParameterList(self):
        self.outFile.write("<parameterList>\n")

        if self.curToken in ["int", "char", "boolean"]:
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        else:
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        while self.curToken == ",":
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            if self.curToken in ["int", "char", "boolean"]:
                self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
            else:
                self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()

        self.outFile.write("</parameterList>\n")

    def compileSubroutineBody(self):
        self.outFile.write("<subroutineBody>\n")

        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        while self.curToken == "var":
            self.compileVarDec()
            self.advance()
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
        self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        while self.curToken != ";":
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()
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
        self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
        self.advance()
        if self.curToken == "[":
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.compileExpression()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.compileExpression()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()

        self.outFile.write("</letStatement>\n")

    def compileIf(self):
        self.outFile.write("<ifStatement>\n")
        
        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.compileExpression()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.compileStatements()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        if self.curToken == "else":
            
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
            self.advance()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.compileStatements()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()

        self.outFile.write("</ifStatement>\n")

    def compileWhile(self):
        self.outFile.write("<whileStatement>\n")

        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.compileExpression()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()
        self.compileStatements()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()

        self.outFile.write("</whileStatement>\n")

    def compileDo(self):
        self.outFile.write("<doStatement>\n")

        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        if self.curToken != ";":
            # SubroutineCall
            if self.inputTokens[self.i] in ["(","."]:

                if self.inputTokens[self.i] == "(":
                    self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
                    self.advance()
                    self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                    self.advance()
                    #if self.curToken != ")":
                    self.compileExpressionList()
                        #self.advance()
                    self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                    self.advance()

                elif self.inputTokens[self.i] == ".":                       
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
                    self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                    self.advance()

                
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()

        self.outFile.write("</doStatement>\n")

    def compileReturn(self):
        self.outFile.write("<returnStatement>\n")

        self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
        self.advance()
        if self.curToken != ";":
            self.compileExpression()
        self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
        self.advance()

        self.outFile.write("</returnStatement>\n")

    
    def compileExpression(self):
        self.outFile.write("<expression>\n")
        self.compileTerm()

        while self.curToken in ['+','-','*','/','&','|','<','>','=','&lt;','&gt;','&amp;']:    
            if self.curToken in ['<', '&lt;']:
                self.outFile.write("<symbol> &lt; </symbol>\n")
            elif self.curToken in ['>','&gt;']:
                self.outFile.write("<symbol> &gt; </symbol>\n")
            elif self.curToken in ['&','&amp;']:
                self.outFile.write("<symbol> &amp; </symbol>\n")
            else:
                self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.compileTerm()	

        self.outFile.write("</expression>\n")

    def compileTerm(self):
        self.outFile.write("<term>\n")
        if self.curToken in ['true','false','null','this']:
            # keywordConstant
            self.outFile.write(f"<keyword> {self.curToken} </keyword>\n")
            self.advance()

        elif self.curToken in ['-','~']:
            # UnaryOp term
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            self.compileTerm()
    
        elif self.curToken[0] == '"':
            # StringConstant
            self.outFile.write(f"<stringConstant> {self.curToken[1:-1]} </stringConstant>\n")
            self.advance()

        elif self.curToken.isdigit():
            # IntegerConstant
            self.outFile.write(f"<integerConstant> {self.curToken} </integerConstant>\n")
            self.advance()

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
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()
            self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
            self.advance()
            if self.curToken != "]":
                self.compileExpression()
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
                self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                self.advance()

            elif self.inputTokens[self.i] == ".":
                                     
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
                self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                self.advance()

        else:
            # varName
            self.outFile.write(f"<identifier> {self.curToken} </identifier>\n")
            self.advance()

        self.outFile.write("</term>\n")


    def compileExpressionList(self):
        if self.curToken != ")":
            self.outFile.write("<expressionList>\n")
            self.compileExpression()
            while self.curToken != ")":
                if self.curToken == ",":
                    self.outFile.write(f"<symbol> {self.curToken} </symbol>\n")
                    self.advance()
                    self.compileExpression()
            self.outFile.write("</expressionList>\n")
        else:
            self.outFile.write("<expressionList>\n </expressionList>\n")