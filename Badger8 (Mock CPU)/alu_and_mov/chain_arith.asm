; chain_arith.asm - Mixed add/sub/not chain
; 10 + 5 - 3 + 7 - 2 = 17  (saved to bl)
; NOT(17) = 238  (left in al)
; Expected: al=238, bl=17
mov al, 0x0a
add al, 0x05
sub al, 0x03
add al, 0x07
sub al, 0x02
mov bl, al
not al
mov flags, 0b10000000
