; sub_regs.asm - Subtract pairs of registers then combine
; al = 50-15=35, cl = 100-40=60, cl = 60-35=25
; Expected: al=35, bl=15, cl=25, dl=40
mov al, 0x32
mov bl, 0x0f
mov cl, 0x64
mov dl, 0x28
sub al, bl
sub cl, dl
sub cl, al
mov flags, 0b10000000
