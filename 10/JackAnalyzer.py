import JackTokenizer 
import JackCompilationEngine
import sys, os

class JackAnalyzer():
    
    def analyze(self, root1):
        tokenizer = JackTokenizer.JackTokenizer(root1)
        compilationEngine = JackCompilationEngine.JackCompilationEngine(compEngOutFile)
        openFile = open(outFile, 'w')
        
        openFile.write("<tokens>\n")       
        # Tokenize the .JACK file
        while tokenizer.hasMoreTokens():
            tokenizer.advance()
            compilationEngine.inputTokens.append(tokenizer.curToken)
            if tokenizer.tokenType() == "KEYWORD":
                tkn = tokenizer.keyWord()
                openFile.write("<keyword> " + tkn + " </keyword>\n") 
            elif tokenizer.tokenType() == "SYMBOL":
                tkn = tokenizer.symbol()
                openFile.write("<symbol> " + tkn + " </symbol>\n")
            elif tokenizer.tokenType() == "INT_CONST":
                tkn = tokenizer.intVal()
                openFile.write("<integerConstant> " + str(tkn) + " </integerConstant>\n")
            elif tokenizer.tokenType() == "STRING_CONST":
                tkn = tokenizer.stringVal()
                openFile.write("<stringConstant> " + tkn + " </stringConstant>\n")
            else:
                tkn = tokenizer.identifier()
                openFile.write("<identifier> " + tkn + " </identifier>\n")
        openFile.write("</tokens>") 
        #print(tokenizer.tokens)

        compilationEngine.compileClass()
               

root = sys.argv[1]
print(root)
outDirectory = ""
outFile = ""
compEngOutFile = ""

if os.path.isdir(root):
    tmpDirectory = []
    
    files = os.listdir(root)
    for file in files:
        if ".jack" in file:            
            tmpDirectory.append(file.replace("jack", "JACK"))
    
    outDirectory = root + "TokenTest"
    try:
        os.mkdir(outDirectory)
    except OSError as error:
        print("DIRECTORY ALREADY EXISTS")
    
    
    for file in tmpDirectory:
        filePath = os.path.join(root, file)
        fileT = file.replace(".JACK", "T")
        outFile = outDirectory + "\\" + (fileT + ".xml")
        compEngOutFile = outDirectory + "\\" + file.replace(".JACK","") + ".xml"
        print(compEngOutFile)
        print(outFile)
        #print(file)
        #print(filePath)
        analyzer = JackAnalyzer()
        analyzer.analyze(filePath)
        print("EOF FOUND\n\n\n")
else:
    #analyzer = JackAnalyzer()
    #analyzer.analyze(root)
    print("SUBMIT DIRECTORY, NOT FILE")
    print("EOF FOUND")