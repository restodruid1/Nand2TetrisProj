import JackTokenizer 
#import JackCompilationEngine
import sys, os

class JackAnalyzer():
    
    def analyze(self, root1):
        tokenizer = JackTokenizer.JackTokenizer(root1)
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            if tokenizer.tokenType() == "KEYWORD":
                tkn = tokenizer.keyWord()
                print("<keyword> " + tkn + " </keyword>") 
            elif tokenizer.tokenType() == "SYMBOL":
                tkn = tokenizer.symbol()
                print("<symbol> " + tkn + " </symbol>")
            elif tokenizer.tokenType() == "INT_CONST":
                tkn = tokenizer.intVal()
                print("<integerConstant> " + str(tkn) + " </integerConstant>")
            elif tokenizer.tokenType() == "STRING_CONST":
                tkn = tokenizer.stringVal()
                print("<stringConstant> " + tkn + " </stringConstant>")
            else:
                tkn = tokenizer.identifier()
                print("<identifier> " + tkn + " </identifier>") 
        #print(tokenizer.tokens)
        



root = sys.argv[1]
print(root)
if os.path.isdir(root):
    tmpDirectory = []
    files = os.listdir(root)
    for file in files:
        if ".jack" in file:            
            tmpDirectory.append(file.replace("jack", "JACK"))
    print(tmpDirectory)
    for file in tmpDirectory:
        filePath = os.path.join(root, file)
        #print(file)
        #print(filePath)
        analyzer = JackAnalyzer()
        analyzer.analyze(filePath)
        print("EOF FOUND\n\n\n")
else:
    analyzer = JackAnalyzer()
    analyzer.analyze(root)
    print("EOF FOUND")