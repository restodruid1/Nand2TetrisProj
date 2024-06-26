symbol  = "(){}.;[],+-*&|<>=~/"
keyword = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]

class JackTokenizer():
    inputFile = ""
    openFile = ""
    nextLine = ""
    tokens = []
    curToken = ""
    i = 0
    test = False

    
    # Tokenize the input file
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.openFile = open(self.inputFile, 'r')
        self.nextLine = self.openFile.readline()
        self.tokens = []
        self.inst = True
        self.eof = False

        # Returns True if the line is not EOF
        while self.nextLine:
                    
            if self.nextLine.strip() == "" or self.nextLine.strip()[0] == "/" or self.nextLine.strip()[0] == "*":
                self.nextLine = self.openFile.readline()               
            else:
                # Tokenize each item of every line in the input file
                self.createTokenList()
                self.nextLine = self.openFile.readline()

        self.openFile.close()    


    def createTokenList(self):
        #Tokenize the input file here
        inputLine = self.nextLine.strip()
        currentToken = ""
        strConst = False
        intConst = False
        comment = False
        tmp = ""
        
        for letter in inputLine:
            if "/" in letter or "*" in letter:
                if comment == False:
                    comment = True
                    tmp += letter
                    continue
                currentToken = ""
                tmp = ""
                comment = False
                break
                

            if strConst and letter != '"':
                currentToken += letter
                continue
            elif strConst and letter == '"':
                currentToken += letter
                self.tokens.append(currentToken)
                strConst = False
                currentToken = ""
                continue
            elif strConst == False and letter == '"':
                currentToken += letter
                strConst = True
                continue

            if letter in symbol and currentToken == "":
                if tmp != "":
                    self.tokens.append(tmp)
                    tmp = ""
                if letter == "<":
                    self.tokens.append("&lt;")
                elif letter == ">":
                    self.tokens.append("&gt;")
                elif letter == "&":
                    self.tokens.append("&amp;")    
                else:
                    self.tokens.append(letter)
                continue
            elif letter in symbol and currentToken != "":
                if tmp != "":
                    self.tokens.append(tmp)
                    tmp = ""
                self.tokens.append(currentToken)
                self.tokens.append(letter)
                intConst = False
                currentToken = ""
                continue

            if letter.isdigit() and currentToken == "":
                currentToken += letter
                intConst = True
                continue
            elif letter.isdigit() and currentToken != "" and intConst:
                currentToken += letter
                continue 
            elif letter.isdigit() == False and intConst:
                self.tokens.append(currentToken)
                intConst = False
                continue

            if letter == " " and currentToken != "":
                self.tokens.append(currentToken)
                currentToken = ""
                intConst = False
                continue
            if letter != " ":
                if tmp != "":
                    self.tokens.append(tmp)
                    tmp = ""
                currentToken += letter
                continue


        #print(self.tokens)


    # Return True if there are more tokens left
    def hasMoreTokens(self):
        if self.i < len(self.tokens):
            return True
        else:
            self.i = 0
            False
    
    
    
    # If hasMoreTokens is true, this grabs the next token
    def advance(self):
        self.curToken = self.tokens[self.i]
        #print(self.curToken, self.i)
        self.i += 1
       
    
    # Returns the type of token from advance()
    def tokenType(self):
        if self.curToken in symbol or self.curToken in ["&lt;","&gt;","&amp;"]:
            return "SYMBOL"
        elif self.curToken in keyword:
            return "KEYWORD"
        elif self.curToken.isdigit():
            return "INT_CONST"
        elif '"' in self.curToken:
            return "STRING_CONST"
        else:
            return "INDENTIFIER"

    def keyWord(self):
        return self.curToken

    def symbol(self):
        return self.curToken

    def identifier(self):
        return self.curToken

    def intVal(self):
        return int(self.curToken)

    def stringVal(self):
        return self.curToken.strip('"')
        