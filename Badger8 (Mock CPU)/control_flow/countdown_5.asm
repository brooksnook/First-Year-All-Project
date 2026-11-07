; countdown_5.asm - Count down from 5, track number of steps in bl
; Each iteration: bl++, al--; exit when al==0
; Note: bl incremented before sub so je reads flags from sub; final bl=5
; Expected: al=0, bl=5  (5 iterations performed)

; instr 0  ip=0
mov al, 0x05        ; counter=5
; instr 1  ip=2
mov bl, 0x00        ; step counter=0
; instr 2  ip=4
mov ch, 0x08        ; ch=8  (loop body address)
; instr 3  ip=6
mov dh, 0x12        ; dh=18 (exit address)

; --- loop body: ip=8 ---
; instr 4  ip=8
add bl, 0x01        ; bl++ first so sub sets flags used for branches
; instr 5  ip=10
sub al, 0x01        ; al--  (sets ZF=1 when al reaches 0)
; instr 6  ip=12
je dh               ; al==0 -> exit to ip=18
; instr 7  ip=14
ja ch               ; al>0  -> loop to ip=8
; instr 8  ip=16  (fallthrough, shouldn't happen)
mov flags, 0b10000000

; --- exit: ip=18 ---
; instr 9  ip=18
mov flags, 0b10000000
