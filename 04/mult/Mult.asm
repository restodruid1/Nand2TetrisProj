@R0
@R1
@R2
M = 0		// Set R2 to 0

(LOOP)
@R1 		// Look at reg 1 
D = M

@END
D;JLE  		// If R1 <= 0 goto END

@R0			// Take R0
D = M
@R2			// Take R2
M = D + M 	// Add contents of R0 to R2 (Multiplaction by addition)
@R1
M = M - 1 	// Decrement the R1 register (our loop iterator)
@LOOP 		// Jump back to the begginging of loop
0;JMP

(END)
@END
0;JMP // Infinite loop