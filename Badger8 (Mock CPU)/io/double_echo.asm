; double_echo.asm - Read a character and print it twice, then a newline
;
; Demonstrates: input polling + using the inp value more than once
; (The value read from inp is stored in al and printed twice.)

; instr 0  ip=0
mov cl, poll          ; cl = address of poll loop

; --- poll loop: ip=2 ---
poll:
; instr 1  ip=2
    mov al, flags
; instr 2  ip=4
    and al, 0b00000100    ; isolate IS (bit 2): 0 if IS=0, 4 if IS=1
; instr 3  ip=6
    je  cl                ; loop while IS=0 (ZF=1 when result=0)

; --- IS=1: character ready ---
; instr 4  ip=8
mov al, inp           ; read the input character
; instr 5  ip=10
mov out, al           ; print it once
; instr 6  ip=12
mov out, al           ; print it again
; instr 7  ip=14
mov out, 0x0a         ; newline
; instr 8  ip=16
mov flags, 0b10000000 ; halt
