; je_equal.asm - je fires when ZF=1, i.e., when two values are equal (a - b = 0)
; sub 7, 7 → result=0, ZF=1, CF=0 → je fires (skips dl and ah writes)
; cl = 14 is the address of the halt instruction (instruction 7, ip=14)
; dl and ah should NOT be set (0xff writes are skipped since je jumps over them)
; Expected: al=0, bl=7, cl=14, dl=0, ah=0

; instr 0  ip=0
mov al, 0x07
; instr 1  ip=2
mov bl, 0x07
; instr 2  ip=4
sub al, bl          ; al=0, ZF=1, CF=0  (7==7)
; instr 3  ip=6
mov cl, 0x0e        ; cl=14 (jump target: halt at ip=14)
; instr 4  ip=8
je cl               ; ZF=1 -> jump to ip=14, skip dl/ah writes
; instr 5  ip=10
mov dl, 0xff        ; SKIPPED
; instr 6  ip=12
mov ah, 0xff        ; SKIPPED
; instr 7  ip=14
mov flags, 0b10000000
