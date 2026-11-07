; ja_above.asm - ja fires when a > b (ZF=0, CF=0 after sub)
; 15 - 5 = 10, no borrow, not zero -> ja jumps, skipping dl=0xFF
; Expected: al=10, bl=5, cl=14, dl=0

; instr 0  ip=0
mov al, 0x0f        ; al=15
; instr 1  ip=2
mov bl, 0x05        ; bl=5
; instr 2  ip=4
sub al, bl          ; al=10, ZF=0, CF=0  (15 > 5)
; instr 3  ip=6
mov cl, 0x0e        ; cl=14 (ja target: halt at ip=14)
; instr 4  ip=8
ja cl               ; ZF=0,CF=0 -> jump to ip=14
; instr 5  ip=10
mov dl, 0xff        ; SKIPPED
; instr 6  ip=12
mov ah, 0xff        ; SKIPPED
; instr 7  ip=14
mov flags, 0b10000000
