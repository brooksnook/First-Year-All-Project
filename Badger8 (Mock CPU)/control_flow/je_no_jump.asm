; je_no_jump.asm - je does NOT fire when values differ (a - b != 0, ZF=0)
; Falls through to execute dl=42, confirming je didn't branch
; Expected: al=4, bl=3, cl=20, dl=42

; instr 0  ip=0
mov al, 0x07
; instr 1  ip=2
mov bl, 0x03
; instr 2  ip=4
sub al, bl          ; al=4, ZF=0, CF=0  (7 > 3, not equal)
; instr 3  ip=6
mov cl, 0x14        ; cl=20 (far address, should not be jumped to)
; instr 4  ip=8
je cl               ; ZF=0 -> no jump
; instr 5  ip=10
mov dl, 0x2a        ; dl=42  (EXECUTED - proves no jump)
; instr 6  ip=12
mov flags, 0b10000000
