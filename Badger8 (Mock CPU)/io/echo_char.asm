; echo_char.asm - Wait for a keypress and echo it to the screen
;
; Input polling idiom:
;   1. Read flags into a register.
;   2. AND to isolate IS (bit 2, value 0b00000100): 0 if IS=0, 4 if IS=1.
;   3. JE loops while IS=0 (ZF=1 when result=0).
;      Falls through when IS=1 (ZF=0, result=4).

; instr 0  ip=0
mov cl, poll          ; cl = address of poll loop

; --- poll loop: ip=2 ---
poll:
; instr 1  ip=2
    mov al, flags         ; al = flags register
; instr 2  ip=4
    and al, 0b00000100    ; isolate IS (bit 2): 0 if IS=0, 4 if IS=1
; instr 3  ip=6
    je  cl                ; loop while IS=0 (ZF=1 when result=0)

; --- IS=1: character ready ---
; instr 4  ip=8
mov al, inp           ; read the input character
; instr 5  ip=10
mov out, al           ; echo to screen
; instr 6  ip=12
mov out, 0x0a         ; newline
; instr 7  ip=14
mov flags, 0b10000000 ; halt
