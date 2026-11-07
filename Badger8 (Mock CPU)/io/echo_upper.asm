; echo_upper.asm - Read a character, convert to uppercase, print it
;
; Uppercase conversion trick:
;   'a'-'z' = 0x61-0x7A = 0b0110xxxx - 0b0111xxxx  (bit 5 = 1)
;   'A'-'Z' = 0x41-0x5A = 0b0100xxxx - 0b0101xxxx  (bit 5 = 0)
;   Clearing bit 5: AND with 0b11011111 (0xDF)
;   This maps lowercase -> uppercase; leaves uppercase unchanged.
;   Non-alphabetic characters are also affected but this demo assumes letter input.

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
mov al, inp               ; read the input character
; instr 5  ip=10
and al, 0b11011111        ; clear bit 5: lowercase -> uppercase
; instr 6  ip=12
mov out, al               ; print the (now uppercase) character
; instr 7  ip=14
mov out, 0x0a             ; newline
; instr 8  ip=16
mov flags, 0b10000000     ; halt
