; conditional_branch.asm - Branch on comparison: if al > bl set cl=1, else cl=2
; al=8, bl=5: 8-5=3, ZF=0, CF=0 -> ja fires -> cl stays 1, dl write skipped
; Expected: al=3, bl=5, cl=1, dl=0

; instr 0  ip=0
mov al, 0x08        ; al=8
; instr 1  ip=2
mov bl, 0x05        ; bl=5
; instr 2  ip=4
mov cl, 0x01        ; cl=1 ("above" branch marker)
; instr 3  ip=6
sub al, bl          ; al=3, ZF=0, CF=0  (8>5)
; instr 4  ip=8
mov dl, 0x10        ; dl=16 (halt address)
; instr 5  ip=10
ja dl               ; 8>5 -> jump to ip=16 (halt), cl stays 1
; instr 6  ip=12
mov cl, 0x02        ; cl=2 ("not above" branch - SKIPPED)
; instr 7  ip=14
nop

; --- halt: ip=16 ---
; instr 8  ip=16
mov flags, 0b10000000
