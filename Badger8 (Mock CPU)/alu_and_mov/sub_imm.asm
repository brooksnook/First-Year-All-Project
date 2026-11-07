; sub_imm.asm - Subtract 50 four times from 200, reaching 0
; 200 - 50 - 50 - 50 - 50 = 0
; Expected: al=0
mov al, 0xc8
sub al, 0x32
sub al, 0x32
sub al, 0x32
sub al, 0x32
mov flags, 0b10000000
