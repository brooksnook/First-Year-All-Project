; power_of_two.asm — double al three times: 1 -> 2 -> 4 -> 8
; al = value to double (starts 1), cl = iteration counter (3 down to 0)
; loop: al = al + al, cl--, exit when cl==0
; Expected: al=8, cl=0, dh=8(0x08), dl=18(0x12)

mov al, 0x01        ; initial value = 1
mov cl, 0x03        ; 3 iterations
mov dh, loop        ; dh = address of loop body
mov dl, exit        ; dl = address of exit

loop:
    add al, al      ; double al
    sub cl, 0x01    ; decrement counter
    je  dl          ; if cl==0: exit
    ja  dh          ; if cl>0: repeat
mov flags, 0b10000000   ; fallthrough guard (should not be reached)

exit:
    mov flags, 0b10000000
