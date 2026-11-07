; add_imm.asm - Repeated doubling via immediate addition: 1+1=2+2=4+4=8+8=16+16=32
; Expected: al=32
mov al, 0x01
add al, 0x01
add al, 0x02
add al, 0x04
add al, 0x08
add al, 0x10
mov flags, 0b10000000
