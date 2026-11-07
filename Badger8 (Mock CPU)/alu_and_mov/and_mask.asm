; and_mask.asm - AND with bitmasks to isolate nibbles and alternating bits
; al = 0xFF & 0x0F = 0x0F = 15  (lower nibble)
; bl = 0xAB & 0xF0 = 0xA0 = 160 (upper nibble)
; cl = 0xFF & 0x55 = 0x55 = 85  (alternating bits)
; Expected: al=15, bl=160, cl=85
mov al, 0xff
and al, 0x0f
mov bl, 0xab
and bl, 0xf0
mov cl, 0xff
and cl, 0x55
mov flags, 0b10000000
