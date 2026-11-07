; je_skip_block.asm — ZF=1 causes je to skip a three-instruction block
; al=5, bl=5: sub al, bl -> al=0, ZF=1 -> je fires -> skip block
; cl, dl, ah remain 0 (writes in the skipped block never execute)
; Expected: al=0, bl=5, cl=0, dl=0, ah=0, dh=16(0x10)

mov al, 0x05        ; first value
mov bl, 0x05        ; second value (equal to al)
mov dh, done        ; dh = address of done (skip target)
sub al, bl          ; al = 5 - 5 = 0, ZF=1
je  dh              ; ZF=1 -> skip block

; skipped block
mov cl, 0xff        ; SKIPPED
mov dl, 0xff        ; SKIPPED
mov ah, 0xff        ; SKIPPED

done:
    mov flags, 0b10000000
