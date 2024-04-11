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
// push constant 4
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

@Main.fibonacci_RETURN_2
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

@1
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

@Main.fibonacci
0;JMP

(Main.fibonacci_RETURN_2)

(END)

@END
0;JMP

(Main.fibonacci)

@0
D=A
@R13
M=D
(Main.fibonacciLOOP)
@Main.fibonacciLOOPEND
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
@Main.fibonacciLOOP
0;JMP
(Main.fibonacciLOOPEND)
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

// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt
@SP
AM=M-1
D=M
@SP
AM=M-1
D=M-D
@JLT_TRUE_0
D;JLT
D=0
@JLT_FALSE_0
0;JMP
(JLT_TRUE_0)
D=-1
(JLT_FALSE_0)
@SP
A=M
M=D
@SP
M=M+1

@SP
AM=M-1
D=M
@N_LT_2
D;JNE

@N_GE_2
0;JMP

(N_LT_2)

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
(N_GE_2)

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

// push constant 2
@2
D=A
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

@Main.fibonacci_RETURN_3
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

@1
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

@Main.fibonacci
0;JMP

(Main.fibonacci_RETURN_3)

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

// push constant 1
@1
D=A
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

@Main.fibonacci_RETURN_4
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

@1
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

@Main.fibonacci
0;JMP

(Main.fibonacci_RETURN_4)

// add
@SP
AM=M-1
D=M
A=A-1
M=D+M

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
