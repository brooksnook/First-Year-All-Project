; al, ah
mov al, 0x01
mov ah, 0x02
add al, ah
mov flags, 0b10000000 ; Set the halt flag to stop the CPU