; loop_multiply.asm — compute 0x03 * 0x04 = 12 by repeated addition
; al = multiplicand (3), bl = counter (4 down to 0), cl = accumulator
; loop: cl += al, bl--, exit when bl==0
; Expected: al=3, bl=0, cl=12, dh=10(0x0a), dl=20(0x14)

mov al, 0x03        ; multiplicand = 3
mov bl, 0x04        ; loop counter = 4
mov cl, 0x00        ; accumulator = 0
mov dh, loop        ; dh = address of loop body
mov dl, exit        ; dl = address of exit

loop:
    add cl, al      ; accumulate: cl += al
    sub bl, 0x01    ; decrement counter
    je  dl          ; if bl==0: exit
    ja  dh          ; if bl>0: repeat
mov flags, 0b10000000   ; fallthrough guard (should not be reached)

exit:
    mov flags, 0b10000000
