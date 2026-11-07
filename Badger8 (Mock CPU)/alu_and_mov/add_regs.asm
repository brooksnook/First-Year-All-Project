; add_regs.asm - Add pairs of registers then combine
; (al+bl) + (cl+dl) = (3+4) + (5+6) = 7 + 11 = 18
; Expected: al=18, bl=4, cl=11, dl=6
mov al, 0x03
mov bl, 0x04
mov cl, 0x05
mov dl, 0x06
add al, bl
add cl, dl
add al, cl
mov flags, 0b10000000
