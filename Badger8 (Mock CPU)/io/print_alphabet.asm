; print_alphabet.asm - Print 'A' through 'Z' followed by a newline
; Uses a loop: al = current letter, bl = remaining count (26 -> 0)
; cl = loop address, dl = exit address

; instr 0  ip=0
mov al, 0x41          ; al = 'A' (65)
; instr 1  ip=2
mov bl, 0x1a          ; bl = 26 (number of letters)
; instr 2  ip=4
mov cl, loop          ; cl = byte address of 'loop' body
; instr 3  ip=6
mov dl, done          ; dl = byte address of 'done'

; --- loop body: ip=8 ---
loop:
; instr 4  ip=8
    mov out, al       ; print current letter
; instr 5  ip=10
    add al, 0x01      ; advance to next ASCII letter
; instr 6  ip=12
    sub bl, 0x01      ; decrement remaining count
; instr 7  ip=14
    je  dl            ; count==0 -> exit
; instr 8  ip=16
    ja  cl            ; count>0  -> repeat

; --- exit: ip=18 ---
done:
; instr 9  ip=18
    mov out, 0x0a     ; newline
; instr 10 ip=20
    mov flags, 0b10000000
