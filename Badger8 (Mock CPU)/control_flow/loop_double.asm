; loop_double.asm - Double al four times: 1 -> 2 -> 4 -> 8 -> 16
; bl = iteration counter (4 down to 0)
; Loop: al += al (double), bl--; exit when bl==0
; Expected: al=16, bl=0

; instr 0  ip=0
mov al, 0x01        ; value to double
; instr 1  ip=2
mov bl, 0x04        ; iteration counter=4
; instr 2  ip=4
mov ch, 0x08        ; ch=8  (loop body address)
; instr 3  ip=6
mov dh, 0x12        ; dh=18 (exit address)

; --- loop body: ip=8 ---
; instr 4  ip=8
add al, al          ; al *= 2
; instr 5  ip=10
sub bl, 0x01        ; bl--
; instr 6  ip=12
je dh               ; bl==0 -> exit to ip=18
; instr 7  ip=14
ja ch               ; bl>0  -> loop to ip=8
; instr 8  ip=16  (fallthrough, shouldn't happen)
mov flags, 0b10000000

; --- exit: ip=18 ---
; instr 9  ip=18
mov flags, 0b10000000
