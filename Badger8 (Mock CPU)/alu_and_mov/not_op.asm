; not_op.asm - NOT on 0x00, 0xFF, and 0x55
; NOT(0x00) = 0xFF = 255
; NOT(0xFF) = 0x00 = 0
; NOT(0x55) = 0xAA = 170
; Expected: al=255, bl=0, cl=170, dl=170
mov al, 0x00
not al
mov bl, 0xff
not bl
mov cl, 0x55
not cl
mov dl, cl
mov flags, 0b10000000
