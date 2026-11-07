; simple_mov.asm - Move immediate values to several registers
; Expected: al=10, bl=20, cl=30, dl=40, ah=5, bh=15
mov al, 0x0a
mov bl, 0x14
mov cl, 0x1e
mov dl, 0x28
mov ah, 0x05
mov bh, 0x0f
mov flags, 0b10000000
