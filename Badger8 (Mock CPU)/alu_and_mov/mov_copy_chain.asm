; mov_copy_chain.asm - Copy a value through a chain of registers
; Expected: al=bl=cl=dl=ah=85 (0x55)
mov al, 0x55
mov bl, al
mov cl, bl
mov dl, cl
mov ah, dl
mov flags, 0b10000000
