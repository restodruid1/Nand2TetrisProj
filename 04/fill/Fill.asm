// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//// Replace this comment with your code.  		
//(LOOP)
//@KBD
//D = A
//@BLACK
//D:JGT		// If keyboard is press, branch to KEY//

//// If keyboard is idle, turn pixels white
//@SCREEN
//D = M
//@addr
//M = D
//M = 0//

//(BLACK)
//// Turn the pixels black
//@SCREEN
//D = M
//@addr
//M = D
//M = -1//

//@LOOP
//0:JMP

(INIT)  	
@8192	 
D=A
@i                   
M=D

(LOOP)	           
@i
M=M-1
D=M
@INIT
D;JLT               
@KBD	            
D=M
@WHITE		        
D;JEQ
@BLACK
0;JMP

(BLACK)             
@SCREEN            
D=A
@i
A=D+M              
M=-1               
@LOOP              
0;JMP

(WHITE)
@SCREEN            
D=A                
@i        
A=D+M              
M=0                
@LOOP           
0;JMP