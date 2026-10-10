; x86-64 assembly program that shows some lil rocks moving
; assemble with nasm -f elf64

%define	BUFFER_SIZE			100 ; one more than limit to account for new line

section .bss
	_map resb BUFFER_SIZE ; stores original input
    _output resb BUFFER_SIZE ; stores output for simulation

section .data
    ; various messages
    invalid_character_error db "Invalid character:  ", 0xA
    invalid_character_error_len equ $ - invalid_character_error

    input_size_error db "Input should be smaller than 99 characters.", 0xA
    input_size_error_len equ $ - input_size_error

    input_size_message db "Input size is:    ", 0xA
    input_size_message_len equ $ - input_size_message

section .text
    global	_start
	global	_read
	global	_print

;
; int _read (void *, int len)
;
;  in: rdi addr, rsi len
; out: rax - bytes read
; taken from lecturer

_read:
	push	rbp
	mov		rbp, rsp
	sub		rsp, 16
	mov		rbp[-8], rdi		; addr
	mov		rbp[-16], rsi		; len

	mov		rax, 0			; read(2)
	mov		rdi, 0			; stdin
	mov		rsi, rbp[-8]
	mov		rdx, rbp[-16]
	syscall

	mov		rsp, rbp
	pop		rbp
	; rax contains number of bytes read
	ret

;
; int _error (void *, int len)
;
;  in: rdi addr, rsi len
; out: rax - bytes read
;

_error:
    push    rbp
    mov     rbp, rsp
    sub     rsp, 16
    mov     rbp[-8], rdi    ; address of message
    mov     rbp[-16], rsi   ; length of message

    mov     rax, 1      ; write  
    mov     rdi, 2      ; select stderr
    mov     rsi, rbp[-8]
    mov     rdx, rbp[-16]
    syscall

	; done, call exit (2)
	mov		rax, 60
	mov		rdi, 0x1 ; adds exit call of one to indicate something went wrong
    syscall

    mov     rsp, rbp
    pop     rbp

    ret

;
; int _print (void *, int len)
;
;  in: rdi addr, rsi len
; out: rax - bytes written
;

_print:
	push	rbp
	mov		rbp, rsp
	sub		rsp, 16
	mov		rbp[-8], rdi		; addr
	mov		rbp[-16], rsi		; len

	mov		rax, 1			; write(2)
	mov		rdi, 1			; stdout
	mov		rsi, rbp[-8]
	mov		rdx, rbp[-16]
	syscall

	mov		rsp, rbp
	pop		rbp
	; rax contains number of bytes written
	ret

; prints map
; length of map should be stored in r9 and map should be stored in buffer _map
_print_map:
	push	rbp
	mov		rbp, rsp

	mov		rax, 1			; write(2)
	mov		rdi, 1			; stdout
	mov		rsi, _map
	mov		rdx, r9
	syscall

	mov		rsp, rbp
	pop		rbp
	; rax contains number of bytes written
	ret

; start of the program
_start:
	mov		rdi, _map
	mov		rsi, BUFFER_SIZE
	call	_read
    
    ; checking if it's above the maximum size 
    cmp     rax, BUFFER_SIZE
    je      check_for_error
    jb      valid_input_length

    check_for_error:
        ; checks if last byte is new line or another character
        mov     rdi, _map
        mov     byte r9b, [rdi + (BUFFER_SIZE - 1)]
        xor     rdi, rdi
        cmp     r9b, 0xA
        je      valid_input_length
        ; moves prints the error message to std err
        mov     rdi, input_size_error
        mov     rsi, input_size_error_len
        call _error
    valid_input_length:
        mov     r9, rax ; stores the number of bytes read in register nine

        cmp     r9, 10 ; checks for how many digits should be printed for the length
        jbe     printonedigit
        ja      printtwodigit
        
    printonedigit:
        mov     rax, r9
        add     rax, 0x2F   ; add one less than 0x30 to account for new line

        ; moves length into input size message
        mov     [abs input_size_message + (input_size_message_len - 3)], al
        
        ; prints input size message
        mov     rdi, input_size_message
        mov     rsi, input_size_message_len
        call    _print

        jmp validity_check

    ; partially taken from lecturer
    printtwodigit:
        ; Clear dcx
        mov rdx, 0
        mov rax, r9
        dec rax     ; decrement to account for new line
        mov rbx, 0xA
        ; Divide by 10
        div rbx
        ; add 0x30 to get ascii code of digit
        add rax, 0x30
        add rdx, 0x30

        ; moves quotient to tens column
        mov [abs input_size_message + (input_size_message_len - 4)], al
        ; moves remainder to ones column
        mov [abs input_size_message + (input_size_message_len - 3)], dl

        ; prints input size message
        mov rdi, input_size_message
        mov rsi, input_size_message_len
        call _print

        jmp validity_check

    ; checks if all characters are valid
    validity_check:
        ; uses rcx as counter for character
        xor rcx, rcx
        ; r11 used for storing position of last character
        mov r11, r9
        ; first character is zero and last character is bytes read - one 
        ; so r11 should be decremented
        dec r11

        validity_loop:
            ; moves character into r10
            mov r10b, [_map + rcx]

            ; compares r10 to every character to make sure it's valid
            cmp r10b, '-'      ; compare to -
            je valid_character
            cmp r10b, 'x'      ; compare to x
            je valid_character
            cmp r10b, 'o'      ; compare to o
            je valid_character
            ; 0xA is a new line
            cmp r10b, 0xA
            je valid_character
            
            jmp invalid_character

            valid_character: 
                ; increments rcx for next character
                inc rcx
                ; checks if were at the last character
                cmp rcx, r11
                jb validity_loop
                jae run_simulation
        
        invalid_character:
            ; moves the invalid character to the last letter of the invalid character message
            mov [abs invalid_character_error + (invalid_character_error_len - 2)], r10b
            ; prints invalid character message to stderr
            mov rdi, invalid_character_error
            mov rsi, invalid_character_error_len
            call _error

    ; simulation being run after all data validation 
    run_simulation:
        ; prints out the input
        call    _print_map
        ; if only one character and the new line was read, simulation is finished
        ; and we can exit
        cmp     r9, 2
        je      success

        ; r10 used for position of current character
        xor     r10, r10
        ; r13 used for tracking iterations of simulation
        ; starts at two to account for new line being read
        xor     r13, r13
        mov     r13, 2
        
        mov     rsi, _map
        mov     rdi, _output
        find_rock:
            ; r11b stores byte of current character
            xor     r11, r11
            mov     r11b, [rsi + r10]
            ; checks if the current character is the new line
            ; if we are then we are at the end and we can move on
            cmp     r11b, 0x0A
            je      next_iteration

            ; r12b stores byte of next character
            xor     r12, r12
            mov     r12b, [rsi + r10 + 1]

            ; checks whether current character is a rock, hole, or dash
            cmp     r11b, 'x'
            je      rock_found

            cmp     r11b, 'o'
            je      hole_found

            cmp     r11b, '-'
            je      dash_found
            rock_found:
                ; checks if next character is dash
                cmp     r12b, '-'
                je      move_rock
                ; checks if next characer is a hole
                cmp     r12b, 'o'
                je      drop_in_hole
                ; checks if the rock is next to a rock
                cmp     r12b, 'x'
                je      rock_next
                move_rock:
                    ; sees if the rock is at the edge by checking if the next characer
                    ; is the newline
                    cmp     r12b, 0xA
                    je      last
                    jne     not_last
                    last:
                        ; doesn't move anything if the rock is the last character
                        mov     byte [rdi + r10], 'x'
                        jmp     next_char
                    not_last: 
                        ; makes current character dash
                        mov     byte [rdi + r10], '-'
                        ; makes next chararacter rock
                        mov     byte [rdi + r10 + 1], 'x'
                        ; another inc to account for rock moving
                        inc     r10
                        jmp     next_char
                drop_in_hole:
                    ; replaces current character with dash
                    mov     byte [rdi + r10], '-'
                    ; replaces hole with dash to "fill hole in"
                    mov     byte [rdi + r10 + 1], '-'
                    inc     r10
                    jmp     next_char
                rock_next:
                    ; doesn't move the rock if it's next to a rock
                    mov     byte [rdi + r10], 'x'
                    jmp     next_char
            hole_found:
                ; moves nothing if there's a hole
                mov     byte [rdi + r10], 'o'
                jmp     next_char
            dash_found:
                ; moves nothing if there's a dash
                mov     byte [rdi + r10], '-'
                jmp next_char

            next_char:
                ; incs to last character
                inc     r10
                jmp     find_rock 
        next_iteration: 
            ; adds newline
            mov     byte [rdi + r10], 0x0A

            xor     r10, r10
            ; moves length to rsi for printing
            mov     rsi, r9
            call    _print

            ; moves latest interation into rsi and rdi
            mov     rsi, _output
            mov     rdi, _output
            
            ; checks if we've run enough iterations 
            inc     r13
            cmp     r13, r9
            jb      find_rock
            jae     success

    ; taken from lectuerer
    success:
	    ; done, call exit (2)
	    mov		rax, 60
        ; sets rdi to zero to indicate code ran successfully
	    xor		rdi, rdi
        syscall
