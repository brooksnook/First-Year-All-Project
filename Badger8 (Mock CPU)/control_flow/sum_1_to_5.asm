; sum_1_to_5.asm - Compute 5+4+3+2+1 = 15 using a countdown loop
; al = accumulator, cl = counter (5 down to 0)
; Loop: add cl to al, decrement cl, repeat until cl==0
; Expected: al=15, cl=0

; instr 0  ip=0
mov al, 0x00        ; sum=0
; instr 1  ip=2
mov cl, 0x05        ; counter=5
; instr 2  ip=4
mov dh, 0x08        ; dh=8  (loop body address)
; instr 3  ip=6
mov dl, 0x12        ; dl=18 (exit address)

; --- loop body: ip=8 ---
; instr 4  ip=8
add al, cl          ; sum += counter
; instr 5  ip=10
sub cl, 0x01        ; counter--
; instr 6  ip=12
je dl               ; counter==0 -> exit to ip=18
; instr 7  ip=14
ja dh               ; counter>0  -> loop to ip=8
; instr 8  ip=16  (fallthrough, shouldn't happen)
mov flags, 0b10000000

; --- exit: ip=18 ---
; instr 9  ip=18
mov flags, 0b10000000
