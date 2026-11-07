; ja_no_jump.asm - ja does NOT fire when a < b (CF=1, borrow after sub)
; 3 - 15 underflows: ZF=0, CF=1 -> ja condition (CF=0) not met -> falls through
; Expected: al=244 (3-15 mod 256), bl=15, cl=20, dl=42

; instr 0  ip=0
mov al, 0x03        ; al=3
; instr 1  ip=2
mov bl, 0x0f        ; bl=15
; instr 2  ip=4
sub al, bl          ; al=244 (borrow), ZF=0, CF=1  (3 < 15)
; instr 3  ip=6
mov cl, 0x14        ; cl=20 (far address, should not jump)
; instr 4  ip=8
ja cl               ; CF=1 -> condition not met, no jump
; instr 5  ip=10
mov dl, 0x2a        ; dl=42  (EXECUTED - proves no jump)
; instr 6  ip=12
mov flags, 0b10000000
