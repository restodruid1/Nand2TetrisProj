# Run program via command line and pass project06.asm with it
#!/usr/bin/env python3
import sys

 
# c-instruction codes
comp = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
    }


dest = {
    "null": "000",
    "M": "001",
    "D": "010",
    "A": "100",
    "MD": "011",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
    }


jump = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
    }


# table of symbols used in assembly code, initialized to include
# standard ones
table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576,
    }
# Update table with R0-R15
for i in range(0,16):
  label = "R" + str(i)
  table[label] = i


variableCursor = 16    # next available memory location for variables
inputFile = sys.argv[1]     # name of file to be translated


def addVariable(label):
# allocates a memory location for new variables

  global variableCursor
  table[label] = variableCursor
  variableCursor += 1
  return table[label]

def normalize(line):
# normalizes c-instructions by adding null dest & jump fields if they're unspecified

  if not "=" in line:
    line = "null=" + line
  if not ";" in line:
    line = line + ";null"
  return line

def cTranslate(line):
# splits a c-instruction into its components & translates them

  line = normalize(line)
  temp = line.split("=")
  destCode = dest.get(temp[0], "destFAIL")
  temp = temp[1].split(";")
  compCode = comp.get(temp[0], "compFAIL")
  jumpCode = jump.get(temp[1], "jumpFAIL")
  return compCode, destCode, jumpCode

def firstPass():
  outFile = inputFile.replace("asm", "tmp")
  with open(inputFile, 'r') as file, open(outFile, 'w') as file2:
    lineNumber = 0
    for line in file:
      line = line.strip()
      if line != "":
        if line[0] == "(":
          newLine = line.replace('(', '').replace(')', '').replace('\n', '')
          table[newLine] = lineNumber
        elif line[0] == "/":
          line = ""
        else:
          file2.write(line + "\n")
          lineNumber += 1
      


def secondPass():
  outFile = inputFile.replace("asm", "hack")
  inputFile2 = inputFile.replace("asm", "tmp")
  # Translate assembly into binary
  with open(inputFile2, 'r') as file, open(outFile, 'w') as file2:
    for line in file:
      line = line.replace("\n", "")
      # A-instruction
      if line[0] == "@":
        if line[1:] in table:
          tmp = int(table[line[1:]])
          tmp = bin(tmp)[2:].zfill(16)
          file2.write(tmp + "\n")
        elif line[1].isalpha():
          addVariable(line[1:])
          tmp = int(table[line[1:]])
          tmp = bin(tmp)[2:].zfill(16)
          file2.write(tmp + "\n")
        else:
          tmp = int(line[1:])
          tmp = bin(tmp)[2:].zfill(16)
          file2.write(tmp + "\n")
      # C-instruction
      else:
          codes = cTranslate(line)
          codes = "111" + codes[0] + codes[1] + codes[2]
          file2.write(codes + "\n")
    #print(table)

# Assemble 
firstPass()
secondPass()




