.global _start
.align 4

_start:
    mov     X0, #1
    adr     X1, head
    mov     X2, #47
    mov     X16, #4
    svc     #0x80

    mov     X0, #1
    adr     X1, body
    mov     X2, #18
    mov     X16, #4
    svc     #0x80

    mov     X0, #0
    mov     X16, #1
    svc     #0x80

head:  .ascii  "asm 200\nContent-Type: text/plain;charset=UTF-8\n"
body:  .ascii  "\nfrom asm to web\n"



