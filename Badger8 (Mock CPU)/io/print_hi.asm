; print_hi.asm - Print "HI!\n" to the screen (output only)
; Demonstrates register-mapped output: mov out, <imm/reg> prints a character.

; instr 0  ip=0
mov out, 0x48         ; 'H'
; instr 1  ip=2
mov out, 0x49         ; 'I'
; instr 2  ip=4
mov out, 0x21         ; '!'
; instr 3  ip=6
mov out, 0x0a         ; '\n' (newline)
; instr 4  ip=8
mov flags, 0b10000000 ; halt
