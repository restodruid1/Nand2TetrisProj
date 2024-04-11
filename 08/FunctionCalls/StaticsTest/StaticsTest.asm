@256
D=A
@SP
M=D
@Sys.init_RETURN_1
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

@0
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D

@Sys.init
0;JMP

(Sys.init_RETURN_1)

(BOOTSTRAP_Sys.vm)
@BOOTSTRAP_Sys.vm
0;JMP

(Sys.init)

@0
D=A
@R13
M=D
(Sys.initLOOP)
@Sys.initLOOPEND
D;JEQ
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@R13
MD=M-1
@Sys.initLOOP
0;JMP
(Sys.initLOOPEND)
// push constant 6
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

@Class1.set_RETURN_2
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

@2
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D

@Class1.set
0;JMP

(Class1.set_RETURN_2)

// pop temp 0
@SP
AM=M-1
D=M
@5
M=D

// push constant 23
@23
D=A
@SP
A=M
M=D
@SP
M=M+1

// push constant 15
@15
D=A
@SP
A=M
M=D
@SP
M=M+1

@Class2.set_RETURN_3
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

@2
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D

@Class2.set
0;JMP

(Class2.set_RETURN_3)

// pop temp 0
@SP
AM=M-1
D=M
@5
M=D

@Class1.get_RETURN_4
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

@0
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D

@Class1.get
0;JMP

(Class1.get_RETURN_4)

@Class2.get_RETURN_5
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1

@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1

@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

@0
D=A
@5
D=D+A
@SP
D=M-D
@ARG
M=D

@SP
D=M
@LCL
M=D

@Class2.get
0;JMP

(Class2.get_RETURN_5)

(END)

@END
0;JMP

(Class1.set)

@0
D=A
@R13
M=D
(Class1.setLOOP)
@Class1.setLOOPEND
D;JEQ
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@R13
MD=M-1
@Class1.setLOOP
0;JMP
(Class1.setLOOPEND)
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 0
@SP
AM=M-1
D=M
@Class1.vm.0
M=D

// push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 1
@SP
AM=M-1
D=M
@Class1.vm.1
M=D

// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
D=A
@SP
M=D+1
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Class1.get)

@0
D=A
@R13
M=D
(Class1.getLOOP)
@Class1.getLOOPEND
D;JEQ
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@R13
MD=M-1
@Class1.getLOOP
0;JMP
(Class1.getLOOPEND)
// push static 0
@Class1.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@Class1.vm.1
D=M
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
D=A
@SP
M=D+1
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Class2.set)

@0
D=A
@R13
M=D
(Class2.setLOOP)
@Class2.setLOOPEND
D;JEQ
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@R13
MD=M-1
@Class2.setLOOP
0;JMP
(Class2.setLOOPEND)
// push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 0
@SP
AM=M-1
D=M
@Class2.vm.0
M=D

// push argument 1
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

// pop static 1
@SP
AM=M-1
D=M
@Class2.vm.1
M=D

// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
D=A
@SP
M=D+1
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
(Class2.get)

@0
D=A
@R13
M=D
(Class2.getLOOP)
@Class2.getLOOPEND
D;JEQ
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@R13
MD=M-1
@Class2.getLOOP
0;JMP
(Class2.getLOOPEND)
// push static 0
@Class2.vm.0
D=M
@SP
A=M
M=D
@SP
M=M+1

// push static 1
@Class2.vm.1
D=M
@SP
A=M
M=D
@SP
M=M+1

// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
D=A
@SP
M=D+1
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
