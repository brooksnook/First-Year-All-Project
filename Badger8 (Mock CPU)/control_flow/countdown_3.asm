; countdown_3.asm - Count down from 3 to 0 using je/ja loop
; Loop: sub 1, je exit (ZF=1 when al reaches 0), ja loop (ZF=0,CF=0 while al>0)
; Expected: al=0, bl=6, cl=14  (loop ran 3 times)

; instr 0  ip=0
mov al, 0x03        ; counter=3
; instr 1  ip=2
mov bl, 0x06        ; bl=6  (loop body address)
; instr 2  ip=4
mov cl, 0x0e        ; cl=14 (exit address)

; --- loop body: ip=6 ---
; instr 3  ip=6
sub al, 0x01        ; al--
; instr 4  ip=8
je cl               ; al==0 -> exit to ip=14
; instr 5  ip=10
ja bl               ; al>0  -> loop to ip=6
; instr 6  ip=12  (only reached on underflow, shouldn't happen starting from 3)
mov flags, 0b10000000

; --- exit: ip=14 ---
; instr 7  ip=14
mov flags, 0b10000000
