; countup_to_5.asm - Count al from 0 up to 5 using ja
; Each iteration: al++, then test (5-al): je exits when al==5, ja loops while al<5
; Note: after sub bl,al: if bl>al: ZF=0,CF=0 -> ja loops; if bl==al: ZF=1 -> je exits
; Expected: al=5

; instr 0  ip=0
mov al, 0x00        ; counter=0

; --- loop body: ip=2 ---
; instr 1  ip=2
add al, 0x01        ; al++
; instr 2  ip=4
mov bl, 0x05        ; fresh copy of limit=5
; instr 3  ip=6
sub bl, al          ; bl = 5-al  (destroys bl, but we reload each iteration)
; instr 4  ip=8
mov cl, 0x14        ; cl=20 (exit address)
; instr 5  ip=10
je cl               ; bl==0 (al==5) -> exit to ip=20
; instr 6  ip=12
mov cl, 0x02        ; cl=2  (loop address, overwrites exit value)
; instr 7  ip=14
ja cl               ; bl>0 (al<5): ZF=0,CF=0 -> loop to ip=2
; instr 8  ip=16  (fallthrough, shouldn't happen)
nop
; instr 9  ip=18
nop

; --- exit: ip=20 ---
; instr 10  ip=20
mov flags, 0b10000000
