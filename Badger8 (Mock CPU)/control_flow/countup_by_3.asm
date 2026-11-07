; countup_by_3.asm — count from 0 to 12 in steps of 3 (4 iterations)
; al = accumulator, bl = iteration counter (4 down to 0)
; loop: al += 3, bl--, exit when bl==0
; Expected: al=12, bl=0, dh=8(0x08), dl=18(0x12)

mov al, 0x00        ; accumulator = 0
mov bl, 0x04        ; iteration counter = 4
mov dh, loop        ; dh = address of loop body
mov dl, exit        ; dl = address of exit

loop:
    add al, 0x03    ; al += 3
    sub bl, 0x01    ; counter--
    je  dl          ; if bl==0: exit
    ja  dh          ; if bl>0: repeat
mov flags, 0b10000000   ; fallthrough guard (should not be reached)

exit:
    mov flags, 0b10000000
