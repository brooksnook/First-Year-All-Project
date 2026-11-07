; max_two.asm — find the maximum of 0x07 and 0x03, stored in cl
; ah saves the original al before sub destroys it
; sub al, bl: 7 - 3 = 4, ZF=0, CF=0 (al > bl) -> ja fires -> use_al
; use_al: cl = ah = original al = 7
; Expected: ah=7, al=4(sub result), bl=3, cl=7, dh=16(0x10)

mov al, 0x07        ; first value
mov ah, 0x07        ; backup of al (sub destroys al)
mov bl, 0x03        ; second value
mov dh, use_al      ; dh = address of use_al branch
sub al, bl          ; al = 7 - 3 = 4, ZF=0, CF=0
ja  dh              ; al > bl: jump to use_al

; al <= bl path: cl = bl (the maximum)
mov cl, bl          ; SKIPPED in this test case
mov flags, 0b10000000   ; SKIPPED

use_al:
    mov cl, ah      ; cl = original al = max
    mov flags, 0b10000000
